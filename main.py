from pysat.card import EncType

from utils import power_set
from solver import SugarRush
from examples.langford import langford, print_langford_solution
from examples.parity_board import parity_board
from examples.assignment import interval_selection

def power_set_literals(lits):
    for subset in power_set(lits):
        yield [lit if lit in subset else -lit for lit in lits]
        #yield [1 if lit in subset else 0 for lit in lits]

def enumeration_test(solver, variables):
    satisfying_assignments = []
    unsatisfying_assignments = []
    for lits in power_set_literals(variables):
        res = solver.solve(assumptions=lits)
        bin_lits = [1 if lit > 0 else 0 for lit in lits]
        if res:
            satisfying_assignments.append(tuple(bin_lits))
        else:
            unsatisfying_assignments.append(tuple(bin_lits))

    print("Satisfying assignments:")
    #[print(lits) for lits in sorted(satisfying_assignments)]
    print(set([sum(lits) for lits in satisfying_assignments]))
    print()
    #print("False positives:")
    #[print(lits) for lits in sorted(satisfying_assignments) if sum(lits[:3]) < 2]
    
    print("Unsatisfying assignments:")
    print(set([sum(lits) for lits in unsatisfying_assignments]))
    #[print(lits) for lits in sorted(unsatisfying_assignments)]

def langford_test(n):
    with SugarRush() as solver:
        X = langford(solver, n)

        print("n:", n)
        solver.print_stats()

        satisfiable = solver.solve()
        print("Satisfiable:", satisfiable)
        if not satisfiable:
            return

        print_langford_solution(solver, X)

def negate_test():
    n = 3
    solver = SugarRush()
    X = [solver.var() for _ in range(n)]
    bound_X = solver.atmost(X, bound=2)
    bound_X_neg = solver.negate(bound_X)
    solver.add(bound_X_neg)
    #enumeration_test(solver, X)
    enumeration_test(solver, list(sorted(solver.lits - set([0]))))
    
def disjunction_test():
    n = 10
    solver = SugarRush()
    X = [solver.var() for _ in range(n)]

    bounds_even = [solver.equals(X, k) for k in range(0, n+1, 2)]
    bound = solver.disjunction(bounds_even)

    solver.add(bound)
    enumeration_test(solver, X)

    ''' successful test
    bound_X_1 = solver.equals(X, bound=0)
    bound_X_2 = solver.equals(X, bound=3)
    bound_X_1or2 = solver.disjunction([bound_X_1, bound_X_2])
    print(bound_X_1)
    print()
    print(bound_X_2)
    print()
    print(bound_X_1or2)
    print()
    solver.add(bound_X_1or2)

    enumeration_test(solver, X)
    '''


def assignment_test():
    sequence = [1, 1, 1, 1, 0, 0]
    feasible = lambda x: len(x) >= 2 and len(x) <= 5
    coords = interval_selection(sequence, feasible)
    for coord in coords:
        print(coord)

def main():
    #langford_test(20)

    #negate_test()

    #disjunction_test()

    #parity_board()

    #assignment_test()

    pizza_test()

if __name__ == '__main__':
    main()