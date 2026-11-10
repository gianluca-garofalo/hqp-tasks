# HQP Tasks

Build hierarchical problems for the [HQP solver](https://github.com/gianluca-garofalo/Weighted-Hierarchical-QP) one task at a time.

A `hqp::Task` wraps a callback that returns a task's `(matrix, lower, upper)`, optionally with a mask that selects which variables the task acts on and a weight between its rows. A `hqp::StackOfTasks` orders tasks by priority and concatenates them into the `(matrix, lower, upper, breaks)` that `hqp::HierarchicalQP::set_problem` takes.

The library is header-only and depends only on Eigen. HQP itself is needed only to solve the stack, and by the tests.

## Usage

```cpp
#include <hqp/hqp.hpp>
#include <task/task.hpp>

// A0, lower0, upper0, A1, lower1, upper1: Eigen matrices and vectors
hqp::StackOfTasks stack(2);
stack[0] = hqp::bind_task([=] { return std::make_tuple(A0, lower0, upper0); });
stack[1] = hqp::bind_task<double>([=](double gain) {
    return std::make_tuple(A1, Eigen::VectorXd(gain * lower1), Eigen::VectorXd(gain * upper1));
});
stack[0].cast<hqp::Task<>>()->compute();
stack[1].cast<hqp::Task<double>>()->compute(0.5);

auto [A, lower, upper, breaks] = stack.get_stack();
hqp::HierarchicalQP solver(A.rows(), A.cols());
solver.set_problem(A, lower, upper, breaks);
Eigen::VectorXd x = solver.get_primal();
```

In CMake, after installing this repository:

```cmake
find_package(hqp_tasks CONFIG REQUIRED)
target_link_libraries(my_target PRIVATE hqp_tasks::hqp_tasks)
```

or without installing:

```cmake
include(FetchContent)
FetchContent_Declare(hqp_tasks GIT_REPOSITORY https://github.com/gianluca-garofalo/hqp-tasks.git GIT_TAG main)
FetchContent_MakeAvailable(hqp_tasks)
```

## Building and testing

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

The tests use an installed HQP when CMake finds one (point `CMAKE_PREFIX_PATH` at its prefix) and otherwise fetch Weighted-Hierarchical-QP at `HQP_GIT_TAG` (default `main`). To test against a local checkout of the solver, pass `-DFETCHCONTENT_SOURCE_DIR_HQP=/path/to/Weighted-Hierarchical-QP`.

## Python

`-DHQP_TASKS_BUILD_PYTHON=ON` builds the `pyhqp_tasks` module (needs `pip install pybind11 numpy pytest`), which provides `Task` and `StackOfTasks`. The solver itself is the `pyhqp` module from Weighted-Hierarchical-QP; `python/task_example.py` uses both.

## License

BSD 3-Clause License.
