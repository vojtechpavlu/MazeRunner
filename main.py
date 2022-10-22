
from src.state_space import StateSpace, State, Operator
from src.maze import load_maze
from src.algorithms.depth_first_search import DepthFirstSearch
from src.algorithms.breath_first_search import BreathFirstSearch
from src.algorithms.a_star import AStar


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
    AStar(ss)
]

# Pro každý z algoritmů
for algo in algorithms:

    # Spusť si algoritmus a získej cestu
    path = algo.run().whole_path

    # Vypiš délku cesty a cestu
    print(f"{algo.algorithm_name}, Počet kroků: {len(path)}")
    print(f"Délka fringe a closed: {len(algo.fringe)}, {len(algo.closed)}")
    print(f"Nalezená cesta: {path}")
    print(100*"-", "\n")

