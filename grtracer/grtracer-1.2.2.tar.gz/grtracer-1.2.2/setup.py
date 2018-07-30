from setuptools import setup

setup(
    name='grtracer',
    version='1.2.2',
    description='Simple tracing setup using Jaeger and Flask',
    url='https://github.com/ryzokuken/grtracer',
    author='Ujjwal Sharma',
    author_email='usharma1998@gmail.com',
    license='MIT',
    packages=['grtracer'],
    install_requires=[
        'flask==0.10.1',
        'flask_opentracing==0.2.0',
        'jaeger_client==3.10.0',
        'opentracing_instrumentation==2.4.1'
    ],
    zip_safe=False
)
