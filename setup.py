from setuptools import find_packages
from setuptools import setup

package_name = 'ros2autodoc'

setup(
  name=package_name,
  version='0.0.0',
  packages=find_packages(exclude=['test']),
  install_requires=['ros2cli'],
  zip_safe=True,
  author='Mohamed Abdelaziz',
  author_email='mohamed.abdelaziz@tutanota.de',
  url='https://github.com/3473f/ros2autodoc',
  keywords=[],
  classifiers=[
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python',
  ],
  description='CLI command to automatically generate documentation for ROS2 nodes in markdown syntax.',
  long_description="""The project provides a CLI command to automatically generate documentation for ROS2 nodes in markdown syntax.""",
  license='Apache License, Version 2.0',
  tests_require=['pytest'],
  entry_points={
        'ros2cli.command': [
            'autodoc = ros2autodoc.command.autodoc:AutodocCommand',
        ],
        'ros2autodoc.verb' : [
            'generate =  ros2autodoc.verb.generate:GenerateVerb',
        ],
    }
)
