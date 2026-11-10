find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE PYBIND11_RESULT
    )
    if(NOT PYBIND11_RESULT EQUAL 0)
        message(FATAL_ERROR "pybind11 not found. Install it with: pip install pybind11")
    endif()
    find_package(pybind11 CONFIG REQUIRED)
endif()

pybind11_add_module(pyhqp_tasks pybind_tasks.cpp)
target_link_libraries(pyhqp_tasks PRIVATE hqp_tasks::hqp_tasks)

if(PROJECT_IS_TOP_LEVEL AND BUILD_TESTING)
    add_test(
        NAME test_pyhqp_tasks
        COMMAND ${Python_EXECUTABLE} -m pytest -q ${CMAKE_CURRENT_SOURCE_DIR}/test_pyhqp_tasks.py
    )
    set_tests_properties(test_pyhqp_tasks PROPERTIES
        ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:pyhqp_tasks>"
    )
endif()
