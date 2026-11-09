add_executable(tasks_00_basic_select 00_basic_select.cpp library.cpp)
add_executable(tasks_01_metric_swap 01_metric_swap.cpp library.cpp)
add_executable(tasks_03_set_stack 03_set_stack.cpp)

set(TASK_TARGETS
    tasks_00_basic_select
    tasks_01_metric_swap
    tasks_03_set_stack
)

foreach(TARGET ${TASK_TARGETS})
    target_link_libraries(${TARGET} PRIVATE Eigen3::Eigen HQP::HQP hqp-tasks)
    target_include_directories(${TARGET} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    add_test(NAME test_${TARGET} COMMAND ${TARGET})
endforeach()
