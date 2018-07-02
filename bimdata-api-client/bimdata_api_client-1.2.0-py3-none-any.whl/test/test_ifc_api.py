# coding: utf-8

"""
    BIMData API

    BIMData API documentation  # noqa: E501

    OpenAPI spec version: v1
    Contact: contact@bimdata.io
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import bimdata_api_client
from bimdata_api_client.api.ifc_api import IfcApi  # noqa: E501
from bimdata_api_client.rest import ApiException


class TestIfcApi(unittest.TestCase):
    """IfcApi unit test stubs"""

    def setUp(self):
        self.api = bimdata_api_client.api.ifc_api.IfcApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_bulk_delete_ifc_classifications(self):
        """Test case for bulk_delete_ifc_classifications

        """
        pass

    def test_bulk_delete_ifc_properties(self):
        """Test case for bulk_delete_ifc_properties

        """
        pass

    def test_bulk_delete_ifc_property_definitions(self):
        """Test case for bulk_delete_ifc_property_definitions

        """
        pass

    def test_bulk_delete_ifc_units(self):
        """Test case for bulk_delete_ifc_units

        """
        pass

    def test_bulk_delete_property_set(self):
        """Test case for bulk_delete_property_set

        """
        pass

    def test_bulk_full_update_elements(self):
        """Test case for bulk_full_update_elements

        """
        pass

    def test_bulk_full_update_ifc_property(self):
        """Test case for bulk_full_update_ifc_property

        """
        pass

    def test_bulk_remove_classifications_of_element(self):
        """Test case for bulk_remove_classifications_of_element

        """
        pass

    def test_bulk_remove_elements_from_classification(self):
        """Test case for bulk_remove_elements_from_classification

        """
        pass

    def test_bulk_update_elements(self):
        """Test case for bulk_update_elements

        """
        pass

    def test_bulk_update_ifc_property(self):
        """Test case for bulk_update_ifc_property

        """
        pass

    def test_create_classification_element_relations(self):
        """Test case for create_classification_element_relations

        """
        pass

    def test_create_classifications_of_element(self):
        """Test case for create_classifications_of_element

        """
        pass

    def test_create_element(self):
        """Test case for create_element

        """
        pass

    def test_create_element_property_set(self):
        """Test case for create_element_property_set

        """
        pass

    def test_create_element_property_set_property(self):
        """Test case for create_element_property_set_property

        """
        pass

    def test_create_element_property_set_property_definition(self):
        """Test case for create_element_property_set_property_definition

        """
        pass

    def test_create_element_property_set_property_definition_unit(self):
        """Test case for create_element_property_set_property_definition_unit

        """
        pass

    def test_create_ifc_property_definition(self):
        """Test case for create_ifc_property_definition

        """
        pass

    def test_create_ifc_unit(self):
        """Test case for create_ifc_unit

        """
        pass

    def test_create_property_set(self):
        """Test case for create_property_set

        """
        pass

    def test_create_property_set_element_relations(self):
        """Test case for create_property_set_element_relations

        """
        pass

    def test_create_raw_elements(self):
        """Test case for create_raw_elements

        """
        pass

    def test_create_space(self):
        """Test case for create_space

        """
        pass

    def test_create_zone(self):
        """Test case for create_zone

        """
        pass

    def test_create_zone_space(self):
        """Test case for create_zone_space

        """
        pass

    def test_delete_element(self):
        """Test case for delete_element

        """
        pass

    def test_delete_ifc(self):
        """Test case for delete_ifc

        """
        pass

    def test_delete_ifc_property(self):
        """Test case for delete_ifc_property

        """
        pass

    def test_delete_ifc_property_definition(self):
        """Test case for delete_ifc_property_definition

        """
        pass

    def test_delete_ifc_unit(self):
        """Test case for delete_ifc_unit

        """
        pass

    def test_delete_property_set(self):
        """Test case for delete_property_set

        """
        pass

    def test_delete_space(self):
        """Test case for delete_space

        """
        pass

    def test_delete_zone(self):
        """Test case for delete_zone

        """
        pass

    def test_delete_zone_space(self):
        """Test case for delete_zone_space

        """
        pass

    def test_full_update_element(self):
        """Test case for full_update_element

        """
        pass

    def test_full_update_ifc(self):
        """Test case for full_update_ifc

        """
        pass

    def test_full_update_ifc_property(self):
        """Test case for full_update_ifc_property

        """
        pass

    def test_full_update_ifc_property_definition(self):
        """Test case for full_update_ifc_property_definition

        """
        pass

    def test_full_update_ifc_unit(self):
        """Test case for full_update_ifc_unit

        """
        pass

    def test_full_update_property_set(self):
        """Test case for full_update_property_set

        """
        pass

    def test_full_update_space(self):
        """Test case for full_update_space

        """
        pass

    def test_full_update_zone(self):
        """Test case for full_update_zone

        """
        pass

    def test_full_update_zone_space(self):
        """Test case for full_update_zone_space

        """
        pass

    def test_get_classifications_of_element(self):
        """Test case for get_classifications_of_element

        """
        pass

    def test_get_element(self):
        """Test case for get_element

        """
        pass

    def test_get_element_property_set(self):
        """Test case for get_element_property_set

        """
        pass

    def test_get_element_property_set_properties(self):
        """Test case for get_element_property_set_properties

        """
        pass

    def test_get_element_property_set_property(self):
        """Test case for get_element_property_set_property

        """
        pass

    def test_get_element_property_set_property_definition(self):
        """Test case for get_element_property_set_property_definition

        """
        pass

    def test_get_element_property_set_property_definition_unit(self):
        """Test case for get_element_property_set_property_definition_unit

        """
        pass

    def test_get_element_property_set_property_definition_units(self):
        """Test case for get_element_property_set_property_definition_units

        """
        pass

    def test_get_element_property_set_property_definitions(self):
        """Test case for get_element_property_set_property_definitions

        """
        pass

    def test_get_element_property_sets(self):
        """Test case for get_element_property_sets

        """
        pass

    def test_get_elements(self):
        """Test case for get_elements

        """
        pass

    def test_get_elements_from_classification(self):
        """Test case for get_elements_from_classification

        """
        pass

    def test_get_ifc(self):
        """Test case for get_ifc

        """
        pass

    def test_get_ifc_bvh(self):
        """Test case for get_ifc_bvh

        """
        pass

    def test_get_ifc_classifications(self):
        """Test case for get_ifc_classifications

        """
        pass

    def test_get_ifc_gltf(self):
        """Test case for get_ifc_gltf

        """
        pass

    def test_get_ifc_map(self):
        """Test case for get_ifc_map

        """
        pass

    def test_get_ifc_properties(self):
        """Test case for get_ifc_properties

        """
        pass

    def test_get_ifc_property(self):
        """Test case for get_ifc_property

        """
        pass

    def test_get_ifc_property_definition(self):
        """Test case for get_ifc_property_definition

        """
        pass

    def test_get_ifc_property_definitions(self):
        """Test case for get_ifc_property_definitions

        """
        pass

    def test_get_ifc_structure(self):
        """Test case for get_ifc_structure

        """
        pass

    def test_get_ifc_systems(self):
        """Test case for get_ifc_systems

        """
        pass

    def test_get_ifc_unit(self):
        """Test case for get_ifc_unit

        """
        pass

    def test_get_ifc_units(self):
        """Test case for get_ifc_units

        """
        pass

    def test_get_ifcs(self):
        """Test case for get_ifcs

        """
        pass

    def test_get_property_set(self):
        """Test case for get_property_set

        """
        pass

    def test_get_property_sets(self):
        """Test case for get_property_sets

        """
        pass

    def test_get_raw_elements(self):
        """Test case for get_raw_elements

        """
        pass

    def test_get_space(self):
        """Test case for get_space

        """
        pass

    def test_get_spaces(self):
        """Test case for get_spaces

        """
        pass

    def test_get_zone(self):
        """Test case for get_zone

        """
        pass

    def test_get_zone_space(self):
        """Test case for get_zone_space

        """
        pass

    def test_get_zone_spaces(self):
        """Test case for get_zone_spaces

        """
        pass

    def test_get_zones(self):
        """Test case for get_zones

        """
        pass

    def test_list_classification_element_relations(self):
        """Test case for list_classification_element_relations

        """
        pass

    def test_remove_classification_of_element(self):
        """Test case for remove_classification_of_element

        """
        pass

    def test_remove_element_property_set(self):
        """Test case for remove_element_property_set

        """
        pass

    def test_remove_element_property_set_property(self):
        """Test case for remove_element_property_set_property

        """
        pass

    def test_remove_element_property_set_property_definition(self):
        """Test case for remove_element_property_set_property_definition

        """
        pass

    def test_remove_element_property_set_property_definition_unit(self):
        """Test case for remove_element_property_set_property_definition_unit

        """
        pass

    def test_remove_elements_from_classification(self):
        """Test case for remove_elements_from_classification

        """
        pass

    def test_update_element(self):
        """Test case for update_element

        """
        pass

    def test_update_ifc(self):
        """Test case for update_ifc

        """
        pass

    def test_update_ifc_files(self):
        """Test case for update_ifc_files

        """
        pass

    def test_update_ifc_property(self):
        """Test case for update_ifc_property

        """
        pass

    def test_update_ifc_property_definition(self):
        """Test case for update_ifc_property_definition

        """
        pass

    def test_update_ifc_unit(self):
        """Test case for update_ifc_unit

        """
        pass

    def test_update_property_set(self):
        """Test case for update_property_set

        """
        pass

    def test_update_space(self):
        """Test case for update_space

        """
        pass

    def test_update_zone(self):
        """Test case for update_zone

        """
        pass

    def test_update_zone_space(self):
        """Test case for update_zone_space

        """
        pass


if __name__ == '__main__':
    unittest.main()
