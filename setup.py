from setuptools import setup, find_packages
import sys, os

version = '2.0'

setup(name='cybertools',
      version=version,
      description="cybertools",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Helmut Merz',
      author_email='helmutm@cy55.de',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            # -*- Extra requirements: -*-
            'lxml',
            'PIL',
            'zope.app.catalog',
            'zope.app.file',
            'zope.app.intid',
            'zope.app.preview',
            'zope.app.renderer',
            'zope.app.session',
            'zope.sendmail',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
