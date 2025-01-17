# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Paraview(CMakePackage, CudaPackage):
    """ParaView is an open-source, multi-platform data analysis and
    visualization application."""

    homepage = 'https://www.paraview.org'
    url      = "https://www.paraview.org/files/v5.6/ParaView-v5.6.2.tar.xz"
    list_url = "https://www.paraview.org/files"
    list_depth = 1
    git      = "https://gitlab.kitware.com/paraview/paraview.git"

    maintainers = ['chuckatkins', 'danlipsa']

    version('develop', branch='master', submodules=True)
    version('5.6.2', sha256='1f3710b77c58a46891808dbe23dc59a1259d9c6b7bb123aaaeaa6ddf2be882ea')
    version('5.6.0', sha256='cb8c4d752ad9805c74b4a08f8ae6e83402c3f11e38b274dba171b99bb6ac2460')
    version('5.5.2', '7eb93c31a1e5deb7098c3b4275e53a4a')
    version('5.5.1', 'a7d92a45837b67c3371006cc45163277')
    version('5.5.0', 'a8f2f41edadffdcc89b37fdc9aa7f005')
    version('5.4.1', '4030c70477ec5a85aa72d6fc86a30753')
    version('5.4.0', 'b92847605bac9036414b644f33cb7163')
    version('5.3.0', '68fbbbe733aa607ec13d1db1ab5eba71')
    version('5.2.0', '4570d1a2a183026adb65b73c7125b8b0')
    version('5.1.2', '44fb32fc8988fcdfbc216c9e40c3e925')
    version('5.0.1', 'fdf206113369746e2276b95b257d2c9b')
    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378')

    variant('plugins', default=True,
            description='Install include files for plugins support')
    variant('python', default=False, description='Enable Python support')
    variant('python3', default=False, description='Enable Python3 support')
    variant('mpi', default=True, description='Enable MPI support')
    variant('osmesa', default=False, description='Enable OSMesa support')
    variant('qt', default=False, description='Enable Qt (gui) support')
    variant('opengl2', default=True, description='Enable OpenGL2 backend')
    variant('examples', default=False, description="Build examples")
    variant('hdf5', default=False, description="Use external HDF5")

    conflicts('+python', when='+python3')
    conflicts('+python', when='@5.6:')
    conflicts('+python3', when='@:5.5')

    # Workaround for
    # adding the following to your packages.yaml
    # packages:
    #   python:
    #     version: [3, 2]
    # without this you'll get:
    # paraview requires python version 3:, but spec asked for 2.7.16
    # for `spack spec paraview+python+osmesa`
    # see spack pull request #11539
    extends('python', when='+python')
    extends('python', when='+python3')

    depends_on('python@2.7:2.8', when='+python', type=('build', 'run'))
    depends_on('python@3:', when='+python3', type=('build', 'run'))

    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python3', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python+mpi', type=('build', 'run'))
    depends_on('py-mpi4py', when='+python3+mpi', type=('build', 'run'))

    depends_on('py-matplotlib@:2', when='+python', type='run')
    depends_on('py-matplotlib@3:', when='+python3', type='run')

    depends_on('mpi', when='+mpi')
    depends_on('qt+opengl', when='@5.3.0:+qt+opengl2')
    depends_on('qt~opengl', when='@5.3.0:+qt~opengl2')
    depends_on('qt@:4', when='@:5.2.0+qt')

    depends_on('mesa+osmesa', when='+osmesa')
    depends_on('gl@3.2:', when='+opengl2')
    depends_on('gl@1.2:', when='~opengl2')
    depends_on('libxt', when='~osmesa platform=linux')
    conflicts('+qt', when='+osmesa')

    depends_on('bzip2')
    depends_on('freetype')
    # depends_on('hdf5+mpi', when='+mpi')
    # depends_on('hdf5~mpi', when='~mpi')
    depends_on('hdf5+hl+mpi', when='+hdf5+mpi')
    depends_on('hdf5+hl~mpi', when='+hdf5~mpi')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('netcdf')
    depends_on('expat')
    # depends_on('netcdf-cxx')
    # depends_on('protobuf') # version mismatches?
    # depends_on('sqlite') # external version not supported
    depends_on('zlib')
    depends_on('cmake@3.3:', type='build')

    patch('stl-reader-pv440.patch', when='@4.4.0')

    # Broken gcc-detection - improved in 5.1.0, redundant later
    patch('gcc-compiler-pv501.patch', when='@:5.0.1')

    # Broken installation (ui_pqExportStateWizard.h) - fixed in 5.2.0
    patch('ui_pqExportStateWizard.patch', when='@:5.1.2')

    # Broken vtk-m config. Upstream catalyst changes
    patch('vtkm-catalyst-pv551.patch', when='@5.5.0:5.5.2')

    def url_for_version(self, version):
        _urlfmt  = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.{3}'
        """Handle ParaView version-based custom URLs."""
        if version < Version('5.1.0'):
            return _urlfmt.format(version.up_to(2), version, '-source', 'gz')
        elif version < Version('5.6.1'):
            return _urlfmt.format(version.up_to(2), version, '', 'gz')
        else:
            return _urlfmt.format(version.up_to(2), version, '', 'xz')

    @property
    def paraview_subdir(self):
        """The paraview subdirectory name as paraview-major.minor"""
        return 'paraview-{0}'.format(self.spec.version.up_to(2))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        spack_env.set('ParaView_DIR', self.prefix)
        spack_env.set('PARAVIEW_VTK_DIR',
                      join_path(lib_dir, 'cmake', self.paraview_subdir))

    def setup_environment(self, spack_env, run_env):
        # paraview 5.5 and later
        # - cmake under lib/cmake/paraview-5.5
        # - libs  under lib
        # - python bits under lib/python2.8/site-packages
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        run_env.set('ParaView_DIR', self.prefix)
        run_env.set('PARAVIEW_VTK_DIR',
                    join_path(lib_dir, 'cmake', self.paraview_subdir))

        if self.spec.version <= Version('5.4.1'):
            lib_dir = join_path(lib_dir, self.paraview_subdir)

        run_env.prepend_path('LIBRARY_PATH', lib_dir)
        run_env.prepend_path('LD_LIBRARY_PATH', lib_dir)

        if '+python' in self.spec or '+python3' in self.spec:
            if self.spec.version <= Version('5.4.1'):
                pv_pydir = join_path(lib_dir, 'site-packages')
                run_env.prepend_path('PYTHONPATH', pv_pydir)
                run_env.prepend_path('PYTHONPATH', join_path(pv_pydir, 'vtk'))
            else:
                python_version = self.spec['python'].version.up_to(2)
                pv_pydir = join_path(lib_dir,
                                     'python{0}'.format(python_version),
                                     'site-packages')
                run_env.prepend_path('PYTHONPATH', pv_pydir)
                # The Trilinos Catalyst adapter requires
                # the vtkmodules directory in PYTHONPATH
                run_env.prepend_path('PYTHONPATH', join_path(pv_pydir,
                                                             'vtkmodules'))

    def cmake_args(self):
        """Populate cmake arguments for ParaView."""
        spec = self.spec

        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        def nvariant_bool(feature):
            """Negated ternary for spec variant to OFF/ON string"""
            return variant_bool(feature, on='OFF', off='ON')

        rendering = variant_bool('+opengl2', 'OpenGL2', 'OpenGL')
        includes  = variant_bool('+plugins')

        cmake_args = [
            '-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % variant_bool('+qt'),
            '-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % variant_bool('+osmesa'),
            '-DVTK_USE_X:BOOL=%s' % nvariant_bool('+osmesa'),
            '-DVTK_RENDERING_BACKEND:STRING=%s' % rendering,
            '-DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=%s' % includes,
            '-DBUILD_TESTING:BOOL=OFF',
            '-DBUILD_EXAMPLES:BOOL=%s' % variant_bool('+examples'),
            '-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON',
            '-DVTK_USE_SYSTEM_HDF5:BOOL=%s' % variant_bool('+hdf5'),
            '-DVTK_USE_SYSTEM_JPEG:BOOL=ON',
            '-DVTK_USE_SYSTEM_LIBXML2:BOOL=ON',
            '-DVTK_USE_SYSTEM_NETCDF:BOOL=ON',
            '-DVTK_USE_SYSTEM_EXPAT:BOOL=ON',
            '-DVTK_USE_SYSTEM_TIFF:BOOL=ON',
            '-DVTK_USE_SYSTEM_ZLIB:BOOL=ON',
            '-DVTK_USE_SYSTEM_PNG:BOOL=ON',
            '-DOpenGL_GL_PREFERENCE:STRING=LEGACY'
        ]

        # The assumed qt version changed to QT5 (as of paraview 5.2.1),
        # so explicitly specify which QT major version is actually being used
        if '+qt' in spec:
            cmake_args.extend([
                '-DPARAVIEW_QT_VERSION=%s' % spec['qt'].version[0],
            ])

        if '+python' in spec or '+python3' in spec:
            cmake_args.extend([
                '-DPARAVIEW_ENABLE_PYTHON:BOOL=ON',
                '-DPYTHON_EXECUTABLE:FILEPATH=%s' %
                spec['python'].command.path,
                '-DVTK_USE_SYSTEM_MPI4PY:BOOL=%s' % variant_bool('+mpi')
            ])
        else:
            cmake_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=OFF')

        if '+mpi' in spec:
            cmake_args.extend([
                '-DPARAVIEW_USE_MPI:BOOL=ON',
                '-DMPIEXEC:FILEPATH=%s/bin/mpiexec' % spec['mpi'].prefix,
                '-DMPI_CXX_COMPILER:PATH=%s' % spec['mpi'].mpicxx,
                '-DMPI_C_COMPILER:PATH=%s' % spec['mpi'].mpicc,
                '-DMPI_Fortran_COMPILER:PATH=%s' % spec['mpi'].mpifc
            ])

        if '+cuda' in spec:
            cmake_args.extend([
                '-DPARAVIEW_USE_CUDA:BOOL=ON',
                '-DPARAVIEW_BUILD_SHARED_LIBS:BOOL=OFF'
            ])
        else:
            cmake_args.extend([
                '-DPARAVIEW_USE_CUDA:BOOL=OFF',
            ])

        if 'darwin' in spec.architecture:
            cmake_args.extend([
                '-DVTK_USE_X:BOOL=OFF',
                '-DPARAVIEW_DO_UNIX_STYLE_INSTALLS:BOOL=ON',
            ])

        # Hide git from Paraview so it will not use `git describe`
        # to find its own version number
        if spec.satisfies('@5.4.0:5.4.1'):
            cmake_args.extend([
                '-DGIT_EXECUTABLE=FALSE'
            ])

        # A bug that has been found in vtk causes an error for
        # intel builds for version 5.6.  This should be revisited
        # with later versions of Paraview to see if the issues still
        # arises.
        if '%intel' in spec and spec.version >= Version('5.6'):
            cmake_args.append('-DPARAVIEW_ENABLE_MOTIONFX:BOOL=OFF')

        return cmake_args
