from setuptools import setup

setup(
    name='plumb',
    packages=[
        'plumb',
        'plumb.aws',
        'plumb.kafka',
        'plumb.redis',
        'plumb.rabbitmq'
    ],
    version='1.2.0',
    description='Connect systems via many brokers such as Kafka, AWS SQS, RabbitMQ and more.',
    long_description=open('README.rst').read(),

    install_requires=['boto3', 'confluent_kafka==0.11.4', 'redis'],
    tests_require=['awstestutils'],

    test_suite='tests',

    author='Spectro Data Engineering Team',
    author_email='data-engineering@spect.ro',

    keywords=['redis', 'AWS', 'queues', 'distributed', 'kafka', 'RabbitMQ', 'AMQP'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: System :: Networking',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Object Brokering',
    ]
)
