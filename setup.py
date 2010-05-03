from setuptools import setup, find_packages
import os

version = '0.2dev'

setup(name='collective.geo.kml',
      version=version,
      description="collective.geo extension for zgeo.kml",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() +
                       open("TODO.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules :: Scientific/Engineering :: GIS",
        ],
      keywords='plone geo gis kml google earth',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://svn.plone.org/svn/collective/collective.geo.kml',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zgeo.kml',
          'collective.geo.mapwidget',
          'collective.geo.geographer',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
