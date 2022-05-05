cmake_minimum_required(VERSION 3.5)
project(qtmolecularnetwork LANGUAGES CXX VERSION ${VERSION_SHORT})
find_package(QT NAMES Qt6 Qt5 COMPONENTS Core REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} 5.5 COMPONENTS Core Gui Widgets Svg REQUIRED)
find_package(RDKit REQUIRED)

get_property(RDKIT_INCLUDE_DIRS TARGET RDKit::rdkit_base PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
get_property(RDKIT_LINK_LIBRARIES TARGET RDKit::rdkit_base PROPERTY INTERFACE_LINK_LIBRARIES)
message(STATUS "RDKit include dirs: ${RDKIT_INCLUDE_DIRS}")
include_directories(${RDKIT_INCLUDE_DIRS})

if (UNIX AND NOT APPLE)
    include_directories(${Qt${QT_VERSION_MAJOR}Gui_PRIVATE_INCLUDE_DIRS})
endif()
set(CMAKE_INCLUDE_CURRENT_DIR ON)
if(BUILD_STATIC)
    set(CMAKE_STATIC_LIBRARY_SUFFIX "_static${CMAKE_STATIC_LIBRARY_SUFFIX}")
endif()
set(qmn_SRCS
    edge.cpp
    mol_depiction.cpp
    networkscene.cpp
    node.cpp
    style.cpp
)
set(qmn_HEADERS
    config.h
    edge.h
    graphicsitem.h
    mol_depiction.h
    networkscene.h
    node.h
    style.h
)
add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")

if(BUILD_STATIC)
    add_library(qtmolecularnetwork STATIC ${qmn_SRCS} ${qmn_HEADERS})
    target_compile_definitions(qtmolecularnetwork PUBLIC QMN_STATIC)
else()
    add_library(qtmolecularnetwork SHARED ${qmn_SRCS} ${qmn_HEADERS})
    target_compile_definitions(qtmolecularnetwork PRIVATE QMN_SHARED_EXPORT)
endif()
list(JOIN CMAKE_SYSTEM_PREFIX_PATH "/lib;" LIBRARIES_PATH)
set(rdkit_lib_path "${LIBRARIES_PATH}/lib")
target_link_directories(qtmolecularnetwork PUBLIC ${LIBRARIES_PATH})
target_link_libraries(qtmolecularnetwork PUBLIC Qt${QT_VERSION_MAJOR}::Core 
                                           Qt${QT_VERSION_MAJOR}::Gui 
                                           Qt${QT_VERSION_MAJOR}::Widgets
                                           Qt${QT_VERSION_MAJOR}::Svg
                                           RDKit::rdkit_base
                                           ${RDKIT_LINK_LIBRARIES})
if (UNIX)
    target_link_libraries(qtmolecularnetwork PUBLIC RDKitDepictor RDKitMolDraw2D RDKitRDGeneral RDKitSmilesParse RDKitRDInchiLib RDKitInchi)
else()
    target_link_libraries(qtmolecularnetwork PUBLIC GenericGroups Depictor MolDraw2D RDGeneral SmilesParse RDInchiLib Inchi GraphMol RDGeometryLib SubstructMatch RingDecomposerLib DataStructs coordgen ChemReactions FileParsers MolTransforms EigenSolvers freetype)
endif()
set_target_properties(qtmolecularnetwork PROPERTIES
    AUTOMOC ON
    AUTORCC ON
    CXX_STANDARD 14
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    VERSION ${VERSION_SHORT}
    EXPORT_NAME "qtmolecularnetwork"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/lib"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/bin"
)
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "qtmolecularnetworkConfigVersion.cmake"
    VERSION ${VERSION_SHORT}
    COMPATIBILITY SameMajorVersion
)
install(FILES ${qmn_HEADERS}
    DESTINATION include/qtmolecularnetwork
    COMPONENT headers
)
install(FILES
    "${CMAKE_SOURCE_DIR}/LICENSE"
    DESTINATION license
    COMPONENT license
)
install(TARGETS qtmolecularnetwork
    EXPORT qmnTargets
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include
)

install(EXPORT qmnTargets
    FILE qmnTargets.cmake
    NAMESPACE qmn::
    DESTINATION lib/cmake/qtmolecularnetwork
)
install(FILES qtmolecularnetworkConfig.cmake "${CMAKE_CURRENT_BINARY_DIR}/qtmolecularnetworkConfigVersion.cmake"
    DESTINATION lib/cmake/qtmolecularnetwork
)

target_include_directories(qtmolecularnetwork PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
)
