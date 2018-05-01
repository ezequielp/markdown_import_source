from setuptools import setup
VERSION = '0.8'

setup(
    name='Markdown Import Source Extension',
    version=VERSION,
    py_modules=['mdx_import_source'],
    author="Ezequiel Pozzo",
    author_email="ezequiel.pozzo@gmail.com",
    description="Import external sources in a Markdown block",
    license="MIT",
    url="https://github.com/ezequielp/markdown_import_source",
    install_requires=['markdown>=2.5'],
        classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)