from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='consent-decoder',
       version='1.0.1',
       packages=find_packages(),
       license='MediaIQ',
       author='Saurav Omar',
       author_email='sauravomar@mediaiqdigital.com',
       description="Decode web-safe base64 consent information" +
            "with the IAB EU's GDPR Transparency and Consent Framework",
    )

