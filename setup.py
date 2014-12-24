from setuptools import setup

setup(
    name='wk',
    version='0.1',
    py_modules=['wk'],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        wk=wk:cli
    ''',
)