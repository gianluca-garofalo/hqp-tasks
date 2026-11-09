cmake_minimum_required(VERSION 3.22)
project(hqp-tasks VERSION 0.1.0 LANGUAGES CXX)

find_package(Eigen3 REQUIRED NO_MODULE)

add_library(hqp-tasks INTERFACE)
add_library(hqp-tasks::hqp-tasks ALIAS hqp-tasks)

target_include_directories(hqp-tasks INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_link_libraries(hqp-tasks INTERFACE Eigen3::Eigen HQP::HQP)
target_compile_features(hqp-tasks INTERFACE cxx_std_20)

if(BUILD_TESTING)
    add_subdirectory(tests)
endif()
