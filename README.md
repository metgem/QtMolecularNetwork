# NetworkView

C++ version (and Python wrapper) of widgets used for visualisation of graph in tsne-network.

# Build for Windows
- Download and install [Visual Studio Community 2017](https://www.visualstudio.com/fr/)
- Download and install [Qt Open Source](https://www.qt.io/)
- Download [SIP](https://riverbankcomputing.com/software/sip/intro/)
- Launch a Qt terminal: `Qt 5.10.1 64-bit for Desktop (MSVC 2017)`
- Activate MSVC environment :

```
> "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64
```

- Build and install SIP:

```
> cd SIP_folder
> python configure.py
> nmake
> nmake install
```

- Build NetworkView:

```
> cd NetworkView_folder
> python configure.py
> nmake
```
