from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'pywin_contextmenu',
    # https://packaging.python.org/en/latest/single_source_version.html
    version = '2020.9.1',
    # https://packaging.python.org/specifications/core-metadata/#summary
    description = 'A simple and intuitive way to add your custom scripts to '
                  'the windows right click contextmenu.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url = 'https://github.com/naveennamani/pywin_contextmenu',
    author = 'Naveen Namani',
    author_email = 'naveennamani877@gmail.com',
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers = [  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
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
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    # package_dir={'': 'src'},  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    py_modules = ["pywin_contextmenu"],
    # packages=find_packages(where='src'),  # Required

    python_requires = '>=3.5, <4',

    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [''],
    entry_points = {
        # 'console_scripts': [
        #     'sample=sample:main',
        # ],
    },
    project_urls = {
        'Bug Reports': 'https://github.com/naveennamani/pywin_contextmenu/issues',
        'Source': 'https://github.com/naveennamani/pywin_contextmenu/',
    },
)
