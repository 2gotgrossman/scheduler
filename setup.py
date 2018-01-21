from setuptools import setup

setup(
    name='scheduler',
    version='0.4',
    py_modules=['cli'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        D20=cli:D20
    ''',
)
