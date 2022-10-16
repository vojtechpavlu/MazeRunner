"""Modul obsahuje definici algoritmu A Star (A*) pro prohledávání stavového
prostoru pomocí heuristické funkce.

Heuristická funkce je obecně taková, která dokáže algoritmu pomoci vybrat
(upřednostnit) některé operátory (resp. cesty) před jinými.
"""

from src.algorithms.algorithm import Algorithm
from src.state_space import StateSpace, State


class AStar(Algorithm):
    """Algoritmus A* je jedním z nejpopulárnějších heuristických algoritmů,
    které dokáží prohledávat graf co do cest vedoucích do cílových uzlů.

    Jeho síla je v heuristické funkci, která dokáže zholednit nejen přiblížení
    se cíli aplikací příslušného operátoru, ale i ceny doposud použitých
    operátorů.

    To je v rámci této třídy reprezentováno dvěma metodami:

        - statická metoda `g(State) -> int`, která vrací cenu cesty k dodanému
          uzlu. V aktuálním pojetí tuto chápe jako počet operátorů, které byly
          na tuto cestu aplikovány.

        - instanční metoda `h(State) -> float`, která vrací dolní odhad ceny
          cesty k cílovému stavu. Ten je v aktuálním pojetí počítán jako
          euklidovská vzdálenost mezi souřadnicemi dodaného uzlu a souřadnicemi
          uzlu cílového (viz využití Pythagorovy věty pro výpočet vzdálenosti
          dvou bodů ve 2D prostoru).

    Teoreticky lze ale pro výpočet dolního odhadu použít libovolné metriky.
    """

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("A*", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Pro algoritmus vyžaduje výběr nejlevnější cesty vypočítané na
        základě skutečné cesty k dosažení daného stavu (g) a dolního odhadu
        ceny cesty k dosažení cíle.
        """
        cheapest = self.fringe[0]
        cheapest_price = self.h(cheapest) + self.g(cheapest)
        for state in self.fringe:
            price = self.h(state) + self.g(state)
            if price < cheapest_price:
                cheapest = state

        self._fringe.remove(cheapest)
        return cheapest

    def h(self, state: State) -> float:
        """Metoda počítá dolní odhad ceny k dosažení cílového stavu. V našem
        pojetí si vystačíme s euklidovskou vzdáleností mezi dodaným a cílovým
        stavem."""
        # Souřadnice aktuálního políčka
        curr_x, curr_y = state.field.xy

        # Souřadnice cílového políčka
        fin_x, fin_y = self.state_space.final_state.field.xy

        # a^2 + b^2 = c^2, resp. (a^2 + b^2)^(1/2) = c
        return (((fin_x - curr_x) ** 2) + ((fin_y - curr_y) ** 2)) ** 0.5

    def run(self) -> State:
        """Implementace algoritmu A*.

        Algoritmus je jakousi anabází na prohledávání do šířky, přičemž však
        nevybírá další stavy k prohledání ze seznamu fringe jako z fronty,
        nýbrž si vybírá ten, který je nejvýhodnější - co do délky cesty k
        danému stavu, tak i co do odhadu cesty k cíli.
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

    @staticmethod
    def g(state: State) -> int:
        """Metoda počítá cenu cesty, kolik stálo dostat se do daného stavu.

        V tomto pojetí je tato hodnota spočítána prostě jen jako počet
        operátorů, kterých bylo třeba aplikovat pro tento stav. Důvodem je
        fakt, že cena operátoru je pro nás vždy roven 1.
        """
        return len(state.whole_path)
