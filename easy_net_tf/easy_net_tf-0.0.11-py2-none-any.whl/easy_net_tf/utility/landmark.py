import numpy


class UtilityLandmark:

    @staticmethod
    def normalize(batch_rectangle, landmark):
        """

        :param batch_rectangle: [batch, 4]
        :param landmark: [2n]
        :return: narry [batch, 2n]
        """

        """
        prepare
        """
        batch, _ = numpy.shape(batch_rectangle)

        landmark = numpy.reshape(landmark, [-1, 2])
        n_landmark = list()

        """
        normalize landmark
        """
        for rectangle in batch_rectangle:
            for x, y in landmark:
                n_landmark.append(
                    (x - rectangle[0]) / (rectangle[2] - rectangle[0] + 1)
                )

                n_landmark.append(
                    (y - rectangle[1]) / (rectangle[3] - rectangle[1] + 1)
                )

        """
        reshape
        """
        n_landmark = numpy.reshape(
            numpy.array(
                n_landmark,
                dtype=numpy.float32
            ),
            [batch, -1]
        )

        return n_landmark

    @staticmethod
    def regress(batch_box, batch_landmark):
        """
        calibrate landmarks to real scale
        :param batch_box: [batch, 4]
        :param batch_landmark: [batch, 10]
        :return:
        """
        boxes_height = batch_box[:, 2] - batch_box[:, 0] + 1
        boxes_width = batch_box[:, 3] - batch_box[:, 1] + 1

        batch_landmark[:, 0] = batch_landmark[:, 0] * boxes_width + batch_box[:, 0]
        batch_landmark[:, 1] = batch_landmark[:, 1] * boxes_height + batch_box[:, 1]

        batch_landmark[:, 2] = batch_landmark[:, 2] * boxes_width + batch_box[:, 0]
        batch_landmark[:, 3] = batch_landmark[:, 3] * boxes_height + batch_box[:, 1]

        batch_landmark[:, 4] = batch_landmark[:, 4] * boxes_width + batch_box[:, 0]
        batch_landmark[:, 5] = batch_landmark[:, 5] * boxes_height + batch_box[:, 1]

        batch_landmark[:, 6] = batch_landmark[:, 6] * boxes_width + batch_box[:, 0]
        batch_landmark[:, 7] = batch_landmark[:, 7] * boxes_height + batch_box[:, 1]

        batch_landmark[:, 8] = batch_landmark[:, 8] * boxes_width + batch_box[:, 0]
        batch_landmark[:, 9] = batch_landmark[:, 9] * boxes_height + batch_box[:, 1]

        return batch_landmark

    @staticmethod
    def align_face(image, landmarks, template):
        image_height, image_width, _ = image.shape

        landmarks = numpy.reshape(landmarks, [-1, 2])
        template = numpy.reshape(template, [-1, 2])

        # maybe it is unnecessary, wait for proving!!!
        for index, _ in enumerate(landmarks):
            landmarks[index][0] *= image_width
            landmarks[index][1] *= image_height

            template[index][0] *= image_width
            template[index][1] *= image_height

        mat = cv2.estimateRigidTransform(src=landmarks,
                                         dst=template,
                                         fullAffine=True)

        align_image = cv2.warpAffine(src=image,
                                     M=mat,
                                     dsize=(image_height, image_width))

        return align_image
