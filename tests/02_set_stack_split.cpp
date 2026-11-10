#include <task/task.hpp>

hqp::StackOfTasks split_into_stack(Eigen::MatrixXd const& matrix,
                                   Eigen::VectorXd const& lower,
                                   Eigen::VectorXd const& upper,
                                   Eigen::VectorXi const& breaks) {
    hqp::StackOfTasks stack;
    stack.set_stack(matrix, lower, upper, breaks);
    return stack;
}
