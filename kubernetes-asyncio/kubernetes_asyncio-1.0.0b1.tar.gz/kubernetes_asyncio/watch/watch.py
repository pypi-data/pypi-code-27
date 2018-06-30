# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pydoc
from functools import partial
from types import SimpleNamespace

from kubernetes_asyncio import client

PYDOC_RETURN_LABEL = ":return:"

# Removing this suffix from return type name should give us event's object
# type. e.g., if list_namespaces() returns "NamespaceList" type,
# then list_namespaces(watch=true) returns a stream of events with objects
# of type "Namespace". In case this assumption is not true, user should
# provide return_type to Watch class's __init__.
TYPE_LIST_SUFFIX = "List"


def _find_return_type(func):
    for line in pydoc.getdoc(func).splitlines():
        if line.startswith(PYDOC_RETURN_LABEL):
            return line[len(PYDOC_RETURN_LABEL):].strip()
    return ""


class Stream(object):

    def __init__(self, func, *args, **kwargs):
        pass


class Watch(object):

    def __init__(self, return_type=None):
        self._raw_return_type = return_type
        self._stop = False
        self._api_client = client.ApiClient()

    def stop(self):
        self._stop = True

    def get_return_type(self, func):
        if self._raw_return_type:
            return self._raw_return_type
        return_type = _find_return_type(func)

        if return_type.endswith(TYPE_LIST_SUFFIX):
            return return_type[:-len(TYPE_LIST_SUFFIX)]
        return return_type

    def unmarshal_event(self, data: str, response_type):
        """Return the K8s response `data` in JSON format.

        """
        js = json.loads(data)

        # Make a copy of the original object and save it under the
        # `raw_object` key because we will replace the data under `object` with
        # a Python native type shortly.
        js['raw_object'] = js['object']

        # Something went wrong. A typical example would be that the user
        # supplied a resource version that was too old. In that case K8s would
        # not send a conventional ADDED/DELETED/... event but an error. Turn
        # this error into a Python exception to save the user the hassle.
        if js['type'].lower() == 'error':
            return js

        # If possible, compile the JSON response into a Python native response
        # type, eg `V1Namespace` or `V1Pod`,`ExtensionsV1beta1Deployment`, ...
        if response_type is not None:
            js['object'] = self._api_client.deserialize(
                response=SimpleNamespace(data=json.dumps(js['raw_object'])),
                response_type=response_type
            )
        return js

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.next()

    async def next(self):
        # Set the response object to the user supplied function (eg
        # `list_namespaced_pods`) if this is the first iteration.
        if self.resp is None:
            self.resp = await self.func()

        # Abort at the current iteration if the user has called `stop` on this
        # stream instance.
        if self._stop:
            raise StopAsyncIteration

        # Fetch the next K8s response.
        line = await self.resp.content.readline()
        line = line.decode('utf8')

        # Stop the iterator if K8s sends an empty response. This happens when
        # eg the supplied timeout has expired.
        if line == '':
            raise StopAsyncIteration

        return self.unmarshal_event(line, self.return_type)

    def stream(self, func, *args, **kwargs):
        """Watch an API resource and stream the result back via a generator.

        :param func: The API function pointer. Any parameter to the function
                     can be passed after this parameter.

        :return: Event object with these keys:
                   'type': The type of event such as "ADDED", "DELETED", etc.
                   'raw_object': a dict representing the watched object.
                   'object': A model representation of raw_object. The name of
                             model will be determined based on
                             the func's doc string. If it cannot be determined,
                             'object' value will be the same as 'raw_object'.

        Example:
            v1 = kubernetes_asyncio.client.CoreV1Api()
            watch = kubernetes_asyncio.watch.Watch()
            async for e in watch.stream(v1.list_namespace, timeout_seconds=10):
                type = e['type']
                object = e['object']  # object is one of type return_type
                raw_object = e['raw_object']  # raw_object is a dict
                ...
                if should_stop:
                    watch.stop()
        """
        self._stop = False
        self.return_type = self.get_return_type(func)
        kwargs['watch'] = True
        kwargs['_preload_content'] = False

        self.func = partial(func, *args, **kwargs)
        self.resp = None

        return self
