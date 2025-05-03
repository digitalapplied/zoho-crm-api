from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="zoho_crm_api_toolkit",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.7",
    author="Digital Applied",
    author_email="development@digitalapplied.com",
    description="A Python package for interacting with the Zoho CRM API v8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digitalapplied/digitalapplied-zoho-crm-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Groupware",
    ],
    keywords='zoho crm api client rest integration',
) 