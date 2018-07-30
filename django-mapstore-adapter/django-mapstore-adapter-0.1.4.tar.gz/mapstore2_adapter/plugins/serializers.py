# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from __future__ import absolute_import

from ..api.models import (MapStoreData,
                          MapStoreAttribute)

from rest_framework.exceptions import APIException

import json
import base64
import logging
import traceback

logger = logging.getLogger(__name__)


class GeoNodeSerializer(object):

    @classmethod
    def update_data(cls, serializer, data):
        if data:
            _data, created = MapStoreData.objects.get_or_create(
                resource=serializer.instance)
            _data.resource = serializer.instance
            _data.blob = data
            _data.save()
            serializer.validated_data['data'] = _data

    @classmethod
    def update_attributes(cls, serializer, attributes):
        _attributes = []
        for _a in attributes:
            attribute, created = MapStoreAttribute.objects.get_or_create(
                name=_a['name'],
                resource=serializer.instance)
            attribute.resource = serializer.instance
            attribute.name = _a['name']
            attribute.type = _a['type']
            attribute.label = _a['label']
            attribute.value = base64.encodestring(_a['value'].encode('utf8'))
            attribute.save()
            _attributes.append(attribute)
        serializer.validated_data['attributes'] = _attributes

    def get_queryset(self, caller, queryset):
        allowed_map_ids = []
        for _q in queryset:
            from geonode.maps.views import (_resolve_map,
                                            _PERMISSION_MSG_VIEW)
            mapid = _q.id
            try:
                map_obj = _resolve_map(
                    caller.request,
                    str(mapid),
                    'base.view_resourcebase',
                    _PERMISSION_MSG_VIEW)
                allowed_map_ids.append(mapid)
            except:
                tb = traceback.format_exc()
                logger.error(tb)

        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(id__in=allowed_map_ids)
        return queryset

    def perform_create(self, caller, serializer):
        from geonode.maps.views import (_resolve_map,
                                        _PERMISSION_MSG_SAVE)
        try:
            if 'id' in serializer.validated_data:
                mapid = serializer.validated_data['id']
                map_obj = _resolve_map(
                    caller.request,
                    str(mapid),
                    'base.change_resourcebase',
                    _PERMISSION_MSG_SAVE)
        except:
            tb = traceback.format_exc()
            logger.error(tb)
            raise APIException(_PERMISSION_MSG_SAVE)

        if 'data' in serializer.validated_data:
            _data = serializer.validated_data.pop('data', None)
        else:
            raise APIException("Map Configuration (data) is Mandatory!")

        if 'attributes' in serializer.validated_data:
            _attributes = serializer.validated_data.pop('attributes', None)
        else:
            raise APIException("Map Metadata (attributes) are Mandatory!")

        if _attributes:
            _map_name = None
            _map_title = None
            _map_abstract = None
            for _a in _attributes:
                if _a['name'] == 'name':
                    _map_name = _a['value']
                if _a['name'] == 'title':
                    _map_title = _a['value']
                if _a['name'] == 'abstract':
                    _map_abstract = _a['value']
        else:
            raise APIException("Map Metadata (attributes) are Mandatory!")

        _map_name = _map_name or serializer.validated_data['name']
        _map_title = _map_title or _map_name
        _map_abstract = _map_abstract or ""
        if _data:
            try:
                _map_conf = _data
                _map_conf["about"] = {
                    "name": _map_name,
                    "title": _map_title,
                    "abstract": _map_abstract}
                _map_conf['sources'] = {}
                from geonode.layers.views import layer_detail
                for _lyr in _map_conf['map']['layers']:
                    _lyr_context = None
                    try:
                        _gn_layer = layer_detail(
                            caller.request,
                            _lyr['name'])
                        if _gn_layer and _gn_layer.context_data:
                            _context_data = json.loads(_gn_layer.context_data['viewer'])
                            for _gn_layer_ctx in _context_data['map']['layers']:
                                if 'name' in _gn_layer_ctx and _gn_layer_ctx['name'] == _lyr['name']:
                                    _lyr_context = _gn_layer_ctx
                                    _src_idx = _lyr_context['source']
                                    _map_conf['sources'][_src_idx] = _context_data['sources'][_src_idx]
                    except:
                        tb = traceback.format_exc()
                        logger.error(tb)

                    if _lyr_context:
                        if 'capability' in _lyr_context:
                            _lyr['capability'] = _lyr_context['capability']
                    elif 'source' in _lyr:
                        _map_conf['sources'][_lyr['source']] = {}

                from geonode.maps.models import Map
                _map = Map(
                    title=serializer.validated_data['name'],
                    owner=caller.request.user,
                    center_x=_map_conf['map']['center']['x'],
                    center_y=_map_conf['map']['center']['y'],
                    zoom=_map_conf['map']['zoom'])
                _map.save()
                _map.update_from_viewer(
                    _map_conf,
                    context={'config': _map_conf})
                serializer.validated_data['id'] = _map.id
            except:
                tb = traceback.format_exc()
                logger.error(tb)
                raise APIException(tb)
        else:
            raise APIException("Map Configuration (data) is Mandatory!")

        serializer.save(user=caller.request.user)

        # Save JSON blob
        GeoNodeSerializer.update_data(serializer, _data)

        # Sabe Attributes
        GeoNodeSerializer.update_attributes(serializer, _attributes)

        return serializer.save()

    def perform_update(self, caller, serializer):
        if 'data' in serializer.validated_data:
            _data = serializer.validated_data.pop('data', None)

        if 'attributes' in serializer.validated_data:
            _attributes = serializer.validated_data.pop('attributes', None)

        # Save JSON blob
        GeoNodeSerializer.update_data(serializer, _data)

        # Sabe Attributes
        GeoNodeSerializer.update_attributes(serializer, _attributes)

        return serializer.save()
