# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mpas-model
#
# You can edit this file again by typing:
#
#     spack edit mpas-model
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
import os
from spack import *
from os import *

class MpasModel(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "https://github.com/MPAS-Dev/MPAS-Model/archive/v7.0.tar.gz"

    version('7.0', sha256='f898ce257e66cff9e29320458870570e55721d16cb000de7f2cc27de7fdef14f')
    version('6.3', sha256='e7f1d9ebfeb6ada37d42a286aaedb2e69335cbc857049dc5c5544bb51e7a8db8')
    version('6.2', sha256='2a81825a62a468bf5c56ef9d9677aa2eb88acf78d4f996cb49a7db98b94a6b16')

    depends_on('parallelio')

    #def edit(self, spec, prefix):
    #    makefile = FileFilter('Makefile')
    #    makefile.filter('CORE=init_atmosphere',prefix)

    def build(self, spec, prefix):
        pio     = ('PIO=%s' % self.spec['parallelio'].prefix + ' ')
        pnetcdf = ('PNETCDF=%s' % self.spec['parallel-netcdf'].prefix + ' ')
        netcdf  = ('NETCDF=%s' % self.spec['netcdf'].prefix + ' ')

        make(pio,pnetcdf,netcdf,'gfortran', 'CORE=init_atmosphere', 'USE_PIO2=true', 'DEBUG=true', 'PRECISION=single')
