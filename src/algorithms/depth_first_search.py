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

    def run(self) -> State:
        """Implementace algoritmu DFS.

        DFS se chápe fringe jako zásobník, tedy získává vždy poslední přidaný
        prvek, který prohlašuje za aktuálně prohledávaný. Samotné prohledávání
        stojí na:

            - Otestování, zda-li není aktuální stav koncem
            - Otestování, zda-li již nebyl aktuální stav prohledáván
            - Přidáním všech svých potomků k prohledání v dalších iteracích.
              Získání potomků je dosaženo pomocí aplikace všech dostupných
              operátorů na aktuální stav. Pro konkrétní pravidla této filtrace
              se podívejte na metodu `StateSpace.available_for_state(State)`

        Pokud algoritmus prohledá všechny své stavy k prohledání a cíl nenajde,
        je vyhozena výjimka, neboť řešení není dosažitelné.

        Při přípravě instance předka (abstraktní třída Algorithm) je fringe
        opatřena úvodním stavem - kořenem.
        """
        while len(self.fringe) > 0:
            current_state = self.get_from_fringe
            if self.state_space.is_final_state(current_state):
                return current_state
            elif self.is_in_closed(current_state):
                continue
            else:
                for o in self.state_space.available_for_state(current_state):
                    self.remember_state(o.apply(current_state))
                self.close_state(current_state)

        raise Exception("Byly prohledány všechny dosažitelné stavy a nic...")
