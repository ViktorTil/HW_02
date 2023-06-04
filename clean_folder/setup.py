from setuptools import setup

setup(
    name='clean_folder',
    version='1.0.1',
    description='Folder parsing code',
    url='https://github.com/ViktorTil/HW_02',
    author='Tilnyak Viktor',
    author_email='tilnyakviktor@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean_folder = clean_folder.hw_02: main']}
    )
