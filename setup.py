from setuptools import setup, find_packages

setup(
    name="zoho_crm_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "python-dotenv==1.0.0",
    ],
    python_requires="3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for interacting with the Zoho CRM API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zoho-crm-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 