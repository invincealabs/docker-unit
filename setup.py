from distutils.core import setup

setup(
    name="docker-unit",
    version="1.0",
    description="Test runtime characteristics of Docker Images",
    author="Patrick Nevin Dwyer",
    author_email="patricknevindwyer@gmail.com",
    url="https://github.com/patricknevindwyer/docker-unit",
    scripts=["docker-unit"],
    install_requires=[
        "PyYAML"
    ]
)