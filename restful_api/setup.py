import os
from setuptools import setup, find_packages
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename='.flaskenv'))

setup(
    name="myapi",
    version=os.getenv('VERSION'),
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-restful",
        "flask-migrate",
        "flask-jwt-extended",
        "flask-marshmallow",
        "marshmallow-sqlalchemy",
        "python-dotenv",
        "passlib",
        "apispec[yaml]",
        "apispec-webframeworks",
    ],
    entry_points={
        "console_scripts": [
            "myapi = myapi.manage:cli"
        ]
    },
)
