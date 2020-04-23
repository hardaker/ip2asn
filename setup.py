import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ip2asn",
    version="0.5.1",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A python class to quickly search ip2asn data for range matches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hardaker/ip2asn",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'ip2asn = ip2asn.main:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['pyfsdb>=0.9.2',
    ],
    python_requires = '>=3.0',
    test_suite='nose.collector',
    tests_require=['nose'],
)
