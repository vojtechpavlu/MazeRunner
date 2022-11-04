"""Modul obsahuje definici algoritmu Depth-First Search (DFS) pro prohledávání
stavového prostoru tzv. po větvích.
"""

from src.algorithms.algorithm import Algorithm
from src.state_space import StateSpace, State


class DepthFirstSearch(Algorithm):
    """Algoritmus DFS je slepým algoritmem pro prohledávání stavového prostoru.
    Na obecné úrovni tento algoritmus negarantuje nalezení řešení, natož pak
    optimálního.

    Při použití na problém prohledávání uzavřeného a konečného bludiště však
    řešení vždy najde (existuje-li nějaké), riziko suboptimality však trvá."""

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("Depth-First Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Implementace abstraktní metody předka.
        Tato implementace pro potřeby algoritmu DFS chápe seznam fringe jako
        zásobník (LIFO), bere tedy prvky z konce.
        """
        return self._fringe.pop()  # Bez indexu metoda pop bere poslední prvek
