"""Modul obsahuje definici algoritmu Breath-First Search (BFS) pro prohledávání
stavového prostoru tzv. po vrstvách.
"""

from src.algorithms.algorithm import Algorithm
from src.state_space import StateSpace, State


class BreathFirstSearch(Algorithm):
    """Algoritmus BFS je slepým algoritmem pro prohledávání stavového prostoru.
    Algoritmus garantuje nalezení řešení, existuje-li cílové."""

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("Breath-First Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Implementace abstraktní metody předka.
        Tato implementace pro potřeby algoritmu BFS chápe seznam fringe jako
        frontu (FIFO), bere tedy prvky ze začátku.
        """
        return self._fringe.pop(0)  # Index 0 značí první prvek z fringe
