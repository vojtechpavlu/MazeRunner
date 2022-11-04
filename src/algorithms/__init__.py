"""Tento balíček obsahuje definice algoritmů, kterých lze použít pro
prohledávání grafů. Přesněji jich lze použít pro prohledávání stavového
prostoru reprezentujícího abstrakci nad bludištěm.
"""

from src.state_space import StateSpace

from .depth_first_search import DepthFirstSearch
from .breath_first_search import BreathFirstSearch
from .a_star import AStar
from .gradient_search import GradientSearch
from .greedy_search import GreedySearch
from .random_algorithm import Random
from .algorithm import Algorithm


def all_algorithms(state_space: StateSpace) -> tuple[Algorithm]:
    """Přístupová funkce, která vrací všechny implementované algoritmy
    uspořádané v ntici.

    K jejich vytvoření je však třeba získat referenci na stavový prostor,
    nad kterým má daný algoritmus být spuštěn.
    """
    return (
        DepthFirstSearch(state_space),
        BreathFirstSearch(state_space),
        AStar(state_space),
        GradientSearch(state_space),
        GreedySearch(state_space),
        Random(state_space),
    )
