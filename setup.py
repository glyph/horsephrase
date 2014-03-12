
from setuptools import setup

setup(
    name="horsephrase",
    version="0.2.0",
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
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        "console_scripts": [
            "horsephrase = horsephrase:output",
        ],
    },
)
