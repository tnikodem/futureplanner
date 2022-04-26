import re
import io
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('fup/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='FuturePlanner',
    version="0.1.0",
    license='MIT',
    author='Thomas Nikodem',
    description='Plan the future of your money',
    long_description=readme,
    packages=['fup'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.9',
    install_requires=[
        'numpy>=1.20,<1.23',
        'pandas>=1.2,<1.5',
        'bokeh>=2.3,<2.5',
        'ruamel.yaml>=0.16,<0.18',
        'networkx>=2.5,<2.9'
    ],
    extras_require={
        'dev': [
            'flake8==4.0.1',
            'pytest==7.1.2',
            'pytest-cov==3.0.0'
        ]
    },
    # entry_points={
    #     'console_scripts': [
    #         'fup = fup.cli:main',
    #     ],
    # },
)
