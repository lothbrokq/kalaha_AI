from setuptools import setup, find_packages

setup(
    name='kalaha_ai',
    version='0.1.0',
    author='Boran Aydas',
    author_email='boran@aydas.dk',
    packages=find_packages(),
    url='https://github.com/lothbrokq/kalaha_AI',
    description='Group 55 - Kahala Game + AI Implementation',
    long_description=open('README.md').read(),
    install_requires=[
        # List your project's dependencies here.
        # They will be installed by pip when your project is installed.
        # Example: 'requests >= 2.19.1'
    ],
    python_requires='>=3.6', # Specify the minimum Python version required
    include_package_data=True, # Whether to include non-code files in your package
)