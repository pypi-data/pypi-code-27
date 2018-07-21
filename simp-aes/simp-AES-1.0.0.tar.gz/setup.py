import setuptools
setuptools.setup(name='simp-AES',
            description="A simple script for AES encryption and decryption using a user-inputted password.",
            version='1.0.0',
            author='C. Johnson',
            author_email='',
            license='MIT',
            classifiers=[
            'Programming Language :: Python :: 3'
            ],
            packages=setuptools.find_packages(),
            install_requires=['pycrypto']
            )
