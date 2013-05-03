import os
import re
from setuptools import setup
from setuptools.command.test import test
import sys

absolute_path = lambda x: os.path.join(os.path.dirname(__file__), x)
readme_path = absolute_path(u'README.md')

def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def run_tests(*args):
    srcdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    sys.path.insert(0, os.path.join(srcdir, 'test_project'))
    if not os.environ.get("DJANGO_SETTINGS_MODULE", False):
        os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

    from django.conf import settings
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_suite = TestRunner(verbosity=2, interactive=True, failfast=False)
    errors = test_suite.run_tests([])
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)
    
test.run_tests = run_tests


setup(
    name = "django-template-preprocessor",
    version='1.2.29',
    url = 'https://github.com/citylive/django-template-preprocessor',
    license = 'BSD',
    description = "Template preprocessor/compiler for Django",
    long_description = open(readme_path, 'r').read(),
    author = 'Jonathan Slenders, City Live nv',
    packages = ['template_preprocessor'], #find_packages('src', exclude=['*.test_project', 'test_project', 'test_project.*', '*.test_project.*']),
    package_dir = {'': 'src'},
    package_data = {'template_preprocessor': [
        'templates/*.html', 'templates/*/*.html', 'templates/*/*/*.html',
        'static/*/js/*.js', 'static/*/css/*.css',
        ],},
    include_package_data=True,
    install_requires = parse_requirements('requirements.txt'),
    zip_safe=False, # Don't create egg files, Django cannot find templates in egg files.
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Software Development :: Internationalization',
    ],
    test_suite = 'dummy',
)

