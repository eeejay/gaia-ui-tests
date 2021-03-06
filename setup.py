import os
from setuptools import setup, find_packages
import shutil

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

# version number
version = {}
execfile(os.path.join('gaiatest', 'version.py'), version)

# dependencies
deps = ['marionette_client==0.5.35', 'mozdevice', 'py==1.4.14']

# copy atoms directory over
setupdir = os.path.dirname(__file__)
jsdir = os.path.join(setupdir, os.pardir, 'atoms')
pythondir = os.path.join(setupdir, 'gaiatest', 'atoms')

if os.path.isdir(jsdir):
    if os.path.isdir(pythondir):
        shutil.rmtree(pythondir)
    print 'copying JS atoms from %s to %s' % (jsdir, pythondir)
    shutil.copytree(jsdir, pythondir)
else:
    if os.path.isdir(pythondir):
        print 'using JS atoms from %s' % pythondir
    else:
        raise Exception('JS atoms not found in %s or %s!' % (jsdir, pythondir))

setup(name='gaiatest',
      version=version['__version__'],
      description="Marionette test automation client for Gaia",
      long_description=description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Jonathan Griffin',
      author_email='jgriffin@mozilla.com',
      url='https://developer.mozilla.org/en-US/docs/Marionette',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={'gaiatest': [
          'atoms/*.js',
          'resources/report/jquery.js',
          'resources/report/main.js',
          'resources/report/style.css']},
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      gaiatest = gaiatest.runtests:main
      """,
      install_requires=deps,
      )
