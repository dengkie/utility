from setuptools import setup, find_packages

setup(
        name='utility',
        version='1.0',
        description='ma-utility',
        keywords="logging configuring utility",
        author='Peng Wu',
        author_email='peng.wu@mindarchitect.cn',
        platforms='mac windows raspbian',
        packages=find_packages(),
        install_requires=[
                'verboselogs>=1.7',
                'coloredlogs>=10.0'
        ]
)

