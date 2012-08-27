import os, sys

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

from iDB.helpers import IDB_VER

def main():
    setup(
        name='iDB',
        description='iDB Database Engine Library',
        long_description = open('README.md').read(),
        version= IDB_VER,
        url='https://github.com/snowyu/idb.py',
        download_url=  'https://github.com/snowyu/idb.py/tarball/%s' % IDB_VER,
        license='MIT license',
        platforms=['unix', 'linux', 'osx'],
        author='Riceball LEE',
        author_email='snowyu.lee at gmail.com',
        maintainer='Riceball LEE',
        maintainer_email='snowyu.lee@gmail.com',
        keywords =  ['iDB', 'key-value store', 'NoSQL', 'Database'],
        classifiers=['Development Status :: 1 - Planning',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Linux',
                     'Operating System :: MacOS :: MacOS X',
                     'Environment :: Console',
                     'Topic :: Database',
                     'Topic :: Database :: Database Engines/Servers',
                     'Topic :: Software Development :: Libraries',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
        packages=['iDB',
        ],
        install_requires=['bitstring'],
        #test_suite = 'test.all_test',
        zip_safe=False,
    )

if __name__ == '__main__':
    main()
