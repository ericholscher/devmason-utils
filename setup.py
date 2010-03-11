from setuptools import setup

setup(name='devmason_utils',
      version='0.1',
      description='A Python client implementation of a the devmason server.',
      author = 'Eric Holscher',
      url = 'http://github.com/ericholscher/devmason-utils',
      license = 'BSD',
      packages = ['devmason_utils'],
      install_requires=['httplib2'],
)
