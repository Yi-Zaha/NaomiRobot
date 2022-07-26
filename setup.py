import re

from setuptools import setup


version = ""
with open("neko/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)


requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()


if not version:
    raise RuntimeError("version is not set")


setup(
    name="nekosxx.py",
    author="AlexFlipnote",
    url="https://github.com/kagutsuchi57/nekosxx.py/",
    version=version,
    packages=["neko"],
    license="GNU v3",
    description="A Python module that uses Nekos API",
    include_package_data=True,
    install_requires=requirements,
)
