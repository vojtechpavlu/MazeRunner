from src.algorithms.random_algorithm import Random
from src.state_space import StateSpace, State, Operator
from src.maze import load_maze
from src.algorithms.depth_first_search import DepthFirstSearch
from src.algorithms.breath_first_search import BreathFirstSearch
from src.algorithms.a_star import AStar
import time


# Připrav si všechny operátory
operators = Operator.create_operators()

# Připrav si bludiště
maze = load_maze("maze_15x15.txt")

# Připrav si stavový prostor (operátory, počátek a cíl)
ss = StateSpace(operators, State(maze.start_field), State(maze.goal_field))

# Připrav si algoritmy
algorithms = [
    DepthFirstSearch(ss),
    BreathFirstSearch(ss),
    AStar(ss),
    Random(ss)
]

# Pro každý z algoritmů
for algo in algorithms:

    # Spusť časovač (v nanosekundách)
    start = time.time_ns()

    # Spusť si algoritmus a získej cestu
    final_state = algo.run()

    # Ukonči časovač (v nanosekundách)
    end = time.time_ns()

    # Nalezená cesta
    path = final_state.whole_path

    # Vypiš délku cesty a cestu
    print(f"{algo.algorithm_name}, Počet kroků: {len(path)}")
    print(f"Délka fringe a closed: {len(algo.fringe)}, {len(algo.closed)}")
    print(f"Nalezená cesta: {path}")
    print(f"Doba hledání cesty: {(end - start) / 10 ** 6} ms")
    print(100*"-", "\n")

