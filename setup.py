from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'pywin_contextmenu',
    version = '2020.9.7',
    description = 'A simple and intuitive way to add your custom scripts to '
                  'the windows right click contextmenu.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/naveennamani/pywin_contextmenu',
    author = 'Naveen Namani',
    author_email = 'naveennamani877@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords = 'windows contextmenu customscripts contextmenu-organization '
               'windows-contextmenu-organization productivity-tools utility-tools',
    py_modules = ["pywin_contextmenu"],
    # packages=find_packages(where='src'),  # Required
    python_requires = '>=3.5, <4',
    install_requires = [''],
    entry_points = {
        # 'console_scripts': [
        #     'create-cm-item=pywin_contextmenu:create_cm_cli',
        # ],
    },
    project_urls = {
        'Bug Reports': 'https://github.com/naveennamani/pywin_contextmenu/issues',
        'Source': 'https://github.com/naveennamani/pywin_contextmenu/',
    },
)
