from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# get the version from file
with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    __version__ = f.read()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name="itembox",
    version=__version__,
    description='A REST service to save items.',
    long_description=long_description,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Web Environment',
      'Framework :: Flask',
      'Intended Audience :: Developers',
      'Operating System :: Unix',
      'Programming Language :: Python :: 3.7',
      'Topic :: Database',
      'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    entry_points={
        "console_scripts": [
            "itembox = itembox.manage:cli"
        ]
    },
)