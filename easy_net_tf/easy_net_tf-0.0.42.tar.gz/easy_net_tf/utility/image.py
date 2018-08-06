import cv2
import numpy

from pathlib import Path


class UtilityImage:
    NORMALIZE_DEFAULT = 'default'
    NORMALIZE_EACH_CHANNEL = 'normalize each channel to [low,high]'
    NORMALIZE_ALL_CHANNEL = 'normalize all channel to [low,high]'

    @staticmethod
    def normalize(image,
                  low,
                  high,
                  mode=NORMALIZE_DEFAULT):
        """
        
        :param image:
        :param low: 
        :param high: 
        :param mode: 
        :return: 
        """
        copy = numpy.copy(image)

        if mode == UtilityImage.NORMALIZE_DEFAULT:
            copy = (copy - 127.5) / 128

        # normalize each channel separately to [-1, 1]
        elif mode == UtilityImage.NORMALIZE_EACH_CHANNEL:
            height, width, channels = copy.shape
            for channel in range(channels):
                maximum = numpy.max(copy[:, :, channel])
                minimum = numpy.min(copy[:, :, channel])
                copy[:, :, channel] = (
                                              (copy[:, :, channel] - minimum) / (
                                          numpy.clip(a=maximum - minimum, a_min=1e-10, a_max=None))
                                      ) * (high - low) + low

        # normalize all channels together to [-1, 1]
        elif mode == UtilityImage.NORMALIZE_ALL_CHANNEL:
            maximum = numpy.max(copy)
            minimum = numpy.min(copy)
            copy = ((copy - minimum) / (numpy.clip(a=maximum - minimum, a_min=1e-10, a_max=None))
                    ) * (high - low) + low

        return copy

    @staticmethod
    def resize(image, scale):
        copy = numpy.copy(image)

        height, width, _ = copy.shape
        new_height = int(height * scale)
        new_width = int(width * scale)

        copy = cv2.resize(copy,
                          (new_width, new_height),
                          interpolation=cv2.INTER_LINEAR)
        return copy

    @staticmethod
    def rotate(image, center, angle):
        """

        :param image:
        :param center: rotation center (x, y)
        :param angle:
        :return:
        """

        copy = numpy.copy(image)

        rotate_mat = cv2.getRotationMatrix2D(center, angle, 1)
        copy = cv2.warpAffine(copy, rotate_mat, (copy.shape[1], copy.shape[0]))

        return copy

    @staticmethod
    def horizontally_flip(image):
        """

        :param image:
        :return:
        """

        """
        image flip
        """
        if image is None:
            print('Error: '
                  '[UtilityImage.horizontally_flip] '
                  'image_in cant be None')
            return

        copy = numpy.copy(image)
        copy = cv2.flip(copy, 1)

        return copy

    @staticmethod
    def vertical_flip(image, landmark_in):
        if image is None:
            return None, None
        copy = numpy.copy(image)
        copy = cv2.flip(copy, 0)

        for i in range(numpy.size(landmark_in)):
            if i % 2 == 1:
                # vertical flip
                landmark_in[i] = 1.0 - landmark_in[i]

        return copy, landmark_in

    @staticmethod
    def draw_rectangle(image, boxes, color):
        """
        draw bounding boxes on image
        :param image:
        :param boxes: [x1, y1, x2, y2]
        :param color: (B, G, R)
        :return:
        """
        height, width, _ = image.shape

        boxes = numpy.reshape(boxes, [-1, 4])
        for box in boxes:
            x_1 = int(numpy.maximum(box[0], 0))
            y_1 = int(numpy.maximum(box[1], 0))
            x_2 = int(numpy.minimum(box[2], width - 1))
            y_2 = int(numpy.minimum(box[3], height - 1))

            cv2.rectangle(image,
                          (x_1, y_1),
                          (x_2, y_2),
                          color,
                          2)

        return image

    @staticmethod
    def draw_points(image, landmarks, color):
        """
        draw landmarks on image
        :param image:
        :param landmarks: shape:[None, 2]
        :param color:
        :return:
        """

        for x, y in landmarks:
            cv2.circle(img=image,
                       center=(x, y),
                       radius=2,
                       color=color,
                       thickness=-1)

        return image

    @staticmethod
    def add_coordinate(batch_image,
                       add_r,
                       normalize,
                       debug=False):
        """

        :param batch_image: a batch of images
        :param add_r: r coordinate=sqrt((x-width/2)^2+(y-height/2)^2)
        :param normalize:
        :param debug:
        :return:
        """

        """
        prepare
        """
        image_out = numpy.copy(batch_image)
        batch, height, width, channels = numpy.shape(image_out)

        """
        x coordinate
        """
        x_ones = numpy.ones(
            [batch, height],
            dtype=numpy.int32
        )

        x_ones = numpy.expand_dims(x_ones, -1)

        x_range = numpy.tile(
            numpy.expand_dims(
                numpy.arange(width),
                0
            ),
            [batch, 1]
        )

        x_range = numpy.expand_dims(x_range, 1)
        x_channel = numpy.matmul(x_ones, x_range)
        x_channel = numpy.expand_dims(x_channel, -1)

        """
        y coordinate
        """
        y_ones = numpy.ones(
            [batch, width],
            dtype=numpy.int32
        )
        y_ones = numpy.expand_dims(y_ones, 1)
        y_range = numpy.tile(
            numpy.expand_dims(
                numpy.arange(height),
                0
            ),
            [batch, 1]
        )
        y_range = numpy.expand_dims(y_range, -1)
        y_channel = numpy.matmul(y_range, y_ones)
        y_channel = numpy.expand_dims(y_channel, -1)

        """
        r coordinate
        """
        r_channel = numpy.sqrt(
            numpy.square(x_channel - (width - 1) / 2.0)
            + numpy.square(y_channel - (height - 1) / 2.0)
        )

        """
        normalize
        """
        if normalize:
            x_channel = x_channel / (width - 1.0) * 2.0 - 1.0
            y_channel = y_channel / (height - 1.0) * 2.0 - 1.0

            maximum = numpy.max(r_channel)
            minimum = numpy.min(r_channel)
            r_channel = ((r_channel - minimum) / (maximum - minimum)) * 2.0 - 1.0

        """
        concatenate
        """
        image_out = numpy.concatenate(
            (image_out, x_channel, y_channel),
            axis=-1
        )
        if add_r:
            if debug:
                print('Log: '
                      '[%s.%s] '
                      'add r coordinate.' % (UtilityImage.__name__,
                                             UtilityImage.add_coordinate.__name__))
            image_out = numpy.concatenate(
                (image_out, r_channel),
                axis=-1
            )

        return image_out

    VALID = 'VALID'
    SAME = 'SAME'

    @staticmethod
    def cut_out_rectangle(image,
                          rectangle,
                          size_out=None,
                          padding=VALID):
        """

        :param image:
        :param rectangle: [x1, y1, x2, y2]
        :param size_out: resize size
        :param padding: 'VALID': output valid image area; 'SAME': padding '0' if rectangle exceeds image
        :return:
        """

        image_copy = numpy.copy(image)
        rectangle = numpy.round(rectangle)

        if padding == UtilityImage.VALID:
            image_out = image_copy[int(rectangle[1]):int(rectangle[3] + 1),
                        int(rectangle[0]):int(rectangle[2] + 1), :]

        elif padding == UtilityImage.SAME:
            height, width, channels = image_copy.shape

            x_1 = rectangle[0]
            y_1 = rectangle[1]
            x_2 = rectangle[2]
            y_2 = rectangle[3]

            m_height = y_2 - y_1 + 1
            m_width = x_2 - x_1 + 1

            if x_1 < 0:
                m_x_1 = -x_1
                x_1 = 0
            else:
                m_x_1 = 0

            if y_1 < 0:
                m_y_1 = -y_1
                y_1 = 0
            else:
                m_y_1 = 0

            if x_2 >= width:
                m_x_2 = m_width - 1 - (x_2 - (width - 1))
                x_2 = width - 1
            else:
                m_x_2 = m_width - 1

            if y_2 >= height:
                m_y_2 = m_height - 1 - (y_2 - (height - 1))
                y_2 = height - 1
            else:
                m_y_2 = m_height - 1

            # generate crop size mask
            image_out = numpy.zeros(shape=(m_height, m_width, channels))
            image_out[m_y_1:m_y_2 + 1, m_x_1:m_x_2 + 1, :] = image_copy[y_1:y_2 + 1, x_1:x_2 + 1, :]

        else:
            print('Error: '
                  '[%s.%s] '
                  'padding should be ''VALID'' or ''SAME''' % (UtilityImage.__name__,
                                                               UtilityImage.cut_out_rectangle.__name__))
            image_out = None

        if image_out is None:
            return
        elif size_out is not None \
                and size_out > 0:
            image_out = cv2.resize(image_out,
                                   (size_out, size_out),
                                   interpolation=cv2.INTER_LINEAR)
            return image_out

    @staticmethod
    def cut_out_rectangles(image,
                           rectangles,
                           size_out):
        """
        1.repair exceeding boxes to valid boxes, padding '0' in exceeding area
        2.resize to net input size;
        :param image:
        :param rectangles:
        :param size_out: resize size
        :return: a batch of resize cropped image
        """

        copy = numpy.copy(image)

        image_height, image_width, channels = copy.shape
        rectangles = numpy.around(rectangles).astype(numpy.int32)
        boxes_number = rectangles.shape[0]

        boxes_x_1 = rectangles[:, 0]
        boxes_y_1 = rectangles[:, 1]
        boxes_x_2 = rectangles[:, 2]
        boxes_y_2 = rectangles[:, 3]

        boxes_width = boxes_x_2 - boxes_x_1 + 1
        boxes_height = boxes_y_2 - boxes_y_1 + 1

        c_x_1 = numpy.zeros((rectangles.shape[0],), numpy.int32)
        c_y_1 = numpy.zeros((rectangles.shape[0],), numpy.int32)
        c_x_2 = boxes_width.copy() - 1
        c_y_2 = boxes_height.copy() - 1

        index = numpy.where(numpy.greater(boxes_x_2, image_width - 1))[0]
        if numpy.size(index) > 0:
            c_x_2[index] = (boxes_width[index] - 1) - (boxes_x_2[index] - (image_width - 1))
            boxes_x_2[index] = image_width - 1

        index = numpy.where(boxes_y_2 > image_height - 1)
        if numpy.size(index) > 0:
            c_y_2[index] = (boxes_height[index] - 1) - (boxes_y_2[index] - (image_height - 1))
            boxes_y_2[index] = image_height - 1

        index = numpy.where(boxes_x_1 < 0)
        if numpy.size(index) > 0:
            c_x_1[index] = 0 - boxes_x_1[index]
            boxes_x_1[index] = 0

        index = numpy.where(boxes_y_1 < 0)
        if numpy.size(index) > 0:
            c_y_1[index] = 0 - boxes_y_1[index]
            boxes_y_1[index] = 0

        images_out = numpy.zeros((boxes_number,
                                  size_out,
                                  size_out,
                                  channels),
                                 dtype=numpy.float32)

        for i in range(boxes_number):
            container = numpy.zeros((boxes_height[i],
                                     boxes_width[i],
                                     channels),
                                    dtype=numpy.float32)
            container[c_y_1[i]:c_y_2[i] + 1, c_x_1[i]:c_x_2[i] + 1, :] = copy[boxes_y_1[i]:boxes_y_2[i] + 1,
                                                                         boxes_x_1[i]:boxes_x_2[i] + 1, :]
            images_out[i, :, :, :] = cv2.resize(container, (size_out, size_out))

        return images_out

    @staticmethod
    def save_image(image,
                   category,
                   save_dir,
                   index,
                   stride,
                   rotation=None,
                   landmarks=None,
                   offsets=None):
        """

        :param image:
        :param category: a list(negative:0, positive:1, partial:-1, landmark:-2).
        :param save_dir: directory of saving specific category
        :param index: image index
        :param stride: [images save stride, label save stride]
        :param rotation:
        :param landmarks:
        :param offsets:
        :return:
        """
        assert image is not None, 'Error: [%s,%s] image can not be None' % (UtilityImage.__name__,
                                                                            UtilityImage.save_image.__name__)

        """
        save image
        """
        image_folder = Path('%d' % int(index / stride[0]))
        image_name = '%d.jpg' % index

        image_path = save_dir / 'image' / image_folder / image_name
        image_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(filename=image_path.__str__(), img=image)

        """
        save labels
        """
        label = ';' + ' '.join(map(str, category))

        if rotation is not None:
            label += ';' + ' '.join(map(str, rotation))

        if offsets is not None:
            label += ';' + ' '.join(map(str, offsets))

        if landmarks is not None:
            label += ';' + ' '.join(map(str, landmarks))

        filename = 'labels-%d' % int(index / stride[1])
        file_path = save_dir / 'label' / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        content = (image_folder / image_name).__str__() + label + '\n'

        with file_path.open('a') as file:
            file.write(content)

        return True


if __name__ == '__main__':
    img = numpy.array([1, 2, 3])
    UtilityImage.save_image(image=img,
                            category=[0, 2],
                            save_dir=Path(''),
                            index=100,
                            stride=[100, 100],
                            rotation=[19],
                            landmarks=[0, 1, 4, 7.0, 8.9],
                            offsets=[0.54, 0.89, 0.13])
