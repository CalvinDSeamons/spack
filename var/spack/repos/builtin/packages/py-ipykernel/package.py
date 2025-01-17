# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpykernel(PythonPackage):
    """IPython Kernel for Jupyter"""

    homepage = "https://pypi.python.org/pypi/ipykernel"
    url      = "https://github.com/ipython/ipykernel/archive/4.5.0.tar.gz"

    version('5.1.0', sha256='30f01a2a1470d3fabbad03f5c43606c1bc2142850fc4ccedcf44281664ae9122')
    version('4.5.0', 'ea6aaf431b100452905aaca208edac72')
    version('4.4.1', 'c0033e524aa9e05ed18879641ffe6e0f')
    version('4.4.0', '8e626a1708ceff83412180d2ff2f3e57')
    version('4.3.1', '971eee85d630eb4bafcd52531c79673f')
    version('4.3.0', '5961164fe908faf798232a265ed48c73')
    version('4.2.2', '4ac8ae11f1eef4920bf4a5383e13ab50')
    version('4.2.1', 'de583ee9c84db6296269ce7de0afb63f')
    version('4.2.0', 'fc535e4e020a41cd2b55508302b155bb')
    version('4.1.1', '51376850c46fb006e1f8d1cd353507c5')
    version('4.1.0', '638a43e4f8a15872f749090c3f0827b6')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.4:', when='@5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@5:')
    depends_on('py-traitlets@4.1.0:', type=('build', 'run'))
    depends_on('py-tornado@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-tornado@4.2:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-ipython@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-ipython@5.0:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-pexpect', type=('build', 'run'))
