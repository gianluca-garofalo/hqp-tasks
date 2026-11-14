# Notes for agents working on hqp-tasks

hqp-tasks builds hierarchical problems one task at a time, for the HQP solver
([Weighted-Hierarchical-QP](https://github.com/gianluca-garofalo/Weighted-Hierarchical-QP)). It is header-only and
depends only on Eigen; HQP is needed only to solve the stack, and by the tests. This file is the handoff from the
sessions that set it up (November 2026).

## Map

| Path | What |
|---|---|
| `include/task/task.hpp`, `task.tpp` | `hqp::TaskBase`; `hqp::Task<Args...>`, a callback returning `(matrix, lower, upper)`, with an optional variable mask and weight, evaluated by `compute(args...)`; `hqp::bind_task<Args...>(f)`; `hqp::TaskPtr` (a `shared_ptr` with `cast<T>()`); `hqp::StackOfTasks`, whose `get_stack()` concatenates the tasks in priority order into `(A, lower, upper, breaks)` |
| `tests/` | `00_basic_select`, `01_metric_swap`, `02_set_stack` (with `02_set_stack_split.cpp`); `library.cpp`/`.hpp` check that `task.hpp` links when included from several files |
| `python/` | `pyhqp_tasks` (pybind11): `Task` and `StackOfTasks`; `task_example.py` uses it with the solver's `pyhqp` |
| `cmake/hqp_tasksConfig.cmake.in` | The installed package: `find_package(hqp_tasks)`, target `hqp_tasks::hqp_tasks` |

## Build and test

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build && ctest --test-dir build   # 3 tests
cmake -S . -B build -DFETCHCONTENT_SOURCE_DIR_HQP=/path/to/Weighted-Hierarchical-QP             # local solver
cmake -S . -B build -DHQP_TASKS_BUILD_PYTHON=ON      # needs pybind11, numpy and pytest
```

- **HQP:** the tests use an installed HQP when CMake finds one (`CMAKE_PREFIX_PATH`). Otherwise they fetch
  Weighted-Hierarchical-QP at `HQP_GIT_TAG`, `main` by default, so a breaking change there breaks this repository's
  CI. Weighted-Hierarchical-QP's `downstream` CI job builds this repository against its own changes.
- **CI** (`.github/workflows/ci.yml`): gcc and clang, Debug and Release, and the Python module.

## History

- The stack of tasks lived in Weighted-Hierarchical-QP until its split (Weighted-Hierarchical-QP#9). Its history
  was grafted here.
- #1 made this repository build on its own:
  - the library depends only on Eigen, and installs `hqp_tasks::hqp_tasks`;
  - `task.hpp` became safe to include from more than one file (it used to fail to link with multiple-definition
    errors);
  - the `Task`/`StackOfTasks` Python bindings moved here from `pyhqp` as `pyhqp_tasks`;
  - CI was added.

## Open

- **Pin HQP:** once Weighted-Hierarchical-QP tags `v2.0.0` (its issue #8), set `HQP_GIT_TAG` to that tag, and tag a
  release here if downstream users should pin it too.
- **hlq:** [hlq](https://github.com/gianluca-garofalo/hlq) is HQP's successor. Its
  `Solver::set_problem(A, lower, upper, level_ends)` takes the same `(A, lower, upper, breaks)` that `get_stack()`
  returns: level ends, not starts. Building stacks for hlq needs no change to this library, but the tests, the
  example and the README only use HQP.

## Conventions

- **Commits and PR titles:** `type> description.`, lowercase, imperative, with a final period (`feat`, `fix`,
  `chore`, `docs`, `test`, `ci`).
- **Every fix comes with a test** that fails without it.
- **No AI attribution:** no `Co-Authored-By`/session trailers, and no model names, in commits, code or PRs.
- **Branches and merging:** work on a branch and open a PR; never merge without the owner's explicit go-ahead.
- **PR descriptions:** keep them short: what changed, why, and how it was checked.
