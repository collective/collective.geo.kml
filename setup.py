from setuptools import setup, find_packages
import os

version = '3.3'

setup(name='collective.geo.kml',
      version=version,
      description="Kml view for collective.geo",
      long_description=(
          open("README.rst").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      classifiers=[
          "Framework :: Plone",
          "Topic :: Internet",
          "Topic :: Scientific/Engineering :: GIS",
          "Programming Language :: Python",
      ],
      keywords='Zope Plone GIS KML Google Maps Bing OpenLayers',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://github.com/collective/collective.geo.kml',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
          'collective.geo.mapwidget >= 2.1.1',
          'collective.geo.geographer >= 2.0',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'mock',
              'collective.geo.behaviour',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
