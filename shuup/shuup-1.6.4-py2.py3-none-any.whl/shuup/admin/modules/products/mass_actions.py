# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import unicodecsv as csv
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from six import string_types

from shuup.admin.modules.products.views.list import ProductListView
from shuup.admin.modules.settings.view_settings import ViewSettings
from shuup.admin.utils.picotable import (
    PicotableFileMassAction, PicotableMassAction, PicotableRedirectMassAction
)
from shuup.core.models import ShopProduct, ShopProductVisibility


class VisibleMassAction(PicotableMassAction):
    label = _("Set visible")
    identifier = "mass_action_product_visible"

    def process(self, request, ids):
        query = Q(product__pk__in=ids)
        if isinstance(ids, string_types) and ids == "all":
            query = Q()
        ShopProduct.objects.filter(query).update(visibility=ShopProductVisibility.ALWAYS_VISIBLE)


class InvisibleMassAction(PicotableMassAction):
    label = _("Set invisible")
    identifier = "mass_action_product_invisible"

    def process(self, request, ids):
        query = Q(product__pk__in=ids)
        if isinstance(ids, string_types) and ids == "all":
            query = Q()
        ShopProduct.objects.filter(query).update(visibility=ShopProductVisibility.NOT_VISIBLE)


class FileResponseAction(PicotableFileMassAction):
    label = _("Export CSV")
    identifier = "mass_action_product_simple_csv"

    def process(self, request, ids):
        query = Q(id__in=ids)
        if isinstance(ids, string_types) and ids == "all":
            query = Q()
        view_settings = ViewSettings(ShopProduct, ProductListView.default_columns, ProductListView)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response, delimiter=";", encoding='utf-8')
        writer.writerow([col.title for col in view_settings.columns])
        for shop_product in ShopProduct.objects.filter(query):
            row = []
            for dr in [col.id for col in view_settings.columns]:
                if dr.startswith("shopproduct_"):
                    row.append(getattr(shop_product, dr.replace("shopproduct_", "")))
                elif dr.startswith("product_"):
                    row.append(getattr(shop_product.product, dr.replace("product_", "")))
                else:
                    row.append(getattr(shop_product.product, dr))
            writer.writerow(row)
        return response


class EditProductAttributesAction(PicotableRedirectMassAction):
    label = _("Edit products")
    identifier = "mass_action_edit_product"
    redirect_url = reverse("shuup_admin:shop_product.mass_edit")
