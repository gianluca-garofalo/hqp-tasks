#!/usr/bin/env python3
"""
Example combining the HQP solver with the stack of tasks.

This example shows how to:
1. Use the solver directly with numpy arrays
2. Build hierarchical problems with StackOfTasks
3. Use the one-shot solve convenience function

It needs both Python modules on PYTHONPATH: pyhqp, built from
Weighted-Hierarchical-QP, and pyhqp_tasks, built from this repository.
"""

import numpy as np
import pyhqp
import pyhqp_tasks


def main():
    print("=== HQP Solver Example ===\n")

    # 1. Direct solver usage with numpy arrays
    print("1. Direct solver usage:")

    # Three priority levels for 2 variables:
    #   Level 0: -0.1 <= x <= 0.1   (bounds, 2 constraints)
    #   Level 1:  0.9 <= x1+x2 <= 1.1 (sum constraint)
    #   Level 2: -0.2 <= x1-x2 <= 0.2 (difference constraint)
    A = np.vstack([np.eye(2), [[1.0, 1.0]], [[1.0, -1.0]]])
    lower = np.array([-0.1, -0.1, 0.9, -0.2])
    upper = np.array([0.1, 0.1, 1.1, 0.2])
    breaks = np.array([2, 3, 4], dtype=np.int32)

    solver = pyhqp.HierarchicalQP(4, 2)
    solver.set_metric(np.eye(2))
    solver.set_problem(A, lower, upper, breaks)

    solution = solver.get_primal()
    print(f"   Solution: {solution}")

    slack_low, slack_up = solver.get_slack()
    print(f"   Slack (lower): {slack_low}")
    print(f"   Slack (upper): {slack_up}")

    # 2. Task-based usage with StackOfTasks
    print("\n2. Task-based hierarchical setup:")

    stack = pyhqp_tasks.StackOfTasks()
    stack.add(np.eye(2), np.array([-0.1, -0.1]), np.array([0.1, 0.1]))
    stack.add(np.array([[1.0, 1.0]]), np.array([0.9]), np.array([1.1]))
    stack.add(np.array([[1.0, -1.0]]), np.array([-0.2]), np.array([0.2]))
    print(f"   Stack: {stack}")

    A, lower, upper, breaks = stack.get_stack()
    print(f"   Stacked matrix shape: {A.shape}")
    print(f"   Break points: {breaks}")

    solver2 = pyhqp.HierarchicalQP(A.shape[0], A.shape[1])
    solver2.set_problem(A, lower, upper, breaks)
    solution2 = solver2.get_primal()
    print(f"   Solution: {solution2}")

    # 3. One-shot solve
    print("\n3. One-shot solve:")
    solution3 = pyhqp.solve(A, lower, upper, breaks)
    print(f"   Solution: {solution3}")

    # 4. Individual Task objects
    print("\n4. Task objects:")
    task = pyhqp_tasks.Task(np.eye(3), -np.ones(3), np.ones(3))
    print(f"   {task}")
    print(f"   Matrix:\n{task.matrix}")

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
