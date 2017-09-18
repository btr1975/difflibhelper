from setuptools import setup
from difflibhelper.difflibhelper import __version__

packages = [
    'difflibhelper'
]

setup(
    name='difflibhelper',
    version=__version__,
    python_requires='~=3.3',
    description='This script expands on the standard difflib library',
    keywords='diff file differ differences',
    url='https://github.com/btr1975/difflibhelper',
    author='Benjamin P. Trachtenberg',
    author_email='e_ben_75-python@yahoo.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)