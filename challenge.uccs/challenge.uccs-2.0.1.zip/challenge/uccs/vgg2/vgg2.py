import numpy
import cv2

# avoid logging of caffe networks to console
import os
os.environ['GLOG_minloglevel'] = '2'
import caffe

class VGGFace2:

  def __init__(self, gpu_id=0, model_path="./model"):
    # set Caffe mode
    if gpu_id is not None:
      caffe.set_device(gpu_id)
      caffe.set_mode_gpu()
    else:
      caffe.set_mode_cpu()

    self.net = caffe.Net(os.path.join(model_path,"senet50_ft.prototxt"), os.path.join(model_path,"senet50_ft.caffemodel"), caffe.TEST)
    self.mean = numpy.array([91.4953, 103.8827, 131.0912]) # BGR order
    self.min_scale_ratio = 224./256.


  def center_crop(self, image, bbox, extension_rate=1.3):
    """Extending the bounding box with extension rate, scaling to 256x256, and return the center crop.
      :argument image is the raw image
      :argument bbox is a bounding box (either from MTCNN or the original IJB-B bounding box)
      :argument extension_rate is a scalar to increase width and height

      :returns a crop
      ideally, crop's width equal bounding box width * extension_rate
      similarly, crop's height equal bounding box height * extension_rate
      ideally, as we can hit the edges of full_image
      Also, we aim to maintain a minimum scale ration (min_scale_ratio).. the edges might have an influence on that
    """

    ### first, crop out the required region
    height, width, channels = image.shape

    bb_width = int(round(bbox[2] - bbox[0]))
    bb_height = int(round(bbox[3] - bbox[1]))
    bb_scale_ratio = float(min(bb_width, bb_height)) / max(bb_width, bb_height)

    # Provisional width and height
    prov_bb_width = int(numpy.ceil(bb_width * extension_rate))
    prov_bb_height = int(numpy.ceil(bb_height * extension_rate))

    if bb_scale_ratio < self.min_scale_ratio:
      # to have the targeted scale-ratio. we round up with np.ceil
      if bb_width < bb_height:
        prov_bb_width = int(numpy.ceil(prov_bb_height * self.min_scale_ratio))
      elif bb_width > bb_height:
        prov_bb_height = int(numpy.ceil(prov_bb_width * self.min_scale_ratio))

    # Provisional x, y coordinates of top-left corner of extended bounding box
    prov_x_tl = int(round(max(0.0, bbox[0] - (prov_bb_width - bb_width) * 0.5)))
    prov_y_tl = int(round(max(0.0, bbox[1] - (prov_bb_height - bb_height) * 0.5)))
    # Provisional x, y coordinates of bottom-right corner of extended bounding box
    prov_x_br = int(round(min(width, bbox[2] + (prov_bb_width - bb_width) * 0.5)))
    prov_y_br = int(round(min(height, bbox[3] + (prov_bb_height - bb_height) * 0.5)))

    x_y_coordinates = (prov_x_tl, prov_y_tl, prov_x_br, prov_y_br)
    crop = image[prov_y_tl:prov_y_br, prov_x_tl:prov_x_br]

    ### now, scale the image and compute the center crop
    h, w, c = crop.shape
    shorter_side = min(h, w)
    # scale image to 256x256 pixels
    scaler = 256. / shorter_side
    scaled_crop = cv2.resize(crop, (0,0), fx=scaler, fy=scaler)
    # compute center crop coordinates
    h, w, c = scaled_crop.shape
    x_tl = int(round((w-224)/2.))
    y_tl = int(round((h-224)/2.))
    x_br = x_tl + 224
    y_br = y_tl + 224

    # crop the face
    coordinates = (x_tl, y_tl, x_br, y_br)
    return scaled_crop[y_tl:y_br, x_tl:x_br]


  def get_face_descriptor(self, image, bbox, normalize=True, layer='pool5/7x7_s1'):
    crop = self.center_crop(image, bbox)
    # preprocess image
    crop = numpy.transpose(crop.astype(numpy.float32) - self.mean, (2, 0, 1))

    # extract feature
    data_shape = self.net.blobs['data'].data.shape
    data = numpy.array([crop]).reshape(data_shape)
    self.net.forward(data=data)
    feature = numpy.array(self.net.blobs[layer].data).flatten()

    # return normalized feature
    if normalize:
      feature = feature / numpy.linalg.norm(feature)
    return feature, crop
