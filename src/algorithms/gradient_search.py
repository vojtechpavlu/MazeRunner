"""
"""
from typing import Iterable

from src.algorithms.algorithm import Algorithm, Success, Failure
from src.state_space import StateSpace, State


class GradientSearch(Algorithm):
    """"""

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("Gradient Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Pro algoritmus vyžaduje výběr nejlevnější cesty vypočítané na
        základě skutečné cesty k dosažení daného stavu (g) a dolního odhadu
        ceny cesty k dosažení cíle.
        """
        cheapest = self.fringe[0]
        cheapest_price = self.lower_bound(cheapest)
        for state in self.fringe:
            price = self.lower_bound(state)
            if price < cheapest_price:
                cheapest = state

        self._fringe.remove(cheapest)
        return cheapest

    def lower_bound(self, state: State) -> float:
        """Metoda počítá dolní odhad ceny k dosažení cílového stavu. V našem
        pojetí si vystačíme s euklidovskou vzdáleností mezi dodaným a cílovým
        stavem."""
        # Souřadnice aktuálního políčka
        curr_x, curr_y = state.field.xy

        # Souřadnice cílového políčka
        fin_x, fin_y = self.state_space.final_state.field.xy

        # a^2 + b^2 = c^2, resp. (a^2 + b^2)^(1/2) = c
        return (((fin_x - curr_x) ** 2) + ((fin_y - curr_y) ** 2)) ** 0.5

    def run(self):
        """"""
        current_state = self.state_space.initial_state

        while True:

            if self.state_space.is_final_state(current_state):
                raise Success("Nalezen cíl!", current_state)

            cheapest = None
            for o in self.state_space.available_for_state(current_state):
                child = o.apply(current_state)
                if self.lower_bound(current_state) > self.lower_bound(child):
                    cheapest = child

            if not cheapest:
                raise Failure("Uvíznuto v lokálním minimu", current_state)
            else:
                current_state = cheapest
