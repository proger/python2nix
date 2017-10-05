from setuptools import setup
from setuptools import find_packages

setup(name='python2nix',
      version='0.1',
      description='put a PyPI package name in, get a Nix expression out',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='Vladimir Kirillov',
      author_email='proger@hackndev.com',
      url='https://github.com/proger/python2nix',
      license='ISC',
      packages=find_packages(),
      install_requires=['requests', 'pip'],
      entry_points="""
      [console_scripts]
      python2nix = python2nix:main
      """,
      include_package_data=True,
      zip_safe=False,
)
