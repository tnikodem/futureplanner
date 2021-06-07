import re
import io
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('fup/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='FuturePlanner',
    version="0.0.0",
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
        'numpy==1.20.*',
        'pandas==1.2.*',
        'bokeh==2.3.*',
        'ruamel.yaml>=0.16,<0.18',
        'networkx==2.5.*'
    ],
    extras_require={
        'dev': [
            'flake8==3.9.2',
            'pytest==6.2.4',
            'pytest-cov==2.12.1'
        ]
    },
    # entry_points={
    #     'console_scripts': [
    #         'fup = fup.cli:main',
    #     ],
    # },
)
