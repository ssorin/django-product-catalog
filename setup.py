import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'readme.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-product-catalog',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple app to manage products in a catalog (portfolio for example).',
    long_description=README,
    url='https://github.com/ssorin/django-product-catalog',
    author='Samuel SORIN',
    author_email='ssorin@dwdlc.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-mptt==0.8.7',
        'Pillow==8.3.2',
        'django-extensions==1.9.1'
    ]
)