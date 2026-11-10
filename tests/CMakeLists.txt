# The tests solve the stacks they build, so they need HQP. Use an installed HQP
# if there is one (set CMAKE_PREFIX_PATH), otherwise fetch it.
if(NOT TARGET HQP::HQP)
    find_package(HQP CONFIG QUIET)
    if(HQP_FOUND)
        message(STATUS "hqp_tasks tests: using HQP from ${HQP_DIR}")
    else()
        set(HQP_GIT_TAG "main" CACHE STRING "Weighted-Hierarchical-QP revision to fetch when HQP is not installed")
        include(FetchContent)
        FetchContent_Declare(HQP
            GIT_REPOSITORY "https://github.com/gianluca-garofalo/Weighted-Hierarchical-QP.git"
            GIT_TAG ${HQP_GIT_TAG}
        )
        FetchContent_MakeAvailable(HQP)
        message(STATUS "hqp_tasks tests: fetched HQP at ${HQP_GIT_TAG}")
    endif()
endif()

add_executable(00_basic_select 00_basic_select.cpp library.cpp)
add_executable(01_metric_swap 01_metric_swap.cpp library.cpp)
add_executable(02_set_stack 02_set_stack.cpp 02_set_stack_split.cpp)

foreach(TARGET 00_basic_select 01_metric_swap 02_set_stack)
    target_link_libraries(${TARGET} PRIVATE hqp_tasks::hqp_tasks HQP::HQP)
    target_include_directories(${TARGET} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    add_test(NAME test_${TARGET} COMMAND ${TARGET})
endforeach()
