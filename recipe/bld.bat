mkdir build
cd build

cmake -LAH -G"NMake Makefiles"                               ^
    -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%"                   ^
    -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%"                ^
    -DCMAKE_BUILD_TYPE=Release                               ^
    -DBUILD_STATIC=OFF                                       ^
    -DQMN_VERSION=%PKG_VERSION%                              ^
    ..
if errorlevel 1 exit 1

cmake --build . --target install
if errorlevel 1 exit 1
