from configparser import ConfigParser
from pathlib import Path

import setuptools

setup_cfg = ConfigParser()
setup_cfg.read('setup.cfg')
metadata = setup_cfg['metadata']

if __name__ == "__main__":
    setuptools.setup(
        name=metadata['dist_name'],
        description='Opinionated Batteries-Included Python 3 CLI Framework.',
        license='MIT License',
        url=metadata['home_page'],
        version=setup_cfg['bumpversion']['current_version'],
        author=metadata['author'],
        author_email=metadata['author_email'],
        maintainer=metadata['author'],
        maintainer_email=metadata['author_email'],
        long_description=Path('README.md').read_text(),
        long_description_content_type="text/markdown",
        package_data={"milc": ["py.typed"]},
        packages=setuptools.find_packages(exclude=('tests',)),
        scripts=['milc-color'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Human Machine Interfaces',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
        ],
        python_requires='>=3.7',
        install_requires=[
            "argcomplete",
            "colorama",
            "halo",
            "platformdirs",
            "spinners",
            "types-colorama",
            "typing_extensions",
        ],
    )
