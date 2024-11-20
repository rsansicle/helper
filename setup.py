from setuptools import setup, find_packages

setup(
    name="helpers",
    version="0.1.0",
    description="A brief description of your project",
    author="rsansicle",
    url="https://github.com/rsansicle/helper.git",
    packages=find_packages(),
    install_requires=[
        "boto3==1.35.65",
        "python-dotenv==1.0.0"
    ],
    python_requires=">=3.7"
)