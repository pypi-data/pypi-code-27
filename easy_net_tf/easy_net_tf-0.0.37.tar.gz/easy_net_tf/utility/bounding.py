import numpy

from easy_net_tf.utility.file import UtilityFile


class UtilityBounding:
    CIRCLE = 'circle'
    RECTANGLE = 'rectangle'

    @staticmethod
    def rectangle_2_circle(r_file_path,
                           s_filename,
                           debug=False):
        """

        :param r_file_path:
        :param s_filename:
        :param debug:
        :return:
        """
        info_generator = UtilityFile.line_generator(r_file_path)
        s_file_path = r_file_path.parent / s_filename

        sample_index = 0
        with s_file_path.open('w') as file:
            while True:
                if debug:
                    sample_index += 1
                    print('Log: '
                          '[%s.%s] '
                          'sample: %d' % (UtilityBounding.__name__,
                                          UtilityBounding.rectangle_2_circle.__name__,
                                          sample_index)
                          )
                try:
                    """
                    get info
                    """
                    info = info_generator.__next__().strip().split(' ')

                    image_path = info.pop(0)

                    box_list = numpy.reshape(
                        numpy.array(info, dtype=numpy.float32),
                        [-1, 4]
                    )

                    """
                    convert to circle
                    """
                    circle_list = list()
                    for box in box_list:
                        center_x = (box[0] + box[2]) / 2
                        center_y = (box[1] + box[3]) / 2
                        radius = numpy.sqrt(
                            numpy.square(box[0] - box[2])
                            + numpy.square(box[1] - box[3])
                        ) / 2

                        circle = [center_x, center_y, radius]
                        circle_list.append(circle)

                    """
                    save to file
                    """
                    circles = numpy.reshape(
                        numpy.array(circle_list),
                        [-1]
                    )

                    new_info = image_path + ' ' + ' '.join(map(str, circles)) + '\n'
                    file.write(new_info)

                except StopIteration:
                    break

    @staticmethod
    def rectangle_2_square(rectangles,
                           image_width,
                           image_height):
        """
        convert boxes to square shape with avoiding exceeding original image by move bounding towards image
        :param rectangles:
        :param image_width:
        :param image_height:
        :return:
        """

        if rectangles is None:
            return None

        squares = numpy.copy(rectangles)

        boxes_height = rectangles[:, 3] - rectangles[:, 1] + 1
        boxes_width = rectangles[:, 2] - rectangles[:, 0] + 1

        long_side = numpy.maximum(boxes_height, boxes_width)

        squares[:, 0] = rectangles[:, 0] + 0.5 * boxes_width - 0.5 * long_side
        squares[:, 1] = rectangles[:, 1] + 0.5 * boxes_height - 0.5 * long_side

        squares[:, 2] = squares[:, 0] + long_side - 1
        squares[:, 3] = squares[:, 1] + long_side - 1

        invalid_indexes = numpy.less(squares[:, 0], 0)
        squares[:, 2] = numpy.where(invalid_indexes,
                                    squares[:, 2] - squares[:, 0],
                                    squares[:, 2])
        squares[:, 0] = numpy.where(invalid_indexes,
                                    0,
                                    squares[:, 0])

        invalid_indexes = numpy.less(squares[:, 1], 0)
        squares[:, 3] = numpy.where(invalid_indexes,
                                    squares[:, 3] - squares[:, 1],
                                    squares[:, 3])
        squares[:, 1] = numpy.where(invalid_indexes,
                                    0,
                                    squares[:, 1])

        invalid_indexes = numpy.greater_equal(squares[:, 2], image_width)
        squares[:, 0] = numpy.where(invalid_indexes,
                                    squares[:, 0] - (squares[:, 2] - image_width + 1),
                                    squares[:, 0])
        squares[:, 2] = numpy.where(invalid_indexes,
                                    image_width - 1,
                                    squares[:, 2])

        invalid_indexes = numpy.greater_equal(squares[:, 3], image_height)
        squares[:, 1] = numpy.where(invalid_indexes,
                                    squares[:, 1] - (squares[:, 3] - image_height + 1),
                                    squares[:, 1])
        squares[:, 3] = numpy.where(invalid_indexes,
                                    image_height - 1,
                                    squares[:, 3])

        return squares

    @staticmethod
    def rectangle_offset_horizontally_flip(offset):
        """

        :param offset:[x1, y1, x2, y2]
        :return:
        """

        copy = offset.copy()
        copy[0], copy[2] = -copy[2], -copy[0]

        return copy

    @staticmethod
    def iou_circle(circle,
                   circles):
        """
        calculate Intersection on Union of box against to each of boxes
        :param circle:
        :param circles:
        :return: intersection on union
        """

        # prepare
        circles = numpy.reshape(circles, [-1, 3])
        pi = 3.1415926
        iou_list = list()

        # get distance between circles
        distances = numpy.sqrt(
            numpy.square(circles[:, 0] - circle[0])
            + numpy.square(circles[:, 1] - circle[1])
        )

        for index, circle_2 in enumerate(circles):

            if circle_2[2] + circle[2] <= distances[index]:
                """
                separate
                """
                iou_list.append(0)

            elif numpy.abs(circle_2[2] - circle[2]) >= distances[index]:
                """
                include
                """
                if circle_2[2] > circle[2]:
                    g_radius = circle_2[2]
                    l_radius = circle[2]

                else:
                    g_radius = circle[2]
                    l_radius = circle_2[2]

                iou_list.append(
                    numpy.square(l_radius) / numpy.square(g_radius)
                )

            else:
                """
                intersect
                """
                # get rhombus_area
                perimeter = distances[index] + circle[2] + circle_2[2]

                rhombus_area = 2 * numpy.sqrt(
                    (perimeter / 2)
                    * (perimeter / 2 - circle_2[2])
                    * (perimeter / 2 - circle[2])
                    * (perimeter / 2 - distances[index])
                )

                # get sector area
                height = rhombus_area / distances[index]

                sector_area_1 = numpy.arcsin(height / circle_2[2]) * numpy.square(circle_2[2])
                sector_area_2 = numpy.arcsin(height / circle[2]) * numpy.square(circle[2])

                # get intersection
                inter_area = sector_area_1 + sector_area_2 - rhombus_area

                # get union
                union_area = pi * numpy.square(circle_2[2]) + pi * numpy.square(circle[2]) - inter_area

                # get iou
                iou = inter_area / union_area

                iou_list.append(iou)

        return iou_list

    @staticmethod
    def iou_rectangle(rectangle,
                      rectangles):
        """
        calculate Intersection on Union of box against to each of boxes
        :param rectangle:
        :param rectangles:
        :return: ious, inter_area, box_area, boxes_area
        """

        rectangles = numpy.round(numpy.reshape(rectangles, [-1, 4]))

        box_area = (rectangle[2] - rectangle[0] + 1) * (rectangle[3] - rectangle[1] + 1)
        boxes_area = (rectangles[:, 2] - rectangles[:, 0] + 1) * (rectangles[:, 3] - rectangles[:, 1] + 1)

        inter_x_1 = numpy.maximum(rectangle[0], rectangles[:, 0])
        inter_y_1 = numpy.maximum(rectangle[1], rectangles[:, 1])
        inter_x_2 = numpy.minimum(rectangle[2], rectangles[:, 2])
        inter_y_2 = numpy.minimum(rectangle[3], rectangles[:, 3])

        inter_w = numpy.maximum(0, inter_x_2 - inter_x_1 + 1)
        inter_h = numpy.maximum(0, inter_y_2 - inter_y_1 + 1)

        inter_area = inter_w * inter_h
        union = box_area + boxes_area - inter_area  # + 10e-10

        ious = inter_area / union

        return ious, inter_area, box_area, boxes_area

    UNION = 'Union'
    MIN = 'Minimum'

    @staticmethod
    def nms(boxes,
            scores,
            threshold,
            mode='Union',
            is_train=True):
        """
        non maximum suppression
        :param boxes:
        :param scores:
        :param threshold:
        :param mode:
        :param is_train:
        :return: kept indexes
        """

        x_1 = boxes[:, 0]
        y_1 = boxes[:, 1]
        x_2 = boxes[:, 2]
        y_2 = boxes[:, 3]

        boxes_area = (x_2 - x_1 + 1) * (y_2 - y_1 + 1)
        increase_order_indexes = numpy.argsort(-scores, axis=0)

        kept_indexes = list()

        while numpy.size(increase_order_indexes) > 0:
            index = increase_order_indexes[0]
            other_indexes = increase_order_indexes[1:]

            kept_indexes.append(index)

            if numpy.size(other_indexes) <= 0:
                break

            if is_train is False:
                # filter [1]:
                delta_x_1 = x_1[index] - x_1[other_indexes]
                delta_y_1 = y_1[index] - y_1[other_indexes]
                delta_x_2 = x_2[index] - x_2[other_indexes]
                delta_y_2 = y_2[index] - y_2[other_indexes]

                # box in other boxes
                mask_1 = numpy.where(delta_x_1 >= 0, 1, 0)
                mask_1 *= numpy.where(delta_y_1 >= 0, 1, 0)
                mask_1 *= numpy.where(delta_x_2 <= 0, 1, 0)
                mask_1 *= numpy.where(delta_y_2 <= 0, 1, 0)

                # box contain other boxes
                mask_2 = numpy.where(delta_x_1 <= 0, 1, 0)
                mask_2 *= numpy.where(delta_y_1 <= 0, 1, 0)
                mask_2 *= numpy.where(delta_x_2 >= 0, 1, 0)
                mask_2 *= numpy.where(delta_y_2 >= 0, 1, 0)

                mask = mask_1 + mask_2

                mask_index = numpy.where(mask == 0)[0]
                if numpy.size(mask_index) <= 0:
                    break
                other_indexes = other_indexes[mask_index]

            # intersection over union
            inter_x_1 = numpy.maximum(x_1[index], x_1[other_indexes])
            inter_y_1 = numpy.maximum(y_1[index], y_1[other_indexes])
            inter_x_2 = numpy.minimum(x_2[index], x_2[other_indexes])
            inter_y_2 = numpy.minimum(y_2[index], y_2[other_indexes])

            inter_width = numpy.maximum(inter_x_2 - inter_x_1 + 1, 0.0)
            inter_height = numpy.maximum(inter_y_2 - inter_y_1 + 1, 0.0)

            inter_area = inter_width * inter_height

            if mode == UtilityBounding.UNION:
                ious = inter_area / (boxes_area[index] + boxes_area[other_indexes] - inter_area)
            elif mode == UtilityBounding.MIN:
                ious = inter_area / numpy.minimum(boxes_area[index],
                                                  boxes_area[other_indexes])
            else:
                print('Error: '
                      '[%s.%s] '
                      'mns mode can only be ''%s'' or ''%s''.' % (UtilityBounding.__name__,
                                                                  UtilityBounding.nms.__name__,
                                                                  UtilityBounding.MIN,
                                                                  UtilityBounding.UNION))
                return None

            mask_index = numpy.where(ious <= threshold)[0]
            if numpy.size(mask_index) <= 0:
                break
            increase_order_indexes = other_indexes[mask_index]

        return kept_indexes

    @staticmethod
    def regress_rectangles(rectangles, normalized_offsets):
        """
        calibrate boxes by adding offsets
        :param rectangles:
        :param normalized_offsets:
        :return:
        """
        boxes_height = rectangles[:, 2] - rectangles[:, 0] + 1
        boxes_width = rectangles[:, 3] - rectangles[:, 1] + 1

        normalized_offsets[:, 0] *= boxes_width
        normalized_offsets[:, 1] *= boxes_height
        normalized_offsets[:, 2] *= boxes_width
        normalized_offsets[:, 3] *= boxes_height

        calibrated_rectangles = rectangles + normalized_offsets

        return calibrated_rectangles


if __name__ == '__main__':
    no = [0.1, 0.2, 0.3, 0.4]

    no2 = UtilityBounding.rectangle_offset_horizontally_flip(no)

    print(no2)
