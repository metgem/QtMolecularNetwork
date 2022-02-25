import os
import sys
import shlex
import subprocess
import glob

from setuptools import setup, find_packages
from setuptools.extension import Extension
from distutils import sysconfig, dir_util, spawn, log
from distutils.dep_util import newer
import sipdistutils
import sipconfig
import versioneer

try:
    from PyQt5.QtCore import PYQT_CONFIGURATION
except ImportError:
    PYQT_CONFIGURATION = {}

MODULE_NAME = "PyQtNetworkView"
SRC_PATH = MODULE_NAME

IS_COMPILED = True
if "--skip-build" in sys.argv:
    IS_COMPILED = False
    sys.argv.remove("--skip-build")
    
REQUIRE_PYQT = True
if "--conda-recipe" in sys.argv:
    REQUIRE_PYQT = False
    sys.argv.remove("--conda-recipe")


def which(name):
    """
    Return the path of program named 'name' on the $PATH.
    """
    if os.name == "nt" and not name.endswith(".exe"):
        name += ".exe"
        
    for path in os.environ["PATH"].split(os.pathsep):
        path = os.path.join(path, name)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
            
    return None

class HostPythonConfiguration(object):
    def __init__(self):
        self.platform = sys.platform
        self.version = sys.hexversion>>8

        self.inc_dir = sysconfig.get_python_inc()
        self.venv_inc_dir = sysconfig.get_python_inc(prefix=sys.prefix)
        self.module_dir = sysconfig.get_python_lib(plat_specific=1)

        if sys.platform == 'win32':
            self.data_dir = sys.prefix
            self.lib_dir = sys.prefix +'\\libs'
            self.module_inc_dir = os.environ.get('LIBRARY_INC')
            if self.module_inc_dir is None:
                self.module_inc_dir = sysconfig.get_config_var('INCLUDEPY')
        else:
            self.data_dir = sys.prefix + '/share'
            self.lib_dir = sys.prefix + '/lib'
            self.module_inc_dir = sysconfig.get_config_var('INCLUDEDIR')
            

class TargetQtConfiguration(object):
    def __init__(self, qmake):
        pipe = os.popen(' '.join([qmake, '-query']))

        for l in pipe:
            l = l.strip()

            tokens = l.split(':', 1)
            if isinstance(tokens, list):
                if len(tokens) != 2:
                    error("Unexpected output from qmake: '%s'\n" % l)

                name, value = tokens
            else:
                name = tokens
                value = None

            name = name.replace('/', '_')
            setattr(self, name, value)

        pipe.close()
        

class build_ext(sipdistutils.build_ext):
    
    description = "Builds the " + MODULE_NAME + " module."
    
    user_options = sipdistutils.build_ext.user_options + [
        ('qmake-bin=', None, "Path to qmake binary"),
        ('sip-bin=', None, "Path to sip binary"),
        ('qt-include-dir=', None, "Path to Qt headers"),
        ('pyqt-sip-dir=', None, "Path to PyQt's SIP files"),
        ('pyqt-sip-flags=', None, "SIP flags used to generate PyQt bindings"),
        ('sip-dir=', None, "Path to module's SIP files"),
        ('inc-dir=', None, "Path to module's include files")
    ]
    
    def initialize_options (self):
        super().initialize_options()
        self.qmake_bin = 'qmake'
        self.sip_bin = None
        self.qt_include_dir = None
        self.qt_libinfix = ''
        self.pyqt_sip_dir = None
        self.pyqt_sip_flags = None
        self.sip_files_dir = None
        self.sip_inc_dir = None
        self.inc_dir = None
        self.module_inc_dir = None
        self.pyconfig = HostPythonConfiguration()
        self.qtconfig = TargetQtConfiguration(self.qmake_bin)
        self.config = sipconfig.Configuration()    
        self.config.default_mod_dir = ("/usr/local/lib/python%i.%i/dist-packages" %
                                      (sys.version_info.major, sys.version_info.minor))
        
    def finalize_options (self):
        super().finalize_options()

        if not self.qt_include_dir:
            self.qt_include_dir = self.qtconfig.QT_INSTALL_HEADERS
            
        if not self.qt_libinfix:
            try:
                with open(os.path.join(self.qtconfig.QT_INSTALL_PREFIX, 'mkspecs', 'qconfig.pri'), 'r') as f:
                    for line in f.readlines():
                        if line.startswith('QT_LIBINFIX'):
                            self.qt_libinfix = line.split('=')[1].strip('\n').strip()
            except (FileNotFoundError, IndexError):
                pass

        if not self.pyqt_sip_dir:
            self.pyqt_sip_dir = os.path.join(self.pyconfig.data_dir, 'sip', 'PyQt5')
            
        if not self.pyqt_sip_flags:
            self.pyqt_sip_flags = PYQT_CONFIGURATION.get('sip_flags', '')
            
        if not self.sip_files_dir:
            self.sip_files_dir = os.path.abspath(os.path.join(".", "sip"))
            
        if not self.sip_inc_dir:
            self.sip_inc_dir = self.pyconfig.venv_inc_dir
            
        if not self.module_inc_dir:
            self.module_inc_dir = self.pyconfig.module_inc_dir
            
        if not self.inc_dir:
            self.inc_dir = os.path.abspath(os.path.join(".", "src"))

        if not self.qt_include_dir:
            raise SystemExit('Could not find Qt5 headers. '
                             'Please specify via --qt-include-dir=')

        if not self.pyqt_sip_dir:
            raise SystemExit('Could not find PyQt SIP files. '
                             'Please specify containing directory via '
                             '--pyqt-sip-dir=')

        if not self.pyqt_sip_flags:
            raise SystemExit('Could not find PyQt SIP flags. '
                             'Please specify via --pyqt-sip-flags=')
        
    def _find_sip(self):
        """override _find_sip to allow for manually speficied sip path."""
        if self.sip_bin:
            return self.sip_bin
            
        sip_bin = super()._find_sip()
        if os.path.isfile(sip_bin):
            return sip_bin
        
        return which('sip')
        
    def _sip_compile(self, sip_bin, source, sbf): 
        cmd = [sip_bin]
        if hasattr(self, 'sip_opts'):
            cmd += self.sip_opts
        if hasattr(self, '_sip_sipfiles_dir'):
            _sip_sipfiles_dir = self._sip_sipfiles_dir()
            if os.path.exists(_sip_sipfiles_dir):
                cmd += ['-I', _sip_sipfiles_dir]
        cmd += [
            "-I", self.sip_files_dir,
            "-I", self.pyqt_sip_dir,
            "-I", self.sip_inc_dir,
            "-I", self.inc_dir,
            "-c", self._sip_output_dir(),
            "-b", sbf,
            "-w", "-o"]
        
        cmd += shlex.split(self.pyqt_sip_flags)  # use same SIP flags as for PyQt5
        cmd.append(source)
        self.spawn(cmd)
        
    def swig_sources (self, sources, extension=None):
        if not self.extensions:
            return

        # Add the local include directory to the include path
        if extension is not None:
            extension.extra_compile_args += ['-D', 'QT_CORE_LIB', '-D', 'QT_GUI_LIB', '-D', 'QT_WIDGETS_LIB', '-D', 'QT_SVG_LIB']
            extension.include_dirs += [self.qt_include_dir, self.inc_dir,
                            os.path.join(self.qt_include_dir, 'QtCore'),
                            os.path.join(self.qt_include_dir, 'QtGui'),
                            os.path.join(self.qt_include_dir, 'QtWidgets'),
                            os.path.join(self.qt_include_dir, 'QtSvg'),
                            self.module_inc_dir,
                            os.path.join(self.module_inc_dir, 'rdkit'),
                            os.path.join(self.module_inc_dir, 'cairo'),
                            ]
            extension.libraries += ['Qt5Core' + self.qt_libinfix,
                                    'Qt5Gui' + self.qt_libinfix,
                                    'Qt5Widgets' + self.qt_libinfix,
                                    'Qt5Svg' + self.qt_libinfix
                                   ]
            
            rdkit_libraries = ['Depictor', 'MolDraw2D', 'RDGeneral', 'SmilesParse',
                               'RDInchiLib', 'Inchi']
            if not sys.platform.startswith('win'):
                rdkit_libraries = ['RDKit' + lib for lib in rdkit_libraries]
            else:
                rdkit_libraries += ['GraphMol', 'RDGeometryLib', 'SubstructMatch', 'RingDecomposerLib', 'DataStructs', 'coordgen', 'ChemReactions', 'FileParsers', 'MolTransforms', 'EigenSolvers', 'freetype']
            extension.libraries += rdkit_libraries
            
            if sys.platform == 'win32':
                extension.library_dirs += [self.qtconfig.QT_INSTALL_LIBS,
                                       self.inc_dir, self._sip_output_dir()]
            elif sys.platform == 'darwin':
                extension.extra_compile_args += ['-F' + self.qtconfig.QT_INSTALL_LIBS,
                    '-std=c++11', '-stdlib=libc++', '-mmacosx-version-min=10.9']
                extension.extra_link_args += ['-F' + self.qtconfig.QT_INSTALL_LIBS,
                    '-mmacosx-version-min=10.9']
            elif sys.platform == 'linux':
                extension.extra_compile_args += ['-std=c++11']

        return super().swig_sources(sources, extension)
        
    def build_extension(self, ext):
        cppsources = [source for source in ext.sources if source.endswith(".cpp")]
        
        dir_util.mkpath(self.build_temp, dry_run=self.dry_run)

        # Run moc on all header files.
        for source in cppsources:
            header = source.replace(".cpp", ".h")
            if os.path.exists(header):
                moc_file = "moc_" + os.path.basename(header).replace(".h", ".cpp")
                out_file = os.path.join(self.build_temp, moc_file)
                
                if newer(header, out_file) or self.force:
                    call_arg = ["moc", "-o", out_file, header]
                    spawn.spawn(call_arg, dry_run=self.dry_run)
                    
                if os.path.getsize(out_file) > 0:
                    ext.sources.append(out_file)

        # Add the temp build directory to include path, for compiler to find
        # the created .moc files
        ext.include_dirs += [self._sip_output_dir()]
        
        sipdistutils.build_ext.build_extension(self, ext)

if IS_COMPILED:
    setup_requires = ["PyQt5"] if REQUIRE_PYQT else []
    ext_modules = [Extension(MODULE_NAME + ".NetworkView",
                             glob.glob("src/*.cpp") + 
                             [os.path.join("sip", "NetworkView.sip")])]
else:
    setup_requires = []
    ext_modules = []

install_requires = ["PyQt5"]
if sys.platform.startswith('win'):
    install_requires.append("pywin32")

with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()
    
setup(
    name = MODULE_NAME,
    author = "Nicolas Elie",
    author_email = "nicolas.elie@cnrs.fr",
    url = "https://github.com/metgem/PyQtNetworkView",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass({'build_ext': build_ext, }),
    description = "Qt Widget and Python bindings for visualisation of a network graph",
    long_description = LONG_DESCRIPTION,
    keywords = ["qt"],
    license = "GPLv3+",
    classifiers = ["Development Status :: 4 - Beta",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Environment :: Win32 (MS Windows)",
                   "Environment :: MacOS X",
                   "Environment :: X11 Applications :: Qt",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8"],
    ext_modules = ext_modules,
    packages = find_packages(),
    setup_requires = setup_requires,
    install_requires = install_requires,
    zip_safe=False
)
