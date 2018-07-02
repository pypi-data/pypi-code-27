# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.

from django.dispatch import Signal

get_visibility_errors = Signal(providing_args=["shop_product", "customer"], use_caching=True)
get_orderability_errors = Signal(providing_args=["shop_product", "customer", "supplier", "quantity"], use_caching=True)
shipment_created = Signal(providing_args=["order", "shipment"], use_caching=True)
shipment_created_and_processed = Signal(providing_args=["order", "shipment"], use_caching=True)
refund_created = Signal(providing_args=["order", "refund_lines"], use_caching=True)
category_deleted = Signal(providing_args=["category"], use_caching=True)
shipment_deleted = Signal(providing_args=["shipment"], use_caching=True)
payment_created = Signal(providing_args=["order", "payment"], use_caching=True)
get_basket_command_handler = Signal(providing_args=["command"], use_caching=True)
pre_clean = Signal(providing_args=["instance"], use_caching=True)
post_clean = Signal(providing_args=["instance"], use_caching=True)
