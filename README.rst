===============
PyQtNetworkView
===============

C++ version (and Python wrapper) of widgets used for visualisation of graph in `MetGem`_


Build for Windows
-----------------

-  Download and install `Visual Studio Community 2017`_
-  Download and install `Qt Open Source`_
-  Download `SIP`
-  Launch a Qt terminal: `Qt 5.xx.x 64-bit for Desktop (MSVC 2017)`
-  Activate MSVC environment :

::

   > "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64


- Build and install SIP:

::

   > cd SIP_folder
   > python configure.py
   > nmake
   > nmake install

-  Build NetworkView:

::

   > cd NetworkView_folder
   > python configure.py
   > nmake


.. _MetGem: https://github.com/metgem
.. _Visual Studio Community 2017: https://www.visualstudio.com/fr/
.. _Qt Open Source: https://www.qt.io/
.. _SIP: https://riverbankcomputing.com/software/sip/intro/