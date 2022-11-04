from src.algorithms.algorithm import Success, Failure
from src.printer import print_maze
from src.state_space import StateSpace, State, Operator
from src.maze import load_maze

from src.algorithms import all_algorithms

import time


# Připrav si všechny operátory
operators = Operator.create_operators()

# Připrav si bludiště
maze = load_maze("maze_30x18.txt")

# Připrav si stavový prostor (operátory, počátek a cíl)
ss = StateSpace(operators, State(maze.start_field), State(maze.goal_field))

# Připrav si algoritmy
algorithms = all_algorithms(ss)

# Pro každý z algoritmů
for algo in algorithms:

    start = time.time_ns()
    final_state = None

    try:
        algo.run()

    except Success as s:
        end = time.time_ns()
        path = s.final_state.whole_path
        print_maze(
            maze.clone(),
            [state.field.xy for state in s.final_state.all_states][1:]
        )

        # Vypiš délku cesty a cestu
        print(f"{algo.algorithm_name}, Počet kroků: {len(path)}")
        print(f"Délka fringe a closed: {len(algo.fringe)}, {len(algo.closed)}")
        print(f"Nalezená cesta: {path}")
        print(f"Doba hledání cesty: {(end - start) / 10 ** 6} ms")
        print(100 * "-", "\n")

    except Failure as f:
        print_maze(
            maze.clone(),
            [state.field.xy for state in f.last_valid_state.all_states][1:]
        )
        print(f"{algo.algorithm_name}: {f}")

