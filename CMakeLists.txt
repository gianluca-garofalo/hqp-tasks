cmake_minimum_required(VERSION 3.22)

project(hqp_tasks VERSION 0.1.0 DESCRIPTION "Stack of tasks for the HQP solver" LANGUAGES CXX)

option(HQP_TASKS_BUILD_PYTHON "Build the pyhqp_tasks Python module" OFF)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

find_package(Eigen3 3.4 REQUIRED NO_MODULE)

# The task layer only needs Eigen. It builds the (matrix, lower, upper, breaks)
# stack that hqp::HierarchicalQP::set_problem takes but never calls the solver,
# so only the tests depend on HQP.
add_library(hqp_tasks INTERFACE)
add_library(hqp_tasks::hqp_tasks ALIAS hqp_tasks)
target_include_directories(hqp_tasks INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
target_link_libraries(hqp_tasks INTERFACE Eigen3::Eigen)
target_compile_features(hqp_tasks INTERFACE cxx_std_20)

# Tests are only built when this is the top-level project, not when a
# dependent project (e.g. hqp-compare) pulls it in.
if(PROJECT_IS_TOP_LEVEL)
    include(CTest)
    if(BUILD_TESTING)
        add_subdirectory(tests)
    endif()
endif()

if(HQP_TASKS_BUILD_PYTHON)
    add_subdirectory(python)
endif()

install(TARGETS hqp_tasks EXPORT hqp_tasks_targets)
install(
    DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.hpp" PATTERN "*.tpp"
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/hqp_tasksConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
    ARCH_INDEPENDENT
)
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/hqp_tasksConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/hqp_tasksConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/cmake/hqp_tasks
)
install(
    FILES
        ${CMAKE_CURRENT_BINARY_DIR}/hqp_tasksConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/hqp_tasksConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/cmake/hqp_tasks
)
install(
    EXPORT hqp_tasks_targets
    FILE hqp_tasksTargets.cmake
    NAMESPACE hqp_tasks::
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/cmake/hqp_tasks
)
