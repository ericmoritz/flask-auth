from setuptools import setup, find_packages


setup(name="flask-auth",
      description="Authentication framework for Flask",
      version="0.1-alpha",
      packages=find_packages(),
      test_suite="flaskext.auth.tests")
