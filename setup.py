import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ogtrans",
    version="0.0.1",
    packages=find_packages(exclude='tests'),
    install_requires=['polib'],
    tests_require=["pytest"],
    author="Bernhard Bockelbrink",
    author_email="bernhard.bockelbrink@gmail.com",
    description="Commandline tools to translate text in OmniGraffle files",
    long_description=read("ogtrans/README.md"),
    license="http://www.opensource.org/licenses/mit-license.php",
    keywords="omnigraffle export gettext i18n command",
    url="https://github.com/bboc/omnigraffle-tools",
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Operating System :: MacOS :: MacOS X',
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'ogtrans = ogtrans.commands:main',
        ],
    },
    test_suite='tests',
    zip_safe=True,

)
