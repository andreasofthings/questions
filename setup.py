import os
from setuptools import setup
from questions import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='questions',
    version=__version__,
    packages=['questions'],
    include_package_data=True,
    license='BSD License',    # example license
    description='Match users by question profile.',
    long_description=README,
    author='Andreas.Neumeier',
    author_email='andreas@neumeier.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',    # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=1.8.0',
        'django-braces',
        'python-dateutil==2.3',
    ],
    dependency_links=[
        'https://github.com/aneumeier/python-django-social/tarball/master#egg=latest',
        'https://github.com/aneumeier/category/tarball/master#egg=latest',
    ]
)
