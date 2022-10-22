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

    def run(self) -> State:
        """Implementace algoritmu BFS.

        BFS se chápe fringe jako frontu, tedy získává vždy první přidaný prvek,
        který prohlašuje za aktuálně prohledávaný. Samotné prohledávání
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
