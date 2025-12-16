
from setuptools import setup, find_packages

setup(
    name="understar",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "discord.py>=2.3.0",
        "gitpython"
    ],
    author="GalTechDev",
    description="A modular Discord bot framework (V2)",
    long_description=open("README.md", encoding="utf-8").read() if open("README.md", encoding="utf-8") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/GalTechDev/UnderStar-OS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
