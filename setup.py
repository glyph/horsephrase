
from setuptools import setup

setup(
    name="horsephrase",
    version="2022.12.9.1",
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
        horsephrase=["*.txt", "py.typed"],
    ),
    license="MIT",
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "horsephrase = horsephrase.__main__:main",
        ],
    },
    extras_require={
        ':python_version < "3.8"': ['typing_extensions'],
        'dev': ['requests'],
    }
)
