import os
from setuptools import setup, find_packages


setup(
    name='mkdocs-cake-plugins',
    version='0.0.1',
    author='Cake1salie',
    description='A MkDocs plugin used in SHU Cyberspace Security 101',
    url='https://github.com/LuminolT/security-101-plugins',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs',
        'GitPython'
    ],
    entry_points={
        'mkdocs.plugins': [
            'cake_changelog = mkdocs_cake_plugins.changelog:ChangelogPlugin',
            'cake_contributors = mkdocs_cake_plugins.contributors:ContributorsPlugin',
            # 'turing_evaluations = mkdocs_cake_plugins.evaluations:EvaluationsPlugin',
        ]
    },
    include_package_data=True,
    package_data={
        'src': [
            'templates/*.html'
        ]
    }
)
