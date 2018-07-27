# Copyright 2016 Brigham Young University
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

from typing import List, NamedTuple, Union

import boto3

__VERSION__ = "1.0.1"


class ParamResult(NamedTuple):
    """ParamResult is a NamedTuple that represents a Parameter result.

    Attributes:
        Name (str): Name of the Parameter
        Value (str): Value of the Parameter
        Type (str): Type of the Parameter

    """
    Name: str
    Value: str
    Type: str


class AWSParams(object):
    """AWSParams handles all Parameter Store operations

    Args:
        profile (optional): AWS Profile to use for the session

    Attributes:
        ssm (:obj:`boto3.client`): Boto3 SSM Client object
        profile (str, optional): AWS Profile to use for the session

    """
    ssm = None
    profile = ""

    def __init__(self, profile: str=""):
        self.profile = profile
        if profile:
            session = boto3.Session(profile_name=self.profile)
            self.ssm = session.client("ssm")
        else:
            self.ssm = boto3.client("ssm")

    def _connect_ssm(self, profile: str=""):
        if profile:
            session = boto3.Session(
                profile_name=profile)
            ssm = session.client("ssm")
        else:
            ssm = boto3.client("ssm")
        return ssm

    def put_parameter(self, parameter: dict, *, overwrite: bool=False, profile: str=""):
        """Put a Parameter

        Args:
            parameter (dict): Parameter to create
            overwrite (bool, optional): Flag to overwrite existing parameters
            profile (str, optional): Optional specifiy a alternate profile to use

        """
        if profile:
            ssm = self._connect_ssm(profile)
        else:
            ssm = self.ssm
        if overwrite:
            parameter["Overwrite"] = True
        ssm.put_parameter(**parameter)

    def remove_parameter(self, param: str):
        """Remove a Parameter

        Args:
            param (str): Name of the parameter to remove

        """
        self.ssm.delete_parameter(Name=param)

    def get_parameter_value(self, name: str, *, decryption: bool=True) -> str:
        """Get a specified Parameter's Value

        Args:
            name (str): Name of parameter to get
            decryption (bool, optional): Flag to choose decryption. Defaults True

        Returns:
            str: Value of the Parameter as a string.

        """
        param = self.ssm.get_parameter(Name=name, WithDecryption=decryption)[
            "Parameter"
        ]
        return param["Value"]

    def get_parameter(self, name: str, *, values: bool=True, decryption: bool=True) -> Union[ParamResult, None]:
        """Get a specific Parameter

        Args:
            name (str): Name of parameter to get
            values (bool, optional): Flag to toggle values defaults True
            decryption (bool, optional): Flag to choose decryption. Defaults True

        Returns:
            ParamResult, None: The Parameter for success or else None

        """
        try:
            param = self.ssm.get_parameter(
                Name=name, WithDecryption=decryption)
        except self.ssm.exceptions.ParameterNotFound:
            return
        result = self.build_param_result(
            param["Parameter"], values=values)
        return result

    def build_param_result(self, param: dict, *, prefix: str="", values: bool=True) -> ParamResult:
        """Build a parameter result

        Args:
            param (dict): Parameter to build ParamResult for
            prefix (str, optional): If passed prefix will be removed from parameter name
            values (bool, optional): Flag to toggle values defaults True

        Returns:
            ParamResult: Parameter result in a ParamResult NamedTuple.

        """
        result = {
            "Name": param["Name"].replace(prefix, "") if prefix else param["Name"],
            "Value": param["Value"] if values else None,
            "Type": param["Type"],
        }
        return ParamResult(**result)

    def get_all_parameters(self, *, prefix: str='', by_path: bool=False, values: bool=True, decryption: bool=True, trim_name: bool=True) -> List[ParamResult]:
        """Get all parameters Optionally by prefix or path

        Args:
            prefix (str, optional): Prefix to filter parameters on
            by_path (bool, optional): Flag when specified prefix is a Path defaults False
            values (bool, optional): Flag toggle values defaults True
            decryption (bool, optional): Flag to toggle decryption defaults True
            trim_name (bool, optional): Flag to toggle name trimming on results defaults True

        Returns:
            List[ParamResult]: List of Parameter Results

        """
        trim = prefix if prefix and trim_name else ""
        path = prefix if by_path else '/'
        parameters = []
        paginator = self.ssm.get_paginator('get_parameters_by_path')
        page_iterator = paginator.paginate(
            Path=path, Recursive=True, WithDecryption=decryption)
        for page in page_iterator:
            if prefix and not by_path:
                parameters.extend(
                    [self.build_param_result(param, values=values, prefix=trim)
                     for param in page['Parameters'] if prefix in param['Name']]
                )
            else:
                parameters.extend(
                    [self.build_param_result(param, values=values, prefix=trim)
                     for param in page['Parameters']]
                )
        return parameters

    def new_param(self, name: str, value: str, *, param_type: str="String", key: str="", description: str="", overwrite: bool=False):
        """
        Create a new parameter

        Args:
            name (str): Name of new parameter.
            value (str): Value of the new parameter
            param_type (str, optional): Type of New parameter default "String"
            key (str, optional): KMS Key to encrypt default ""
            description (str, optional): Description of the new parameter default ""
            overwrite (bool, optional): Flag to toggle overwriting existing parameter default False

        """
        param = {
            "Name": name,
            "Value": value,
            "Type": param_type,
            "Overwrite": overwrite,
        }
        if key:
            param['KeyId'] = key
        if description:
            param["Description"] = description
        self.put_parameter(param, overwrite=overwrite)

    def set_param(self, param: str, value: str) -> bool:
        """
        Edit an existing parameter

        Args:
            param (str): Name of parameter to set.
            value (str): Value to set.

        Returns:
            bool: True for modified False for unmodified
        """
        existing_value = self.get_parameter_value(param, decryption=True)
        if existing_value != value:
            put = self.get_parameter(
                name=param, values=True, decryption=True
            )._asdict()
            put["Value"] = value
            self.put_parameter(put, overwrite=True)
            return True
        else:
            return False
