from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ashrafi_food/__init__.py
from ashrafi_food import __version__ as version

setup(
	name="ashrafi_food",
	version=version,
	description="Ashrafi Foods",
	author="VFG",
	author_email="shahrukh@ventureforceglobal.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
