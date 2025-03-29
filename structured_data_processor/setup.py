from setuptools import setup, find_packages

setup(
    name='document_process',
    version='0.1.0',
    author='Hearn',
    description='A package to process origin file to generate Structured data for ModelEngine, input should less than 512 token and output should no more than 800',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/QkHearn/VectorDatabaseTools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'document_process=document_process.processor:main'
        ],
    },
    install_requires=[
        'xlsxwriter'
    ],
)