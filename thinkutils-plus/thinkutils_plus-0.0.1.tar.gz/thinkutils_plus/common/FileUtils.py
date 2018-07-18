#!/usr/bin/python
#coding=utf-8

import os

def create_folder_if_not_exists(szPath):
    if False == os.path.exists(szPath):
        os.makedirs(szPath)