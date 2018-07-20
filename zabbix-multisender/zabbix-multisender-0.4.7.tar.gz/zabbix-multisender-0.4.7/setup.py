#!/usr/bin/python3

from setuptools import setup
# import xdg.BaseDirectory

setup(
    name="zabbix-multisender",
    version="0.4.7",

    description="Zabbix MiltiSender",

    author="Vojtěch Pachol",
    author_email="v.pachol@mikroelektronika.cz",

    # license="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ],
    keywords="python, zabbix",

    # packages=find_packages(exclude=["contrib", "docs", "tests*", "latex"]),
    packages=["zms"],

    install_requires=["PyYAML", "pyxdg", "jsbeautifier",
                      "SQLAlchemy", "psycopg2"],

    # package_data={
    #     'zms': ["*.yaml", "*.db"],
    # },

    # data_files=[(os.path.join(xdg.BaseDirectory.xdg_data_home, "zms"),
    data_files=[
        # ("share/zms/", [
        #     "data/zms.yaml",
        #     "data/unavailables.db",
        #     "data/zms.html",
        # ]),
        # ("share/systemd/user/", [
        #     "systemd/system/zms-sender.service",
        #     "systemd/system/zms-sender.timer",
        #     "systemd/system/zms-listener.service",
        # ]),
        # ("/etc/apache2/sites-available/", [
        #     "etc/apache2/sites-available/zms.conf",
        # ]),
        # ("/etc/init.d/", [
        #     "etc/init.d/zms",
        # ]),
    ],

    entry_points={
        "console_scripts": [
            "zms-listener=zms:listen",
            "zms-sender=zms:sendfromdb_loop",

            "zms-send=zms:sendfromdb_once",
            "zms-list=zms:list_unavailable",
        ],
    },
)
