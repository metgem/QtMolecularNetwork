#!/usr/bin/env python3
import inspect
import os
import sys
from pathlib import Path
from typing import List

import cmake_build_extension
import setuptools
from wheel.bdist_wheel import bdist_wheel

import PySide6
import shiboken6
import versioneer


class CustomCMakeExtension(cmake_build_extension.CMakeExtension):
    """XXX: Override CMakeExtension to support extra kwargs"""
    def __init__(
        self,
        name: str,
        install_prefix: str = "",
        disable_editable: bool = False,
        write_top_level_init: str = None,
        cmake_configure_options: List[str] = (),
        source_dir: str = str(Path(".").absolute()),
        cmake_build_type: str = "Release",
        cmake_component: str = None,
        cmake_depends_on: List[str] = (),
        expose_binaries: List[str] = (),
        cmake_generator: str = "Ninja",
        **kwargs
    ):
        setuptools.Extension.__init__(self, name=name, sources=[], **kwargs)

        if not Path(source_dir).is_absolute():
            source_dir = str(Path(".").absolute() / source_dir)

        if not Path(source_dir).absolute().is_dir():
            raise ValueError(f"Directory '{source_dir}' does not exist")

        self.install_prefix = install_prefix
        self.cmake_build_type = cmake_build_type
        self.disable_editable = disable_editable
        self.write_top_level_init = write_top_level_init
        self.cmake_depends_on = cmake_depends_on
        self.source_dir = str(Path(source_dir).absolute())
        self.cmake_configure_options = cmake_configure_options
        self.cmake_component = cmake_component
        self.expose_binaries = expose_binaries
        self.cmake_generator = cmake_generator


setuptools.setup(
    ext_modules=[
        CustomCMakeExtension(
            name="qmn",
            install_prefix="PySide6MolecularNetwork",
            source_dir=str(Path(__file__).parent.absolute() / "shiboken"),
            py_limited_api=True
        ),
    ],
    cmdclass=versioneer.get_cmdclass(
        {
            'build_ext': cmake_build_extension.BuildExtension,
            'bdist_wheel': bdist_wheel,
        }
    ),
    version=versioneer.get_version(),
)