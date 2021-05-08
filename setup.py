from distutils.core import setup

from setuptools import find_namespace_packages

setup(
    name="time-elapse-recorder",
    version="0.0.1",
    description="A script to record time-elapse video using computer's camera!",
    author="PENG Zhenghao",
    author_email="pengzh@ie.cuhk.edu.hk",
    packages=find_namespace_packages(),
    install_requires=[
        "opencv-python",
        "click"
    ],
    include_package_data=False,
    license="Apache 2.0",
)
