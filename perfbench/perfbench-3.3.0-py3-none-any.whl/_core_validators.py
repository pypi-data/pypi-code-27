#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import types
import cerberus


class ValidationError(Exception):
    pass


# -----------------------------
# for dataset.
# -----------------------------
class DatasetValidator(cerberus.Validator):
    def _validate_type_Function(self, value):
        return isinstance(value, types.FunctionType)


def dataset_schema():
    return dict(
        factories=dict(
            type='list',
            required=True,
            schema=dict(
                type='Function',
            )
        ),
        extra_args=dict(
            type='dict',
            required=False,
            nullable=True
        )
    )


def validate_dataset(dataset):
    v = DatasetValidator(dataset_schema())
    if not v.validate(
            dict(
                factories=dataset.factories,
                extra_args=dataset.extra_args
            )
    ):
        raise ValidationError('dataset {}'.format(v.errors))


# -----------------------------
# for datasets.
# -----------------------------
class DatasetsValidator(cerberus.Validator):
    def _validate_type_Dataset(self, value):
        from . import core
        return isinstance(value, core.Dataset)


def datasets_schema():
    return dict(
        a_list=dict(
            type='list',
            schema=dict(
                type='Dataset',
            )
        )
    )


def validate_datasets(datasets):
    v = DatasetsValidator(datasets_schema())
    if not v.validate(dict(a_list=datasets)):
        raise ValidationError('datasets {}'.format(v.errors))

    v = DatasetValidator(dataset_schema())
    for i, dataset in enumerate(datasets):
        if not v.validate(
                dict(
                    factories=dataset.factories,
                    extra_args=dataset.extra_args
                )
        ):
            raise ValidationError('datasets[{}] {}'.format(i, v.errors))


# -----------------------------
# for dataset_sizes.
# -----------------------------
def dataset_sizes_schema():
    return dict(
        a_list=dict(
            type='list',
            schema=dict(
                type='integer',
                min=1
            )
        )
    )


def validate_dataset_sizes(dataset_sizes):
    '''Validate dataset sizes.'''
    v = cerberus.Validator(dataset_sizes_schema())
    if not v.validate(dict(a_list=dataset_sizes)):
        raise ValidationError('dataset_sizes ' + str(v.errors))


# -----------------------------
# for kernel.
# -----------------------------
class KernelValidator(cerberus.Validator):
    def _validate_type_stmt(self, value):
        return isinstance(value, (str, types.FunctionType))


def kernel_schema():
    return dict(
        stmt=dict(
            type='stmt',
            required=False,
            empty=False
        ),
        setup=dict(
            type='stmt',
            required=False,
            empty=False
        )
    )


def validate_kernel(kernel):
    v = KernelValidator(kernel_schema())
    if not v.validate(
            dict(
                stmt=kernel.stmt,
                setup=kernel.setup
            )
    ):
        raise ValidationError('kernel {}'.format(v.errors))


# -----------------------------
# for kernels.
# -----------------------------
class KernelsValidator(cerberus.Validator):
    def _validate_type_Kernel(self, value):
        from . import core
        return isinstance(value, core.Kernel)


def kernels_schema():
    return dict(
        a_list=dict(
            type='list',
            schema=dict(
                type='Kernel',
            )
        )
    )


def validate_kernels(kernels):
    v = KernelsValidator(kernels_schema())
    if not v.validate(dict(a_list=kernels)):
        raise ValidationError('kernels {}'.format(v.errors))

    v = KernelValidator(kernel_schema())
    for i, kernel in enumerate(kernels):
        if not v.validate(
                dict(
                    stmt=kernel.stmt,
                    setup=kernel.setup
                )
        ):
            raise ValidationError('kernel[{}] {}'.format(i, v.errors))


# -----------------------------
# for bench.
# -----------------------------
def validate(
        datasets,
        dataset_sizes,
        kernels,
        repeat,
        number
):
    validate_datasets(datasets)
    validate_dataset_sizes(dataset_sizes)
    validate_kernels(kernels)

    for dataset in datasets:
        if (len(dataset.factories) > 1) and (len(dataset.factories) != len(kernels)):
            raise ValueError('`dataset.factories` and `kernels` must be the same length.')

    if repeat < 0:
        raise ValueError('`repeat` must be greater than or equal to 0.')

    if number < 0:
        raise ValueError('`number` must be greater than or equal to 0.')
