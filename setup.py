import setuptools


description = r'''A tree structure to store files & directories.'''

setuptools.setup(
    name='fstree',
    packages = setuptools.find_packages(exclude=['tests*']),
    version="1.0.6",
    description=description,
    author = 'Henry Weickert',
    author_email = 'henryweickert@gmail.com',
    url = 'https://github.com/hweickert/fstree',
    keywords = [],
    entry_points={},
    install_requires=[
        'six',
        'anytree==2.4.3',
        'oyaml==0.9',
    ]
)
