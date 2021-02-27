import re
import io
from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="FuturePlaner",
    install_requires=[
        "numpy"
    ]
)

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('fup/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='FuturePlaner',
    version="0.0.0",
    license='MIT',
    author='Thomas Nikodem',
    description='Plan the future of your money',
    long_description=readme,
    packages=['fup'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.8',
    install_requires=[
        'numpy==1.19.*',
        'pandas==1.2.*',
    ],
    extras_require={
        'dev': [
            'pytest==4.0.*',
            'pytest-cov==2.6.*',
        ]
    },
    # entry_points={
    #     'console_scripts': [
    #         'fup = fup.cli:main',
    #     ],
    # },
)

