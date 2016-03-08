from setuptools import setup, find_packages


def read_md(file):
    try:
        # noinspection PyPackageRequirements,PyUnresolvedReferences
        from pypandoc import convert

        return convert(file, 'rst', 'md')
    except ImportError:
        import warnings
        warnings.warn('pypandoc module not found, could not convert Markdown to RST')

        with open(file, 'r') as md:
            return md.read()


setup(
    name='Tumblr Downloader',
    version='0.1.0',
    description='A Tumblr image and video scraping utility',
    long_description=read_md('README.md'),
    author='makoto',
    author_email='makoto@makoto.io',
    url='',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',

        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Mirroring',
        'Topic :: Utilities',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tumdlr = tumdlr.main:cli'
        ]
    },
    install_requires=['click', 'yurl', 'lxml', 'requests', 'humanize', 'appdirs']
)