"""
Author: qiacai
"""


from ada_core.algorithms import algorithm_meta
from ada_core import exceptions


class AlgorithmFactory(object):

    _cls_name_list = algorithm_meta.__all__

    #@classmethod
    def getAlgorithmMeta(self, alg_name, input_type):

        alg_meta_class = None

        for cls_name in AlgorithmFactory._cls_name_list:

            cls_class = algorithm_meta.__dict__.get(cls_name)
            if cls_class.alg_name == alg_name and isinstance(cls_class.input_value, input_type):
                alg_meta_class = cls_class
                break
            else:
                continue

        if alg_meta_class is None:
            raise exceptions.ParametersNotPassed('Could not find algorithm meta class based on name and input_type')

        return alg_meta_class

        #@classmethod
    def getAlgorithmMetaList(self, alg_name):

        meta_class_list = []

        for cls_name in AlgorithmFactory._cls_name_list:

            cls_class = algorithm_meta.__dict__.get(cls_name)
            if cls_class.alg_name == alg_name:
                meta_class_list.append(cls_class)
            else:
                continue

        if not meta_class_list:
            raise exceptions.ParametersNotPassed('Could not find algorithm meta class based on name')

        return meta_class_list

    #@classmethod
    def getAlgorithm(self, alg_name, input_type):

        alg_cls = None

        for cls_name in AlgorithmFactory._cls_name_list:

            cls_class = algorithm_meta.__dict__.get(cls_name)
            if cls_class.alg_name == alg_name and isinstance(cls_class.input_value, input_type):
                alg_cls = cls_class.alg_cls
                break
            else:
                continue

        if alg_cls is None:
            raise exceptions.ParametersNotPassed('Could not find algorithm class based on name and input_type')

        # for alg in AlgorithmFactory._alg_obj_list:
        #     if type(alg) is alg_cls:
        #         return alg
        #     else:
        #         continue

        alg_obj = alg_cls()
        # AlgorithmFactory._alg_obj_list.append(alg_obj)

        return alg_obj

    #@classmethod
    def getAlgorithmOutputType(self, alg_name, input_type):

        alg_output_value = None

        for cls_name in AlgorithmFactory._cls_name_list:

            cls_class = algorithm_meta.__dict__.get(cls_name)
            if cls_class.alg_name == alg_name and isinstance(cls_class.input_value,input_type):
                alg_output_value = cls_class.output_value
                break
            else:
                continue

        if alg_output_value is None:
            raise exceptions.ParametersNotPassed('Could not find algorithm meta class based on name and input_type')

        return type(alg_output_value)