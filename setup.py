from setuptools import setup, find_packages
import sys, os

version = '2.1.4'

setup(name='cybertools',
      version=version,
      description="cybertools: basic utilities for Zope3/bluebream/loops",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='cyberconcepts.org team',
      author_email='team@cyberconcepts.org',
      url='https://www.cyberconcepts.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            # -*- Extra requirements: -*-
            'lxml',
            #'Pillow',
            'zope.app.catalog',
            'zope.app.file',
            'zope.app.intid',
            'zope.app.session',
            'zope.sendmail',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
