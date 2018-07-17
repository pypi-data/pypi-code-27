import logging

from pip._internal import req
from pip._internal.req import req_install

from .requirement import Requirement

req.InstallRequirement = Requirement
req_install.InstallRequirement = Requirement

from pipreqs import pipreqs
pipreqs.logging = logging.getLogger("pipreqs")
