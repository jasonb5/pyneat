from distutils.core import setup

setup(name='pyneat',
        version='1.0',
        packages=['pyneat', 'pyneat.genotype', 'pyneat.ann'],
        install_requires=['numpy', 'django'])
