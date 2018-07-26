#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cerberus
from . import _core_validators


# -----------------------------
# for dataset.
# -----------------------------
def dataset_schema():
    schema = _core_validators.dataset_schema()
    schema.update(
        dict(
            title=dict(
                type='string',
                required=False,
                empty=True
            )
        )
    )
    return schema


def validate_dataset(dataset):
    v = _core_validators.DatasetValidator(dataset_schema())
    if not v.validate(
            dict(
                factories=dataset.factories,
                extra_args=dataset.extra_args,
                title=dataset.title
            )
    ):
        raise _core_validators.ValidationError('dataset {}'.format(v.errors))


# -----------------------------
# for datasets.
# -----------------------------
def validate_datasets(datasets):
    _core_validators.validate_datasets(datasets)


# -----------------------------
# for dataset_sizes.
# -----------------------------
def validate_dataset_sizes(dataset_sizes):
    _core_validators.validate_dataset_sizes(dataset_sizes)


# -----------------------------
# for kernel.
# -----------------------------
def kernel_schema():
    schema = _core_validators.kernel_schema()
    schema.update(
        dict(
            label=dict(
                type='string',
                required=False,
                empty=True
            )
        )
    )
    return schema


def validate_kernel(kernel):
    v = _core_validators.KernelValidator(kernel_schema())
    if not v.validate(
            dict(
                stmt=kernel.stmt,
                setup=kernel.setup,
                label=kernel.label
            )
    ):
        raise _core_validators.ValidationError('kernel {}'.format(v.errors))


# -----------------------------
# for kernels.
# -----------------------------
def validate_kernels(kernels):
    _core_validators.validate_kernels(kernels)


# -----------------------------
# for layout_size.
# -----------------------------
def layout_size_schema():
    return dict(
        width=dict(
            type='integer',
            required=False,
            nullable=True,
            min=0
        ),
        height=dict(
            type='integer',
            required=False,
            nullable=True,
            min=0
        ),
        label=dict(
            type='string',
            required=False,
            empty=True
        )
    )


def validate_layout_size(layout_size):
    v = cerberus.Validator(layout_size_schema())
    if not v.validate(
            dict(
                width=layout_size.width,
                height=layout_size.height,
                label=layout_size.label
            )
    ):
        raise _core_validators.ValidationError('layout_size {}'.format(v.errors))


# -----------------------------
# for layout_sizes.
# -----------------------------
class LayoutSizesValidator(cerberus.Validator):
    def _validate_type_LayoutSize(self, value):
        from . import bench
        return isinstance(value, bench.LayoutSize)


def layout_sizes_schema():
    return dict(
        a_list=dict(
            type='list',
            schema=dict(
                type='LayoutSize',
            )
        )
    )


def validate_layout_sizes(layout_sizes):
    v = LayoutSizesValidator(layout_sizes_schema())
    if not v.validate(dict(a_list=layout_sizes)):
        raise _core_validators.ValidationError('layout_sizes {}'.format(v.errors))

    v = cerberus.Validator(layout_size_schema())
    for i, layout_size in enumerate(layout_sizes):
        if not v.validate(
                dict(
                    width=layout_size.width,
                    height=layout_size.height,
                    label=layout_size.label,
                )
        ):
            raise _core_validators.ValidationError('layout_sizes[{}] {}'.format(i, v.errors))


# -----------------------------
# for Benchmark.
# -----------------------------
def validate(
        datasets,
        dataset_sizes,
        kernels,
        repeat,
        number,
        layout_sizes
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

    if layout_sizes is not None:
        validate_layout_sizes(layout_sizes)
