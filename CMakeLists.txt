cmake_minimum_required(VERSION 3.5)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules ${CMAKE_MODULE_PATH})

# By default, the version information is extracted from the git index. However,
# we can override this behavior by explicitly setting QMN_VERSION and
# skipping the git checks. This is useful for cases where this project is being
# used independently of its original git repo (e.g. vendored in another project)
if(NOT QMN_VERSION)
    include(GetGitRevisionDescription)
    git_describe(GitTagVersion --tags)
    string(REGEX REPLACE "^v([0-9]+)\\..*" "\\1" VERSION_MAJOR "${GitTagVersion}")
    string(REGEX REPLACE "^v[0-9]+\\.([0-9]+).*" "\\1" VERSION_MINOR "${GitTagVersion}")
    string(REGEX REPLACE "^v[0-9]+\\.[0-9]+\\.([0-9]+).*" "\\1" VERSION_PATCH "${GitTagVersion}")
    set(VERSION_SHORT "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")
else()
    string(REGEX MATCHALL "[\.]" VERSION_DOT_MATCHES ${QMN_VERSION})
    list(LENGTH VERSION_DOT_MATCHES VERSION_DOT_COUNT)
    if(VERSION_DOT_COUNT EQUAL 2)
        set(VERSION_SHORT ${QMN_VERSION})
    else()
        message(FATAL_ERROR "QMN_VERSION must be in major.minor.patch format, e.g. 3.8.1. Got ${QMN_VERSION}")
    endif()
endif()


project(QtMN LANGUAGES CXX VERSION ${VERSION_SHORT})

option(BUILD_STATIC "Build the static library" OFF)

if("${CMAKE_SIZEOF_VOID_P}" STREQUAL "4")
    set(qmn_PlatformDir "x86")
else()
    set(qmn_PlatformDir "x64")
endif()

add_subdirectory(src)
