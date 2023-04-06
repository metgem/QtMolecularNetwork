cmake_minimum_required(VERSION 3.5)
project(qtmolecularnetwork LANGUAGES CXX VERSION ${VERSION_SHORT})

find_package(QT NAMES Qt6 Qt5 COMPONENTS Core REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Core Gui Widgets Svg REQUIRED)
find_package(RDKit REQUIRED)
find_package(Cairo REQUIRED)

include(FindFreetype)
include_directories(${FREETYPE_INCLUDE_DIRS})

get_property(RDKIT_INCLUDE_DIRS TARGET RDKit::rdkit_base PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "RDKit include dirs: ${RDKIT_INCLUDE_DIRS}")
include_directories(${RDKIT_INCLUDE_DIRS})

set(RDKIT_LIBRARIES RDKit::rdkit_base RDKit::RDInchiLib RDKit::Depictor RDKit::SmilesParse RDKit::MolDraw2D)
set(RDKIT_LINK_LIBRARIES)
foreach(lib ${RDKIT_LIBRARIES})
    get_property(link_libraries TARGET ${lib} PROPERTY INTERFACE_LINK_LIBRARIES)
    list(APPEND RDKIT_LINK_LIBRARIES ${link_libraries})
endforeach()
message(STATUS "RDKit link libraries: ${RDKIT_LINK_LIBRARIES}")

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

set(library_name "qt${QT_VERSION_MAJOR}molecularnetwork")
if(BUILD_STATIC)
    add_library(${library_name} STATIC ${qmn_SRCS} ${qmn_HEADERS})
    target_compile_definitions(${library_name} PUBLIC QMN_STATIC)
else()
    add_library(${library_name} SHARED ${qmn_SRCS} ${qmn_HEADERS})
    target_compile_definitions(${library_name} PRIVATE QMN_SHARED_EXPORT)
endif()

target_compile_features(${library_name} PRIVATE cxx_std_17)

list(JOIN CMAKE_SYSTEM_PREFIX_PATH "/lib;" LIBRARIES_PATH)
target_link_directories(${library_name} PUBLIC ${LIBRARIES_PATH})
target_link_libraries(${library_name} PUBLIC Qt${QT_VERSION_MAJOR}::Core 
                                           Qt${QT_VERSION_MAJOR}::Gui 
                                           Qt${QT_VERSION_MAJOR}::Widgets
                                           Qt${QT_VERSION_MAJOR}::Svg
                                           ${CAIRO_LIBRARIES}
                                           ${FREETYPE_LIBRARIES}
                                           ${RDKIT_LIBRARIES}
                                           ${RDKIT_LINK_LIBRARIES})
set_target_properties(${library_name} PROPERTIES
    AUTOMOC ON
    AUTORCC ON
    CXX_STANDARD 14
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    VERSION ${VERSION_SHORT}
    EXPORT_NAME ${library_name}
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/lib"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${qmn_PlatformDir}/bin"
)
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${library_name}ConfigVersion.cmake"
    VERSION ${VERSION_SHORT}
    COMPATIBILITY SameMajorVersion
)
install(FILES ${qmn_HEADERS}
    DESTINATION include/${library_name}
    COMPONENT headers
)
install(TARGETS ${library_name}
    EXPORT qmnTargets
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include/${library_name}
)

install(EXPORT qmnTargets
    FILE qmnTargets.cmake
    NAMESPACE qmn::
    DESTINATION lib/cmake/${library_name}
)
install(FILES qtmolecularnetworkConfig.cmake RENAME ${library_name}Config.cmake
    DESTINATION lib/cmake/${library_name}
)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${library_name}ConfigVersion.cmake"
    DESTINATION lib/cmake/${library_name}
)

target_include_directories(${library_name} PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
)
