import numpy
import cv2

# avoid logging of caffe networks to console
import os
os.environ['GLOG_minloglevel'] = '2'
import caffe

import logging
logger = logging.getLogger("challenge.uccs")


class MTCNNDetector:
  """This MTCNNv2 implementation is adjusted from https://github.com/walkoncross/mtcnn-caffe-zyf"""

  def __init__(self, gpu_id=0, model_path="./model", min_detection_size = 15., threshold = [0.1, 0.2, 0.2], factor = 0.709, fast_resize = False):
    # set Caffe mode
    if gpu_id is not None:
      caffe.set_device(gpu_id)
      caffe.set_mode_gpu()
    else:
      caffe.set_mode_cpu()

    self.PNet = caffe.Net(os.path.join(model_path,"det1.prototxt"), os.path.join(model_path,"det1.caffemodel"), caffe.TEST)
    self.RNet = caffe.Net(os.path.join(model_path,"det2.prototxt"), os.path.join(model_path,"det2.caffemodel"), caffe.TEST)
    self.ONet = caffe.Net(os.path.join(model_path,"det3.prototxt"), os.path.join(model_path,"det3.caffemodel"), caffe.TEST)
#    self.LNet = caffe.Net(os.path.join(model_path,"det4.prototxt"), os.path.join(model_path,"det4.caffemodel"), caffe.TEST)
    self.LNet = None
    self.min_detection_size = min_detection_size
    self.threshold = threshold
    self.factor = factor
    self.fast_resize = fast_resize


  def detect_faces(self, filename):
    """Detects the faces for the given image name"""
    logger.debug("Detecting faces for image %s", filename)
    img = cv2.imread(filename)
    if img is None:
      raise ValueError("Image file %s not found" % filename)
    min_size = 0.05 * min(img.shape[0], img.shape[1])

    # convert color space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if self.fast_resize:
      img = (img - 127.5) * 0.0078125  # [0,255] -> [-1,1]

    total_boxes = []
    points = []

    h = img.shape[0]
    w = img.shape[1]
    minl = min(h, w)

    m = self.min_detection_size / min_size
    minl = minl * m

    # create scale pyramid
    scales = []
    factor_count = 0
    while minl >= self.min_detection_size:
      scales.append(m * pow(self.factor, factor_count))
      minl *= self.factor
      factor_count += 1

    ##############
    # first stage
    ##############

    # 1.1 run PNet
    for scale in scales:
      hs = int(numpy.ceil(h * scale))
      ws = int(numpy.ceil(w * scale))

      im_data = cv2.resize(img, (ws, hs))  # default is bilinear
      if not self.fast_resize:
          im_data = (im_data - 127.5) * 0.0078125  # [0,255] -> [-1,1]

      im_data = self.adjust_input(im_data)  # from (h, w, c) to (c, w, h)

      self.PNet.blobs['data'].reshape(1, 3, ws, hs)
      self.PNet.blobs['data'].data[...] = im_data
      out = self.PNet.forward()

      boxes = self.generate_bboxes(out['prob1'][0, 1, :, :], out['conv4-2'][0], scale)

      if boxes is None:
        continue

      if boxes.shape[0] > 0:
        # intra-scale nms
        pick = self.nms(boxes, 0.5, False)

        if len(pick) > 0:
          boxes = boxes[pick, :]
          total_boxes.append(boxes)


    total_boxes = numpy.vstack(total_boxes)
    n_boxes = total_boxes.shape[0]

    if n_boxes < 1:
      return img, None

    # 1.2 run NMS on all boxes between scales
    # inter-scale nms
    pick = self.nms(total_boxes, 0.7, False)

    n_boxes = len(pick)
    if n_boxes < 1:
        return img, None

    total_boxes = total_boxes[pick, :]
    total_boxes = self.bbox_reg(total_boxes, total_boxes[:, 5:].T)


    ###############
    # second stage
    ###############

    # 2.1 construct input for RNet
    total_boxes = self.convert_to_squares(total_boxes)  # convert box to square
    total_boxes[:, 0:4] = numpy.fix(total_boxes[:, 0:4])
    dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = self.pad(total_boxes, w, h)

    tmp_img = numpy.zeros((n_boxes, 24, 24, 3))  # (24, 24, 3, n_boxes)
    for k in range(n_boxes):
        tmp = numpy.zeros((int(tmph[k]), int(tmpw[k]), 3))
        tmp[dy[k]:edy[k] + 1, dx[k]:edx[k] +
            1] = img[y[k]:ey[k] + 1, x[k]:ex[k] + 1]

        tmp_img[k, :, :, :] = cv2.resize(tmp, (24, 24))

    # 2.2 run RNet
    if not self.fast_resize:
        tmp_img = (tmp_img - 127.5) * 0.0078125  # [0,255] -> [-1,1]

    tmp_img = numpy.swapaxes(tmp_img, 1, 3)  # from (N, h, w, c) to (N, c, w, h)

    self.RNet.blobs['data'].reshape(n_boxes, 3, 24, 24)
    self.RNet.blobs['data'].data[...] = tmp_img
    out = self.RNet.forward()

    scores = out['prob1'][:, 1]
    pass_t = numpy.where(scores > self.threshold[1])[0]

    n_boxes = pass_t.shape[0]

    if n_boxes < 1:
        return img, None

    scores = numpy.array([scores[pass_t]]).T
    total_boxes = numpy.concatenate((total_boxes[pass_t, 0:4], scores), axis=1)
    reg_factors = out['conv5-2'][pass_t, :].T

    # 2.3 NMS
    pick = self.nms(total_boxes, 0.7, False)

    n_boxes = len(pick)
    if n_boxes < 1:
        return img, None

    total_boxes = total_boxes[pick, :]
    total_boxes = self.bbox_reg(total_boxes, reg_factors[:, pick])


    ###############
    # third stage
    ###############

    # 3.1 construct input for ONet
    total_boxes = self.convert_to_squares(total_boxes)
    total_boxes = numpy.fix(total_boxes)
    dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = self.pad(total_boxes, w, h)

    tmp_img = numpy.zeros((n_boxes, 48, 48, 3))
    for k in range(n_boxes):
      tmp = numpy.zeros((tmph[k], tmpw[k], 3))
      tmp[dy[k]:edy[k] + 1, dx[k]:edx[k] + 1] = img[y[k]:ey[k] + 1, x[k]:ex[k] + 1]
      tmp_img[k, :, :, :] = cv2.resize(tmp, (48, 48))

    # 3.2 run ONet
    if not self.fast_resize:
      tmp_img = (tmp_img - 127.5) * 0.0078125  # [0,255] -> [-1,1]

    tmp_img = numpy.swapaxes(tmp_img, 1, 3)  # from (N, h, w, c) to (N, c, w, h)
    self.ONet.blobs['data'].reshape(n_boxes, 3, 48, 48)
    self.ONet.blobs['data'].data[...] = tmp_img
    out = self.ONet.forward()

    scores = out['prob1'][:, 1]
    points = out['conv6-3']
    pass_t = numpy.where(scores > self.threshold[2])[0]

    n_boxes = pass_t.shape[0]
    if n_boxes < 1:
      return img, None

    points = points[pass_t, :]
    scores = numpy.array([scores[pass_t]]).T
    total_boxes = numpy.concatenate((total_boxes[pass_t, 0:4], scores), axis=1)

    reg_factors = out['conv6-2'][pass_t, :].T
    boxes_w = total_boxes[:, 3] - total_boxes[:, 1] + 1
    boxes_h = total_boxes[:, 2] - total_boxes[:, 0] + 1

    points[:, 0:5] = numpy.tile(boxes_w, (5, 1)).T * points[:, 0:5] + numpy.tile(total_boxes[:, 0], (5, 1)).T - 1
    points[:, 5:10] = numpy.tile(boxes_h, (5, 1)).T * points[:, 5:10] + numpy.tile(total_boxes[:, 1], (5, 1)).T - 1

    total_boxes = self.bbox_reg(total_boxes, reg_factors)

    pick = self.nms(total_boxes, 0.7, True)

    n_boxes = len(pick)
    if n_boxes < 1:
      return img, None

    total_boxes = total_boxes[pick, :]
    points = points[pick, :]
    scores = scores[pick, :]


    #################
    # extended stage
    #################

    if self.LNet is not None:
      # 4.1 construct input for LNet
      patchw = numpy.maximum(total_boxes[:, 2] - total_boxes[:, 0] + 1, total_boxes[:, 3] - total_boxes[:, 1] + 1)
      patchw = numpy.round(patchw * 0.25)

      # make it even
      patchw[numpy.where(numpy.mod(patchw, 2) == 1)] += 1

      pointx = numpy.zeros((n_boxes, 5))
      pointy = numpy.zeros((n_boxes, 5))

      tmp_img = numpy.zeros((n_boxes, 15, 24, 24), dtype=numpy.float32)
      for i in range(5):
        x, y = points[:, i], points[:, i + 5]
        x, y = numpy.round(x - 0.5 * patchw), numpy.round(y - 0.5 * patchw)
        [dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph] = self.pad(numpy.vstack([x, y, x + patchw - 1, y + patchw - 1]).T, w, h)

        for j in range(n_boxes):
          tmpim = numpy.zeros((tmpw[j], tmpw[j], 3), dtype=numpy.float32)
          tmpim[dy[j]:edy[j] + 1, dx[j]:edx[j] + 1, :] = img[y[j]:ey[j] + 1, x[j]:ex[j] + 1, :]
          tmp_img[j, i * 3:i * 3 + 3, :, :] = self.adjust_input(cv2.resize(tmpim, (24, 24)))

      # 4.2 run LNet
      if not self.fast_resize:
        tmp_img = (tmp_img - 127.5) * 0.0078125  # [0,255] -> [-1,1]

      self.LNet.blobs['data'].reshape(n_boxes, 15, 24, 24)
      self.LNet.blobs['data'].data[...] = tmp_img
      out = self.LNet.forward()

      for k in range(5):
        # do not make a large movement
        layer_name = 'fc5_' + str(k + 1)
        tmp_index = numpy.where(numpy.abs(out[layer_name] - 0.5) > 0.35)
        out[layer_name][tmp_index[0]] = 0.5

        pointx[:, k] = numpy.round(points[:, k] - 0.5 * patchw) + out[layer_name][:, 0] * patchw
        pointy[:, k] = numpy.round(points[:, k + 5] - 0.5 * patchw) + out[layer_name][:, 1] * patchw

      points = numpy.hstack([pointx, pointy])

    return img, (total_boxes.tolist(), points.tolist(), scores.tolist())



  def adjust_input(self, in_data):
    """Adjust the input from (h, w, c) to (1, c, w, h) for network input."""
    out_data = in_data.astype(numpy.float32)
    out_data = numpy.expand_dims(out_data, 0)  # from (h, w, c) to (1, h, w, c)
    return numpy.swapaxes(out_data, 1, 3)  # from (N, h, w, c) to (N, c, w, h)


  def generate_bboxes(self, scores_map, reg, scale):
    """Generates boudning boxes out of the output of the first stage"""
    stride = 2
    cellsize = 12

    y, x = numpy.where(scores_map >= self.threshold[0])

    if len(y) < 1:
        return None

    scores = scores_map[y, x]

    dx1, dy1, dx2, dy2 = (reg[i, y, x] for i in range(4))

    reg = numpy.array(reg[:4, y, x])

    bbox = numpy.array([y, x])
    bb1 = numpy.fix((stride * bbox) / scale)
    bb2 = numpy.round((stride * bbox + cellsize) / scale)

    bbox_out = numpy.vstack((bb1, bb2, scores, reg))
    return bbox_out.T


  def nms(self, boxes, threshold, use_min):
    """Performs non-maximum-suppression (NMS) on the given bounding boxes
    :boxes: [:,0:5]
    :threshold: 0.5 like
    :use_min: boolean
    :returns: TODO
    """
    if boxes.shape[0] == 0:
        return numpy.array([])

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    score = boxes[:, 4]
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = numpy.argsort(score)

    pick = []
    while len(idxs) > 0:
      last = len(idxs) - 1
      i = idxs[last]
      pick.append(i)

      xx1 = numpy.maximum(x1[i], x1[idxs[0:last]])
      yy1 = numpy.maximum(y1[i], y1[idxs[0:last]])
      xx2 = numpy.minimum(x2[i], x2[idxs[0:last]])
      yy2 = numpy.minimum(y2[i], y2[idxs[0:last]])
      w = numpy.maximum(0.0, xx2 - xx1 + 1)
      h = numpy.maximum(0.0, yy2 - yy1 + 1)
      inter = w * h

      if use_min:
        overlap = inter / numpy.minimum(area[i], area[idxs[0:last]])
      else:
        overlap = inter / (area[i] + area[idxs[0:last]] - inter)

      idxs = numpy.delete(idxs, numpy.concatenate(([last], numpy.where(overlap > threshold)[0])))
    return pick


  def bbox_reg(self, bbox, reg):
    """No idea, what this function is doing"""
    reg = reg.T

    w = bbox[:, 2] - bbox[:, 0] + 1
    w = numpy.expand_dims(w, 1)
    h = bbox[:, 3] - bbox[:, 1] + 1
    h = numpy.expand_dims(h, 1)

    reg_m = numpy.hstack([w, h, w, h])
    aug = reg_m * reg

    bbox[:, 0:4] = bbox[:, 0:4] + aug
    return bbox


  def convert_to_squares(self, bboxA):
    """Convert the given bounding box to square"""
    w = bboxA[:, 2] - bboxA[:, 0]
    h = bboxA[:, 3] - bboxA[:, 1]
    max_side = numpy.maximum(w, h).T

    bboxA[:, 0] = bboxA[:, 0] + w * 0.5 - max_side * 0.5
    bboxA[:, 1] = bboxA[:, 1] + h * 0.5 - max_side * 0.5
    bboxA[:, 2] = bboxA[:, 0] + max_side - 1
    bboxA[:, 3] = bboxA[:, 1] + max_side - 1
    return bboxA


  def pad(self, boxesA, w, h):
    """No idea."""
    boxes = boxesA.copy()  # shit, value parameter!!!

    tmpw = boxes[:, 2] - boxes[:, 0] + 1
    tmph = boxes[:, 3] - boxes[:, 1] + 1
    n_boxes = boxes.shape[0]

    tmpw = tmpw.astype(numpy.int32)
    tmph = tmph.astype(numpy.int32)

    dx = numpy.zeros(n_boxes, numpy.int32)
    dy = numpy.zeros(n_boxes, numpy.int32)
    edx = tmpw - 1
    edy = tmph - 1

    x = (boxes[:, 0]).astype(numpy.int32)
    y = (boxes[:, 1]).astype(numpy.int32)
    ex = (boxes[:, 2]).astype(numpy.int32)
    ey = (boxes[:, 3]).astype(numpy.int32)

    tmp = numpy.where(ex > w - 1)[0]
    if tmp.shape[0] != 0:
      edx[tmp] = -ex[tmp] + w - 1 + tmpw[tmp] - 1
      ex[tmp] = w - 1

    tmp = numpy.where(ey > h - 1)[0]
    if tmp.shape[0] != 0:
      edy[tmp] = -ey[tmp] + h - 1 + tmph[tmp] - 1
      ey[tmp] = h - 1

    tmp = numpy.where(x < 0)[0]
    if tmp.shape[0] != 0:
      dx[tmp] = -x[tmp]
      x[tmp] = 0  # numpy.zeros_like(x[tmp])

    tmp = numpy.where(y < 0)[0]
    if tmp.shape[0] != 0:
      dy[tmp] = - y[tmp]
      y[tmp] = 0  # numpy.zeros_like(y[tmp])

    ##########
    # added by zhaoyafei
    # when doing 5 points patch regression
    # for 5 points patch regression, x might exceed right-side
    tmp = numpy.where(x > w - 1)[0]
    if tmp.shape[0] != 0:
      dx[tmp] = tmpw[tmp] - 1
      edx[tmp] = tmpw[tmp] - 2
      x[tmp] = w - 1
      ex[tmp] = w - 2

    # for 5 points patch regression, y might exceed bottom-side
    tmp = numpy.where(y > h - 1)[0]
    if tmp.shape[0] != 0:
      dy[tmp] = tmph[tmp] - 1
      edy[tmp] = tmph[tmp] - 2
      y[tmp] = h - 1  # numpy.zeros_like(y[tmp])
      ey[tmp] = h - 2

    # for 5 points patch regression, ex might exceed left-side
    tmp = numpy.where(ex < 0)[0]
    if tmp.shape[0] != 0:
      dx[tmp] = 1
      edx[tmp] = 0
      x[tmp] = 1
      ex[tmp] = 0

    # for 5 points patch regression, ey might exceed top-side
    tmp = numpy.where(ey < 0)[0]
    if tmp.shape[0] != 0:
      dy[tmp] = 1
      edy[tmp] = 0
      y[tmp] = 1
      ey[tmp] = 0
    ##########

    return dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph
