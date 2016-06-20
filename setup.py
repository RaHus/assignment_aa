import os, sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

pyver = sys.version_info[0]

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'colander',
    'pyramid_mailer'
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

dev_require = [
    'waitress',
    'pyramid_debugtoolbar',
    'IPython'
]

if pyver == 2:
    tests_require.append("Mock")

setup(name='assignment_aa',
      version='0.0',
      description='assignment_aa',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Rami Chousein',
      author_email='rami.chousein@gmail.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
          'development': dev_require
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = assignment_aa:main
      [console_scripts]
      initialize_assignment_aa_db = assignment_aa.scripts.initializedb:main
      """,
      )
