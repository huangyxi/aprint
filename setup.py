from setuptools import setup, find_packages
import os

setup(
	name='aprint',
	version=os.getenv('GITHUB_REF', '0.0.0').split('/')[-1].removeprefix('v'),
	description='A function to print arrays in a concise way',
	long_description=open('README.md').read(),
	long_description_content_type = "text/markdown",
	author='HUANG Yuxi',
	author_email='aprint@hyxi.dev',
	url='https://github.com/huangyxi/aprint',
	license='MIT License',
	keywords=('aprint', 'print'),
	platforms='any',
	packages=find_packages(),
	install_requires=[
	],
)
