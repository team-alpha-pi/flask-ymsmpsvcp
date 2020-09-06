from setuptools import setup, find_packages

with open('requirements.txt', 'r') as req_f:
    requirements = req_f.read().split()

setup(
    name='Flask-YMSMPSVCP',
    version='1.0',
    author='Michael Shustin',
    author_email='michaelshustinl@gmail.com',
    description='YMSMPSCCP Configuration for',
    packages=find_packages(),
    python_requires=">= 3.6",
    platforms='any',
    install_requires=requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)