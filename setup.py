from setuptools import setup, find_packages

setup(
    name='qdynpylib',  
    version='0.1.0',  
    description='quantum mechanics simulation library',
    author='ishaan ganti',
    author_email='ishaan_ganti@brown.edu',
    url='https://github.com/ishaanganti/qlib',  
    license='MIT', 
    packages=find_packages(),
    install_requires=[
        'numpy',        
        'scipy',
        'matplotlib',
        'wolframclient'
    ],
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
