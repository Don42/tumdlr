from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='Tumblr Downloader',
    version='0.1.0',
    description='A Tumblr image and video scraping utility',
    # long_description=readme(),
    author='makoto',
    author_email='makoto@makoto.io',
    url='',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
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
    install_requires=['click', 'yurl', 'lxml', 'requests', 'humanize', ]
)