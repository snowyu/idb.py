import os, sys

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

def main():
    setup(
        name='iDB',
        description='iDB Library',
        long_description = open('README.txt').read(),
        version='0.0.1',
        url='https://github.com/snowyu/pyidb',
        license='MIT license',
        platforms=['unix', 'linux', 'osx'],
        author='Riceball LEE',
        author_email='snowyu.lee at gmail.com',
        classifiers=['Development Status :: 1 - Planning',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Linux',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Database',
                     'Topic :: Software Development :: Libraries',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
        packages=['idb',
        ],
        zip_safe=False,
    )

if __name__ == '__main__':
    main()
