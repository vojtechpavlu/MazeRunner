"""Tento modul obsahuje definici tzv. hladového algoritmu pro prohledávání
stavového prostoru.

Tento algoritmus je postaven na uspořádaném prohledávání grafu (bludiště) tak,
že privileguje větve, které se zdají být nejperspektivnější, tedy ty, které
vedou nejspíše k řešení. Toho dosahuje průbežným řazením stavů dle jejich
bonity (dle hodnoty heuristické funkce).

V tomto případě je použita jako heuristická funkce euklidovská vzdálenost.
"""

from src.algorithms.algorithm import Algorithm
from src.state_space import StateSpace, State


class GreedySearch(Algorithm):
    """Tato třída reprezentuje definici hladového algoritmu pro prohledávání.
    To stojí na principu hledání aktuálně nejvýhodnějšího následníka.

    Výhodou je směřování rovnou přímo k cíli, nevýhodou je časová a paměťová
    komplexita algoritmu.
    """

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("Greedy Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Vrací ten stav, který je z doposud uložených nejperspektivnější,
        tedy přibližuje k cíli nejvíce.
        """
        # Definice nejlevnějšího (předpokládáme první prvek)
        current_cheapest = self._fringe[0]
        current_price = self.__euclid(current_cheapest)

        # Pro každý prvek z uzlů nerozvinutých porovnej ceny - pokud je některý
        # výhodnější, než doposud určený nejlevnější, přenastav ho
        for state in self.fringe:
            states_price = self.__euclid(state)
            if states_price < current_price:
                current_cheapest = state
                current_price = states_price

        # Nalezený nejlevnější z fringe odstraň a vrať ho
        self._fringe.remove(current_cheapest)
        return current_cheapest

    def __euclid(self, state: State) -> float:
        """Tato pomocná privátní metoda slouží k výpočtu euklidovské
        vzdálenosti tohoto stavu (resp. políčka) od cíle.

        Přijímá k tomu aktuální stav, ze kterého získává souřadnice aktuálně
        prohledávaného políčka, které porovnává se souřadnicemi políčka cíle.
        """
        # Souřadnice aktuálního políčka
        curr_x, curr_y = state.field.xy

        # Souřadnice cílového políčka
        fin_x, fin_y = self.state_space.final_state.field.xy

        # a^2 + b^2 = c^2, resp. (a^2 + b^2)^(1/2) = c
        return (((fin_x - curr_x) ** 2) + ((fin_y - curr_y) ** 2)) ** 0.5
