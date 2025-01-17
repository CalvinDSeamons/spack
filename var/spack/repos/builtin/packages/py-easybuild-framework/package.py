# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEasybuildFramework(PythonPackage):
    """The core of EasyBuild, a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = 'https://easybuilders.github.io/easybuild'
    url      = 'https://pypi.io/packages/source/e/easybuild-framework/easybuild-framework-4.0.0.tar.gz'
    maintainers = ['boegel']

    version('4.0.0', sha256='f5c40345cc8b9b5750f53263ade6c9c3a8cd3dfab488d58f76ac61a8ca7c5a77')
    version('3.1.2', '283bc5f6bdcb90016b32986d52fd04a8')

    depends_on('python@2.6:2.8', when='@:3', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.5:', when='@4:', type=('build', 'run'))
    depends_on('py-setuptools', when='@:3', type=('build', 'run'))
    depends_on('py-vsc-base@2.5.4:', when='@2.9:3', type='run')

    # Only required for tests (python -O -m test.framework.suite)
    depends_on('py-vsc-install', when='@:3', type='test')
