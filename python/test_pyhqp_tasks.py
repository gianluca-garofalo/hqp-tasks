import numpy as np
import pyhqp_tasks
import pytest


def make_stack():
    stack = pyhqp_tasks.StackOfTasks()
    stack.add(np.eye(2), np.array([-0.1, -0.1]), np.array([0.1, 0.1])).add(
        np.array([[1.0, 1.0]]), np.array([0.9]), np.array([1.1])
    )
    return stack


def test_get_stack_concatenates_levels():
    A, lower, upper, breaks = make_stack().get_stack()
    np.testing.assert_array_equal(A, [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    np.testing.assert_array_equal(lower, [-0.1, -0.1, 0.9])
    np.testing.assert_array_equal(upper, [0.1, 0.1, 1.1])
    np.testing.assert_array_equal(breaks, [2, 3])


def test_levels_are_indexable():
    stack = make_stack()
    assert len(stack) == 2
    np.testing.assert_array_equal(stack[1].matrix, [[1.0, 1.0]])
    with pytest.raises(IndexError):
        stack[2]


def test_task_holds_its_data():
    task = pyhqp_tasks.Task(np.eye(3), -np.ones(3), np.ones(3))
    assert repr(task) == "<Task 3x3>"
    np.testing.assert_array_equal(task.upper, np.ones(3))
