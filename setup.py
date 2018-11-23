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
from PyQt5.QtCore import PYQT_CONFIGURATION

MAJOR = 0
MINOR = 2
MICRO = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
MODULE_NAME = "PyQtNetworkView"
SRC_PATH = MODULE_NAME

IS_COMPILED = True
if "--skip-build" in sys.argv:
    IS_COMPILED = False
    sys.argv.remove("--skip-build")


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
        else:
            self.data_dir = sys.prefix + '/share'
            self.lib_dir = sys.prefix + '/lib'
            

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
        self.pyqt_sip_dir = None
        self.pyqt_sip_flags = None
        self.sip_files_dir = None
        self.sip_inc_dir = None
        self.inc_dir = None
        self.pyconfig = HostPythonConfiguration()
        self.qtconfig = TargetQtConfiguration(self.qmake_bin)
        self.config = sipconfig.Configuration()    
        self.config.default_mod_dir = ("/usr/local/lib/python%i.%i/dist-packages" %
                                      (sys.version_info.major, sys.version_info.minor))
        
    def finalize_options (self):
        super().finalize_options()

        if not self.qt_include_dir:
            if sys.platform == 'darwin':
                self.qt_include_dir = self.qtconfig.QT_INSTALL_LIBS
            else:
                self.qt_include_dir = self.qtconfig.QT_INSTALL_HEADERS

        if not self.pyqt_sip_dir:
            self.pyqt_sip_dir = os.path.join(self.pyconfig.data_dir, 'sip', 'PyQt5')
            
        if not self.pyqt_sip_flags:
            self.pyqt_sip_flags = PYQT_CONFIGURATION.get('sip_flags', '')
            
        if not self.sip_files_dir:
            self.sip_files_dir = os.path.abspath(os.path.join(".", "sip"))
            
        if not self.sip_inc_dir:
            self.sip_inc_dir = self.pyconfig.venv_inc_dir
            
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
        return self.sip_bin or super()._find_sip()
        
    def _sip_compile(self, sip_bin, source, sbf): 
        cmd = [sip_bin]
        if hasattr(self, 'sip_opts'):
            cmd += self.sip_opts
        if hasattr(self, '_sip_sipfiles_dir'):
            cmd += ['-I', self._sip_sipfiles_dir()]
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
            extension.extra_compile_args += ['-D', 'QT_CORE_LIB', '-D', 'QT_GUI_LIB', '-D', 'QT_WIDGETS_LIB']
            extension.include_dirs += [self.qt_include_dir, self.inc_dir,
                              os.path.join(self.qt_include_dir, 'QtCore'),
                              os.path.join(self.qt_include_dir, 'QtGui'),
                              os.path.join(self.qt_include_dir, 'QtWidgets')]
            extension.libraries += ['Qt5Core','Qt5Gui','Qt5Widgets']
            
            
            if sys.platform == 'win32':
                extension.library_dirs += [self.qtconfig.QT_INSTALL_LIBS,
                                       self.inc_dir, self._sip_output_dir()]
            elif sys.platform == 'darwin':
                extension.extra_compile_args += ['-F' + self.qtconfig.QT_INSTALL_LIBS, '-std=c++11']
                extension.extra_link_args += ['-F' + self.qtconfig.QT_INSTALL_LIBS]
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

        
def git_version():
    '''Return the git revision as a string'''
    
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION
  

def get_version_info():
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('libmetgem/version.py'):
        # must be a source distribution, use existing version file
        try:
            from libmetgem.version import git_revision as GIT_REVISION
        except ImportError:
            raise ImportError("Unable to import git_revision. Try removing " \
                              "libmetgem/version.py and the build directory " \
                              "before building.")
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION
    

def write_version_py(filename=os.path.join(SRC_PATH, '_version.py')):
    cnt = ("# THIS FILE IS GENERATED FROM LIBMETGEM SETUP.PY\n\n"
           "short_version = '%(version)s'\n"
           "version = '%(version)s'\n"
           "full_version = '%(full_version)s'\n"
           "git_revision = '%(git_revision)s'\n"
           "release = %(isrelease)s\n"
           "if not release:\n"
           "    version = full_version\n"
           "IS_COMPILED = %(compiled)s\n")
    FULLVERSION, GIT_REVISION = get_version_info()

    with open(filename, 'w') as f:
        f.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED),
                       'compiled': bool(IS_COMPILED)})
  
if IS_COMPILED:
    setup_requires = ["PyQt5"]
    ext_modules = [Extension(MODULE_NAME + ".NetworkView",
                             glob.glob("src/*.cpp") + 
                             [os.path.join("sip", "NetworkView.sip")])]
else:
    setup_requires = []
    ext_modules = []

install_requires = ["PyQt5"]
if sys.platform.startswith('win'):
    install_requires.append("pywin32")
    

write_version_py(os.path.join(SRC_PATH, '_version.py'))
with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()
    
setup(
    name = MODULE_NAME,
    author = "Nicolas Elie",
    author_email = "nicolas.elie@cnrs.fr",
    url = "https://github.com/metgem/PyQtNetworkView",
    version = get_version_info()[0],
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
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7"],
    ext_modules = ext_modules,
    cmdclass = {
        'build_ext': build_ext,
    },
    packages = find_packages(),
    setup_requires = setup_requires,
    install_requires = install_requires,
    zip_safe=False
)
