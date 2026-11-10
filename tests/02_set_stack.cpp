#include <iostream>
#include <Eigen/Dense>
#include <hqp/hqp.hpp>
#include <task/task.hpp>

// Defined in 02_set_stack_split.cpp, a second translation unit that also
// includes task.hpp: linking the two checks that the header can be included
// from more than one file.
hqp::StackOfTasks split_into_stack(Eigen::MatrixXd const& matrix,
                                   Eigen::VectorXd const& lower,
                                   Eigen::VectorXd const& upper,
                                   Eigen::VectorXi const& breaks);

int main() {
    // -1 <= x <= 1;  x1+x2+x3 <= 1;  x1-x2 == 0.5;  10 <= 3*x1+x2-x3 <= 20
    Eigen::MatrixXd A(6, 3);
    A << 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, -1, 0, 3, 1, -1;
    Eigen::VectorXd lower(6), upper(6);
    lower << -1, -1, -1, -1e9, 0.5, 10;
    upper << 1, 1, 1, 1, 0.5, 20;
    Eigen::VectorXi breaks(4);
    breaks << 3, 4, 5, 6;

    auto stack = split_into_stack(A, lower, upper, breaks);
    auto [A2, lower2, upper2, breaks2] = stack.get_stack();
    bool roundTrip = stack.size() == 4 && A2 == A && lower2 == lower && upper2 == upper && breaks2 == breaks;

    hqp::HierarchicalQP solver(A2.rows(), A2.cols());
    solver.set_problem(A2, lower2, upper2, breaks2);
    Eigen::VectorXd solution = solver.get_primal();
    bool solved = solution.isApprox(Eigen::Vector3d(1, 0.5, -1));

    // Setting a stack with fewer levels replaces the old levels.
    stack.set_stack(A.topRows(4), lower.head(4), upper.head(4), Eigen::Vector2i(3, 4));
    bool resized = stack.size() == 2 && std::get<0>(stack.get_stack()).rows() == 4;

    std::cout << "round trip: " << roundTrip << ", solved: " << solved << " (" << solution.transpose()
              << "), resized: " << resized << std::endl;
    return roundTrip && solved && resized ? 0 : 1;
}
