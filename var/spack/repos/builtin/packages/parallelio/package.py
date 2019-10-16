# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
import sys
import os

from spack import *


class Parallelio(AutotoolsPackage):
    """Abandon all hope ye who runs this spack package."""

    # blah.
    homepage = "https://github.com/NCAR/ParallelIO"
    url      = "https://github.com/NCAR/ParallelIO/releases/download/pio2_4_4/pio-2.4.4.tar.gz"

    version('2.4.4', sha256='69ed1535b16b3b5a42b37849e324cf9d2f4fa5d9fa87092e3574642eb12355e9')
    version('2.4.3', sha256='71ce0be0de3abb7e6a3a7f44de7ffa98f26d103e7c37c45ae4350a86def7c400')
    version('2.4.2', sha256='55e7c0d8911139599e2f31b1aa79bf5e0f2818d2519ae40671db5711977afcc6')
    version('2.4.1', sha256='f3ca3f56aa18efa1c4d7cdc6ce1c7b11d3f6382d31ec96874897814dffe6a78a')

    variant('full',    default=False, description='If not relying on packages already built use "+full"')
    variant('fortran', default=False, description='Builds with netcdf-fortran')
    variant('shared',  default=False, description='Enable shared')

    depends_on('zlib@1.2.11')
    depends_on('openmpi@3.1.2',                                   type='build', when='+full')
    depends_on('python@2.7',                                      type='build', when='+full')
    depends_on('hdf5@1.10.5~cxx+fortranio+shared+mpi+hl+vfd+all', type='build', when='+full')
    depends_on('parallel-netcdf+shared',                          type='build', when='+full')
    depends_on('netcdf@4.7.0+parallel-netcdf+mpi+shared',         type='build', when='+full')
    depends_on('netcdf-fortran',                                  type='build', when='+full')

    def configure_args(self):
        spec = self.spec
        rpath = self.rpath
        args = []
        #cflags = []
        cppflags = []
        ldflags = []

        hdf5_hl = self.spec['hdf5:hl']
        pnetcdf = self.spec['parallel-netcdf']

        #cflags.append(self.compiler.pic_flag)
        cppflags.append(hdf5_hl.headers.cpp_flags)
        cppflags.append(pnetcdf.headers.cpp_flags)
        #ldflags.append(curl_libs.search_flags)
        #ldflags.append(hdf5_hl.libs.search_flags)
        #ldflags.insert(0,'-L')
        #cppflags.insert(0,'-I')
        netcdf = ('%s' % self.spec['netcdf'].prefix)
        ldflags.append(netcdf+'/lib -lnetcdf')
        if '+full' in spec:
            args.append('CC=%s' % self.spec['openmpi'].prefix +'/bin/mpicc')
            args.append('FC=mpif90')
            args.append('CFLAG=-std=c99')

        if '+fortran' in spec:
            args.append('--enable-fortran')
        if '+shared' in spec:
            args.append('--enable-shared')

        #args.append('CFLAGS=' + ' '.join(cflags))
        args.append('CPPFLAGS=' + ' '.join(cppflags))
        args.append('LDFLAGS=' + ' '.join(ldflags))
        return args

