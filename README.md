# NetworkView

C++ version (and Python wrapper) of widgets used for visualisation of graph in tsne-network.

# Build for Windows
1. Download and install [Visual Studio Community 2017](https://www.visualstudio.com/fr/)
2. Download and install [Qt Open Source](https://www.qt.io/)
3. Download [SIP](https://riverbankcomputing.com/software/sip/intro/)
4. Launch a Qt terminal: `Qt 5.10.1 64-bit for Desktop (MSVC 2017)`
5. > "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64
   > cd SIP_folder
   > python configure.py
   > nmake
   > nmake install
   > cd NetworkView_folder
   > python configure.py
   > nmake

