from setuptools import setup

setup(
    name='MS_Booker',
    version='v0.1',
    packages=['card_app'],
    url='',
    license='',
    author='Nicholas A. Del Grosso',
    author_email='delgrosso@biochem.mpg.de',
    description='',
    install_requires=['jinja2', 'pandas', 'flask', 'xlrd', 'PyPDF2', 'XCaliburMethodReader', 'matplotlib'],
    include_package_data=True,
    zip_safe=False,
)
