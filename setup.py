from setuptools import find_packages, setup

PACKAGE_NAME = "ros2autodoc"

setup(
    name=PACKAGE_NAME,
    version="1.2.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/" + PACKAGE_NAME, ["package.xml"]),
        ("share/ament_index/resource_index/packages", ["resource/" + PACKAGE_NAME]),
    ],
    install_requires=["ros2cli"],
    zip_safe=True,
    author="Mohamed Abdelaziz",
    author_email="mohamed.abdelaziz@tutanota.de",
    url="https://github.com/3473f/ros2autodoc",
    keywords=[],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The 3-Clause BSD License",
        "Programming Language :: Python",
    ],
    description="CLI command to automatically generate documentation for ROS2 nodes in markdown syntax.",  # noqa: E501
    long_description="""The project provides a CLI command to automatically generate documentation for ROS2 nodes in markdown syntax.""",  # noqa: E501
    license="BSD 3-Clause",
    tests_require=["pytest"],
    entry_points={
        "ros2cli.command": [
            "autodoc = ros2autodoc.command.autodoc:AutodocCommand",
        ],
        "ros2autodoc.verb": [
            "generate =  ros2autodoc.verb.generate:GenerateVerb",
            "update = ros2autodoc.verb.update:UpdateVerb",
        ],
    },
)
