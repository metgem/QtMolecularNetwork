mkdir build
cd build
if errorlevel 1 exit 1

cmake -LAH -G"NMake Makefiles"                  ^
    -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%"      ^
    -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%"   ^
    -DCMAKE_BUILD_TYPE=Release                  ^
    -DBUILD_STATIC=OFF                          ^
    -DQMN_VERSION=%PKG_VERSION%                 ^
    -DPython3_FIND_STRATEGY=LOCATION           ^
    ..
if errorlevel 1 exit 1

cmake --build . --target install
if errorlevel 1 exit 1
