
from setuptools import setup

setup(
    name="horsephrase",
    version="0.6.0",
    description="Secure password generator.",
    long_description=(
        "Like http://correcthorsebatterystaple.net/ except it's not a web page"
        " which is logging your passwords and sending them all to the NSA."
    ),
    author="Glyph",
    author_email="glyph@twistedmatrix.com",
    maintainer="Glyph",
    maintainer_email="glyph@twistedmatrix.com",
    url="https://github.com/glyph/horsephrase/",
    packages=["horsephrase"],
    package_data=dict(
        horsephrase=["*.txt"],
    ),
    install_requires=['six==1.11.0'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points={
        "console_scripts": [
            "horsephrase = horsephrase.__main__:main",
        ],
    },
    extras_require={
        ':python_version == "2.7"': ['mock'],
        'dev': ['requests'],
    }
)
