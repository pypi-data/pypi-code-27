# -*- coding:utf-8 -*-
from .app import Application

from .build import main
from .build.tasks import Task

from .bases.session import Session
from .bases.service import Service
from .bases.repository import Repository
from .bases.response import FileResponse
from .bases.components import Component, Cookie

from .solo import Solo
from .solo.manager import SoloManager

from .console import main as console

from .types import Type, AsyncType, TypeEncoder, validators

from .route import route, get, post, delete, put, options


__version__ = "0.6.9"
