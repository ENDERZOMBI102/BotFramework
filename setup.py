import setuptools

with open( 'README.md', 'r', encoding='utf-8' ) as file:
	long_description = file.read()

setuptools.setup(
	name='botframework-enderzombi102',
	version='1.0.0',
	author='ENDERZOMBI102',
	author_email='enderzombi102.end@gmail.com',
	description='A feature rich, yet low level discord bot framework',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ENDERZOMBI102/BotFramework',
	project_urls={
		'Bug Tracker': 'https://github.com/ENDERZOMBI102/BotFramework/issues',
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Development Status :: 4 - Beta',
		'Framework :: AsyncIO'
	],
	package_dir={"": 'src'},
	packages=setuptools.find_packages(
		where='src',
		exclude='modules'
	),
	python_requires='>=3.7',
)
