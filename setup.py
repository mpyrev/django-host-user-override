import os
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(BASE_DIR, 'requirements.txt')) as requirements:
    REQUIREMENTS = list(line.strip() for line in requirements.readlines())

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-host-user-override',
    version='0.4.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='MIT License',
    description='Override current user based on subdomain',
    long_description=README,
    author='Mikhail Pyrev',
    author_email='mikhail.pyrev@gmail.com',
    url='https://github.com/mpyrev/django-host-user-override',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
