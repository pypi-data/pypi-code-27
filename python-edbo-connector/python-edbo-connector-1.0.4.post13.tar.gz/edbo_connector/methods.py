#!/usr/bin/python
# -*- coding: utf-8 -*-

from .config import MAX_REQUESTS_COUNT, CONNECTION_RETRIES
from .helper import EDBOWebApiHelper


class EDBOWebApiMethods(object):
    """EDBOWebApiMethods - class which implements some RESTful API methods,
    so you don't need to call this methods with many common parameters and
    pass only required and necessary parameters.
    """

    def get_specialities_list(self) -> dict:
        """Get list of available specialities
        :return: Status of last method execution
        :rtype: dict
        """
        specialities_list = self._connector.execute(
            'entrance/specialities/list',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ4_UniversitySpecialities',
                'pageNo': 0,
                'pageSize': 100,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

        return {
            speciality['specialityId']: speciality['specialityFullName'] for speciality in specialities_list
        }

    def get_requests_list(self, limit: int = MAX_REQUESTS_COUNT, full: bool = False,
                          originals_added_only: bool = False) -> list:
        """Get list of available requests
        :param limit: Path to RESTful method
        :param full: Return full data about requests (Default=False)
        :param originals_added_only: Return requests with original documents (Default=False)
        :type limit: int
        :type full: bool
        :type originals_added_only: bool
        :return: List of requests IDs or full data about request
        :rtype: list
        """
        requests_list = self._connector.execute(
            'entrance/personRequest/list',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ1_Orders',
                'pageNo': 0,
                'pageSize': limit,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

        if originals_added_only:
            requests_list = [
                request_item for request_item in requests_list if
                request_item['isOriginalDocumentsAdded'] is True or
                request_item['informationOriginalDocumentLocation'] is True
            ]

        if not full:
            return [request_item['personRequestId'] for request_item in requests_list]
        else:
            return requests_list

    def get_request_info(self, person_request_id: int) -> dict:
        """Get details about person request
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Request details
        :rtype: dict
        """
        return self._connector.execute(
            'entrance/personRequest/get',
            data={
                'governanceTypeId': self._university_info['governanceTypeId'],
                'parentUniversityId': self._university_info['parentUniversityId'],
                'personRequestId': person_request_id,
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

    def get_request_coefficients(self, person_request_id: int) -> dict:
        """Get coefficients for request
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Request coefficients
        :rtype: dict
        """
        return self._connector.execute(
            'entrance/personRequest/coefficients',
            data={
                'personRequestId': person_request_id,
            }
        )

    def get_request_subjects(self, person_request_id: int) -> list:
        """Get subjects for request
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Request subjects array
        :rtype: list
        """
        return self._connector.execute(
            'entrance/personRequest/subjectResult/list',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ1_Orders',
                'pageNo': 0,
                'pageSize': 100,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'personRequestId': person_request_id,
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

    def get_request_person_categories(self, person_request_id: int) -> list:
        """Get person categories
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Person categories array for request
        :rtype: list
        """
        return self._connector.execute(
            'entrance/personRequest/category/list',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ1_Orders',
                'pageNo': 0,
                'pageSize': 100,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'personRequestId': person_request_id,
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

    def get_request_special_conditions(self, person_request_id: int) -> list:
        """Get special conditions for person
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Person special conditions array for request
        :rtype: list
        """
        return self._connector.execute(
            'entrance/personRequest/specialConditions',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ1_Orders',
                'pageNo': 0,
                'pageSize': 100,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'personRequestId': person_request_id,
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
            }
        )

    def get_request_olympiads(self, request_info: list) -> list:
        """Get olympiads added to request
        :param request_info: Request info
        :type request_info: list
        :return: Request olympiads
        :rtype: list
        """
        return self._connector.execute(
            'entrance/personRequest/olympiads/list',
            data={
                'filters': [],
                'governanceTypeId': self._university_info['governanceTypeId'],
                'menuItemCode': 'ENT_NZ1_Orders',
                'pageNo': 0,
                'pageSize': 100,
                'parentUniversityId': self._university_info['parentUniversityId'],
                'personId': request_info['personId'],
                'universityCode': self._university_info['code'],
                'universityId': self._university_info['universityId'],
                'universitySpecialitiesId': request_info['universitySpecialitiesId'],
            }
        )

    def get_full_request(self, person_request_id: int) -> dict:
        """Get all request components
        :param person_request_id: ID of request
        :type person_request_id: int
        :return: Full request information
        :rtype: dict
        """
        for _ in range(0, CONNECTION_RETRIES):
            try:
                request_info = self.get_request_info(person_request_id)
                request_info.update({
                    'requestCoefficients': self.get_request_coefficients(person_request_id),
                    'requestSubjectsResults': self.get_request_subjects(person_request_id),
                    'requestPrivileges': self.get_request_person_categories(person_request_id),
                    'requestSpecialConditions': self.get_request_special_conditions(person_request_id),
                    'requestOlympiads': self.get_request_olympiads(request_info),
                })
                return request_info
            except:
                pass
            continue


    def get_full_requests(self, limit: int = MAX_REQUESTS_COUNT, originals_added_only: bool = False) -> list:
        """Get full info about all available requests
        :param limit: Limit of requests (Default=from config file ~15000)
        :param originals_added_only: Return requests with original documents (Default=False)
        :type limit: int
        :type originals_added_only: bool
        :return: Array with full requests information
        :rtype: list
        """
        requests_list = []
        requests_ids = self.get_requests_list(limit, originals_added_only=originals_added_only)

        for index, request_id in enumerate(requests_ids, start=1):
            requests_list.append(self.get_full_request(request_id))
            print('Завантажено {0:d}/{1:d}'.format(index, len(requests_ids)))

        return requests_list

    def get_education_document_image(self, person_request_id: int, save_to: str = None) -> tuple:
        """Get image with document about education for request
        :param person_request_id: ID of request
        :param save_to: Path to save image (Default=None)
        :type person_request_id: int
        :type save_to: str
        :return: Image data and image size
        :rtype: tuple
        """
        image = self._connector.execute(
            'entrance/files/dodatok',
            data={
                'personRequestId': person_request_id,
            },
            json_format=False
        )

        if image is not None:
            if save_to is not None and len(image.content) > 0:
                EDBOWebApiHelper.save_image(image.content, save_to)

            return image.content, image.headers['Content-Length']
        else:
            return None, None

    def get_registration_document_image(self, person_request_id: int, save_to: str = None) -> tuple:
        """Get image with document about registration in village for request
        :param person_request_id: ID of request
        :param save_to: Path to save image (Default=None)
        :type person_request_id: int
        :type save_to: str
        :return: Image data and image size
        :rtype: tuple
        """
        image = self._connector.execute(
            'entrance/files/regSK',
            data={
                'personRequestId': person_request_id,
            },
            json_format=False
        )

        if image is not None:
            if save_to is not None and len(image.content) > 0:
                EDBOWebApiHelper.save_image(image.content, save_to)

            return image.content, image.headers['Content-Length']
        else:
            return None, None

    def get_person_photo(self, person_request_id: int, save_to: str = None) -> tuple:
        """Get photo of admitter
        :param person_request_id: ID of request
        :param save_to: Path to save image (Default=None)
        :type person_request_id: int
        :type save_to: str
        :return: Image data and image size
        :rtype: tuple
        """
        image = self._connector.execute(
            'entrance/files/photo',
            data={
                'personRequestId': person_request_id,
            },
            json_format=False
        )

        if image is not None:
            if save_to is not None and len(image.content) > 0:
                EDBOWebApiHelper.save_image(image.content, save_to)

            return image.content, image.headers['Content-Length']
        else:
            return None, None

    def get_person_request_document(self, person_request_id: int, save_to: str = None) -> tuple:
        """Get request document of admitter
        :param person_request_id: ID of request
        :param save_to: Path to save document (Default=None)
        :type person_request_id: int
        :type save_to: str
        :return: Image data and image size
        :rtype: tuple
        """
        document = self._connector.execute(
            'entrance/personRequest/reports/personRequest',
            data={
                'personRequestId': person_request_id,
            },
            json_format=False
        )

        if document is not None:
            if save_to is not None and len(document.content) > 0:
                EDBOWebApiHelper.save_image(document.content, save_to)

            return document.content, document.headers['Content-Length']
        else:
            return None, None
