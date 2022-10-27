"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="team94_robot_2022",  # Required
    version="1.4.0",  # Required
    maintainer="Derelle Redmond",
    maintainer_email="ninetyfouriors@gmail.com",
    description="Team 94: NinetyFouriors Robot code",  # Required
    long_description=long_description,  # Optional
    url="https://github.com/TechnoJays/robot2022",  # Optional
    classifiers=[  # Optional
        "Development Status :: 4 - Beta",
        "Environment :: roboRIO" "Intended Audience :: Developers",
        "Topic :: Robotpy :: Team 94 Robot Code",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="first frc team94 robotpy",  # Optional
    packages=find_packages(exclude=["tests/*"]),  # Required
    install_requires=[
        "wpilib",
        "robotpy",
        "robotpy[commands]",
        "robotpy-wpimath",
        "robotpy-wpiutil",
        "opencv-python",
        # See `robotpy-cscore` install guide for more info
        # "robotpy-cscore" # Only works on certain platforms
        #"robotpy[rev]",
    ],
    extras_require={
        "test": [
            "black", 
            "pipenv", 
            "tox", 
            "tox-pipenv", 
            "coverage", 
            "robotpy[ctre]"
        ],
    },
)
