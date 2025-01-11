from setuptools import setup, find_packages

setup(
    name="compiler",  # Replace with your project's name
    version="0.1.0",
    packages=find_packages(),
    package_dir={"": "."},  # `src` contains the root of the packages
)
