import os
import json

try:
    from urlparse import urlunparse
except ImportError:
    from urllib.parse import urlunparse

from azure.storage.blob import PublicAccess
from azure.common import AzureMissingResourceHttpError, AzureHttpError

from dtoolcore.storagebroker import BaseStorageBroker

from dtoolcore.utils import (
    generate_identifier,
    get_config_value,
    mkdir_parents,
    generous_parse_uri,
    timestamp
)

from dtoolcore.filehasher import FileHasher, md5sum_hexdigest

from dtool_azure import __version__
from dtool_azure.utils import base64_to_hex, get_blob_service


_STRUCTURE_PARAMETERS = {
    "fragments_key_prefix": "fragments/",
    "overlays_key_prefix": "overlays/",
    "dataset_readme_key": "README.yml",
    "manifest_key": "manifest.json",
    "structure_dict_key": "structure.json",
    "dtool_readme_key": "README.txt",
    "admin_metadata_key": "dtool",
    "http_manifest_key": "http_manifest.json",
    "storage_broker_version": __version__,
}

_DTOOL_README_TXT = """README
======
This is a Dtool dataset stored in Azure storage.

Content provided during the dataset creation process
----------------------------------------------------

Azure container named $UUID, where UUID is the unique identifier for the
dataset.

Dataset descriptive metadata: README.yml

Dataset items. The keys for these blobs are item identifiers. An item
identifier is the sha1sum hexdigest of the relative path used to represent the
file on traditional file system disk.

Administrative metadata describing the dataset is encoded as metadata on the
container.


Automatically generated blobs
-----------------------------

This file: README.txt
Structural metadata describing the dataset: structure.json
Structural metadata describing the data items: manifest.json
Per item descriptive metadata prefixed by: overlays/
"""


class AzureStorageBroker(BaseStorageBroker):

    #: Attribute used to define the type of storage broker.
    key = "azure"

    #: Attribute used by :class:`dtoolcore.ProtoDataSet` to write the hash
    #: function name to the manifest.
    hasher = FileHasher(md5sum_hexdigest)

    _structure_parameters = _STRUCTURE_PARAMETERS
    _dtool_readme_txt = _DTOOL_README_TXT

    def __init__(self, uri, config_path=None):

        parse_result = generous_parse_uri(uri)

        self.storage_account_name = parse_result.netloc

        uuid = parse_result.path[1:]

        self.uuid = uuid

        self.fragments_key_prefix = self._generate_key('fragments_key_prefix')
        self.overlays_key_prefix = self._generate_key('overlays_key_prefix')

        self.http_manifest_key = self._generate_key("http_manifest_key")

        self._azure_cache_abspath = get_config_value(
            "DTOOL_AZURE_CACHE_DIRECTORY",
            config_path=config_path,
            default=os.path.expanduser("~/.cache/dtool/azure")
        )

        self._blobservice = get_blob_service(
            self.storage_account_name,
            config_path
        )

    # Generic helper functions.

    def _generate_key(self, structure_dict_key):
        return self._structure_parameters[structure_dict_key]

    def _get_blob_properties(self, handle):
        identifier = generate_identifier(handle)
        return self._blobservice.get_blob_properties(
            self.uuid,
            identifier
        )

    def _generate_http_manifest(self):

        readme_url = self._blobservice.make_blob_url(
            self.uuid,
            "README.yml"
        )

        manifest_url = self._blobservice.make_blob_url(
            self.uuid,
            "manifest.json"
        )

        overlays = {}
        for overlay_name in self.list_overlay_names():
            overlay_fpath = self.overlays_key_prefix + overlay_name + '.json'
            overlays[overlay_name] = self._blobservice.make_blob_url(
                self.uuid,
                overlay_fpath
            )

        manifest = self.get_manifest()
        item_urls = {}
        for identifier in manifest["items"]:
            item_urls[identifier] = self._blobservice.make_blob_url(
                self.uuid,
                identifier
            )

        http_manifest = {
            "admin_metadata": self.get_admin_metadata(),
            "item_urls": item_urls,
            "overlays": overlays,
            "readme_url": readme_url,
            "manifest_url": manifest_url
        }

        return http_manifest

    def _write_http_manifest(self, http_manifest):

        self.put_text(
            self.http_manifest_key,
            json.dumps(http_manifest)
        )

    # Class methods to override.

    @classmethod
    def generate_uri(cls, name, uuid, base_uri):

        scheme, netloc, path, _, _, _ = generous_parse_uri(base_uri)
        assert scheme == 'azure'

        # Force path (third component of tuple) to be the dataset UUID
        uri = urlunparse((scheme, netloc, uuid, _, _, _))

        return uri

    @classmethod
    def list_dataset_uris(cls, base_uri, config_path):
        """Return list containing URIs with base URI."""

        storage_account_name = generous_parse_uri(base_uri).netloc
        blobservice = get_blob_service(storage_account_name, config_path)
        containers = blobservice.list_containers(include_metadata=True)

        uri_list = []
        for c in containers:
            admin_metadata = c.metadata
            uri = cls.generate_uri(
                admin_metadata['name'],
                admin_metadata['uuid'],
                base_uri
            )
            uri_list.append(uri)

        return uri_list

    # Methods to override.

    def get_structure_key(self):
        return self._generate_key("structure_dict_key")

    def get_dtool_readme_key(self):
        return self._generate_key("dtool_readme_key")

    def get_admin_metadata_key(self):
        return self._generate_key("admin_metadata_key")

    def get_readme_key(self):
        return self._generate_key("dataset_readme_key")

    def get_manifest_key(self):
        return self._generate_key("manifest_key")

    def get_overlay_key(self, overlay_name):
        return self.overlays_key_prefix + overlay_name + '.json'

    def _create_structure(self):

        result = self._blobservice.create_container(self.uuid)

        if not result:
            raise Exception(
                "Container for {} already exists.".format(self.uuid)
            )

    def put_admin_metadata(self, admin_metadata):
        super(AzureStorageBroker, self).put_admin_metadata(admin_metadata)

        for k, v in admin_metadata.items():
            admin_metadata[k] = str(v)

        self._blobservice.set_container_metadata(
            self.uuid,
            admin_metadata
        )

    def get_admin_metadata(self):

        return self._blobservice.get_container_metadata(
            self.uuid
        )

    def has_admin_metadata(self):
        """Return True if the administrative metadata exists.

        This is the definition of being a "dataset".
        """

        try:
            self.get_admin_metadata()
            return True
        except (AzureMissingResourceHttpError, AzureHttpError):
            return False

    def list_overlay_names(self):
        """Return list of overlay names."""

        overlay_names = []
        for blob in self._blobservice.list_blobs(
            self.uuid,
            prefix=self.overlays_key_prefix
        ):
            overlay_file = blob.name.rsplit('/', 1)[-1]
            overlay_name, ext = overlay_file.split('.')
            overlay_names.append(overlay_name)

        return overlay_names

    def put_item(self, fpath, relpath):

        identifier = generate_identifier(relpath)

        self._blobservice.create_blob_from_path(
            self.uuid,
            identifier,
            fpath
        )

        self._blobservice.set_blob_metadata(
            container_name=self.uuid,
            blob_name=identifier,
            metadata={
                "relpath": relpath,
                "type": "item"
            }
        )

        return relpath

    def add_item_metadata(self, handle, key, value):
        """Store the given key:value pair for the item associated with handle.

        :param handle: handle for accessing an item before the dataset is
                       frozen
        :param key: metadata key
        :param value: metadata value
        """

        identifier = generate_identifier(handle)

        metadata_blob_suffix = "{}.{}.json".format(identifier, key)
        metadata_blob_name = self.fragments_key_prefix + metadata_blob_suffix

        self._blobservice.create_blob_from_text(
            self.uuid,
            metadata_blob_name,
            json.dumps(value)
        )

        self._blobservice.set_blob_metadata(
            container_name=self.uuid,
            blob_name=metadata_blob_name,
            metadata={
                "type": "item_metadata"
            }
        )

    def get_text(self, key):

        try:
            text_blob = self._blobservice.get_blob_to_text(
                self.uuid,
                key
            )
        except AzureMissingResourceHttpError:
            raise NameError("Can't retrieve text with name {}".format(key))

        return text_blob.content

    def put_text(self, key, contents):
        """Store the given text contents so that they are later retrievable by
        the given key."""

        self._blobservice.create_blob_from_text(
            self.uuid,
            key,
            contents
        )

    def get_item_abspath(self, identifier):
        """Return absolute path at which item content can be accessed.

        :param identifier: item identifier
        :returns: absolute path from which the item content can be accessed
        """
        admin_metadata = self.get_admin_metadata()
        uuid = admin_metadata["uuid"]
        # Create directory for the specific dataset.
        dataset_cache_abspath = os.path.join(self._azure_cache_abspath, uuid)
        mkdir_parents(dataset_cache_abspath)

        metadata = self._blobservice.get_blob_metadata(
            self.uuid,
            identifier
        )

        relpath = metadata['relpath']
        _, ext = os.path.splitext(relpath)

        local_item_abspath = os.path.join(
            dataset_cache_abspath,
            identifier + ext
        )
        if not os.path.isfile(local_item_abspath):

            tmp_local_item_abspath = local_item_abspath + ".tmp"
            self._blobservice.get_blob_to_path(
                self.uuid,
                identifier,
                tmp_local_item_abspath
            )
            os.rename(tmp_local_item_abspath, local_item_abspath)

        return local_item_abspath
        # original_path = self.item_properties(identifier)['path']

    def iter_item_handles(self):
        """Return iterator over item handles."""

        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            include='metadata'
        )

        for blob in blob_generator:
            if 'type' in blob.metadata:
                if blob.metadata['type'] == 'item':
                    handle = blob.metadata['relpath']
                    yield handle

    def get_size_in_bytes(self, handle):
        blob = self._get_blob_properties(handle)
        return blob.properties.content_length

    def get_utc_timestamp(self, handle):
        blob = self._get_blob_properties(handle)
        aware_datetime = blob.properties.last_modified
        naive_datetime = aware_datetime.replace(tzinfo=None)
        return timestamp(naive_datetime)

    def get_hash(self, handle):
        blob = self._get_blob_properties(handle)
        md5_base64 = blob.properties.content_settings.content_md5
        if md5_base64 is None:
            md5_hexdigest = None
        else:
            md5_hexdigest = base64_to_hex(md5_base64)
        return md5_hexdigest

# According to the tests the below is not needed.
#   def get_relpath(self, handle):
#       blob = self._get_blob_properties(handle)
#       return blob.metadata['relpath']

    def pre_freeze_hook(self):
        pass

    def post_freeze_hook(self):

        self.fragments_key_prefix
        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            prefix=self.fragments_key_prefix
        )

        # Delete the temporary fragment metadata objects from the bucket.
        for blob in blob_generator:
            self._blobservice.delete_blob(self.uuid, blob.name)

    def get_item_metadata(self, handle):
        """Return dictionary containing all metadata associated with handle.

        In other words all the metadata added using the ``add_item_metadata``
        method.

        :param handle: handle for accessing an item before the dataset is
                       frozen
        :returns: dictionary containing item metadata
        """

        metadata = {}

        identifier = generate_identifier(handle)
        prefix = self.fragments_key_prefix + '{}'.format(identifier)

        blob_generator = self._blobservice.list_blobs(
            self.uuid,
            include='metadata',
            prefix=prefix
        )

        for blob in blob_generator:
            metadata_key = blob.name.split('.')[-2]
            value_as_string = self.get_text(blob.name)
            value = json.loads(value_as_string)

            metadata[metadata_key] = value

        return metadata

    def http_enable(self):

        http_manifest = self._generate_http_manifest()
        self._write_http_manifest(http_manifest)

        self._blobservice.set_container_acl(
            self.uuid,
            public_access=PublicAccess.Container
        )

        access_url = '{}://{}/{}'.format(
            self._blobservice.protocol,
            self._blobservice.primary_endpoint,
            self.uuid
        )

        return access_url

    def _list_historical_readme_keys(self):
        # This method is used to test the
        # BaseStorageBroker.readme_update method.
        prefix = self.get_readme_key() + "-"
        historical_readme_keys = []
        for blob in self._blobservice.list_blobs(
            self.uuid,
            prefix=prefix
        ):
            key = blob.name
            historical_readme_keys.append(key)
        return historical_readme_keys
