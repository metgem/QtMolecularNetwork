#!/bin/sh

if [[ "$target_platform" == osx* ]]; then
    CXXFLAGS="${CXXFLAGS} -D_LIBCPP_DISABLE_AVAILABILITY"
fi

mkdir build
cd build

cmake ${CMAKE_ARGS} \
  -DCMAKE_PREFIX_PATH=${PREFIX} \
  -DCMAKE_INSTALL_PREFIX=${PREFIX} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_RPATH=${PREFIX}/lib \
  -DBUILD_STATIC=OFF \
  -DQMN_VERSION=${PKG_VERSION} \
  -D Python3_EXECUTABLE:FILEPATH=${PYTHON} \
  -D Python3_ROOT_DIR:PATH=${PREFIX} \
  ..
make install -j${CPU_COUNT}

