from setuptools import setup

setup(
    entry_points={
        'sqlalchemy.dialects': [
            'informix = sqlalchemy_informix.ibmdb:InformixDialect',
        ]
    }
)
