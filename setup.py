from os import path
from setuptools import setup


pwd = path.abspath(path.dirname(__file__))
with open(path.join(pwd, 'README.md'), 'r') as f:
    readme = f.read()


setup(
    name='lqubo',
    version='0.1.0',
    description='A quantum/classical hybrid optimizer',
    long_description=readme,
    long_description_content_type='test/markdown',
    url='git@github.com:seangholson/lqubo.git',
    author='Sean Gholson, Group W, Inc.',
    author_email='sgholson@groupw.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='quantum computing hybrid algorithm',
    project_urls={
        'Documentation': 'git@github.com:seangholson/lqubo.git',
        'Source': 'git@github.com:seangholson/lqubo.git',
        'Bugs': 'https://github.com/seangholson/lqubo/issues',
        'Say hi!': 'mailto:sgholson@groupw.com',
    },
    packages=[
        'experiment_code',
        'form_LQUBO',
        'quality_of_LQUBO_and_methods',
        'response_selection',
        'solvers',
        'switch_networks',
        'tabu_experiment',
        'utilities',
    ],
    python_requires='>=3.5, <4',
    install_requires=[
        'dwave-ocean-sdk', 
        'numpy',
        'pandas',
    ],
)
