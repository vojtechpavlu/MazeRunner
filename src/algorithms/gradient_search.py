"""Tento modul obsahuje definici algoritmu gradientního prohledávání stavového
prostoru. Algoritmus gradientního prohledávání je postaven na principu hledání
v každé následující interaci nejlepšího možného potomka.

Tím však může snadno skončit v lokálním extrému a nemusí dojít do svého cíle.
"""

from src.algorithms.algorithm import Algorithm, Success, Failure
from src.state_space import StateSpace, State


class GradientSearch(Algorithm):
    """Tato třída reprezentuje definici algoritmu gradientního prohledávání.
    Jde tedy o prohledávání hledajíce gradient zlepšení heuristické funkce v
    každé své iteraci.

    Mocný a snadný algoritmus však trpí problémem s uvíznutím v lokálním
    extrému, kdy již neexistuje východisko nalezení lepšího řešení.V kontextu
    bludiště pak tento algoritmus může snadno uvíznout ve slepé uličce, ze
    které již se vrátit nedokáže (hodnotu heuristické funkce by si zhoršil,
    resp. by se vzdálil od svého cíle).

    Jako heuristická funkce je zde použita euklidovská vzdálenost mezi aktuálně
    prohledávaným políčkem a tím cílovým."""

    def __init__(self, state_space: StateSpace):
        """Initor, který přijímá instanci stavového prostoru, v němž řešení
        bude hledat.
        """
        # Volání initoru předka, tedy Algorithm.__init__(str, StateSpace)
        super().__init__("Gradient Search", state_space)

    @property
    def get_from_fringe(self) -> State:
        """Získávání nejlepší další cesty je provedeno na principu hledání
        operátoru, který by v dané iteraci zajistil přiblížení cíli.

        Pokud takový operátor neexistuje, je vrácena hodnota None.
        """
        current_state = self._fringe.pop()
        cheapest = None
        for o in self.state_space.available_for_state(current_state):
            child = o.apply(current_state)
            if self.__euclid(current_state) > self.__euclid(child):
                cheapest = child
        return cheapest

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

    def run(self):
        """Samotná definice gradientního algoritmu pro prohledávání stavového
        prostoru.

        Algoritmus stojí na principu hledání největšího gradientu zlepšení,
        dle kterého volí své operároty.

        Jeho obrovskou slabinou je možnost uvíznutí v lokálním extrému, tedy
        jinými slovy kdy by jakýkoliv operátor hodnotu heuristické funkce
        jen zhoršil, leč v tomto bodě o cíl nejde.
        """

        # Jako počáteční uzel vyber první prvek z jednoprvkové fringe
        current_state = self.fringe[0]

        while True:

            # Pokud je daný stav cílem
            if self.state_space.is_final_state(current_state):
                raise Success("Nalezen cíl!", current_state)

            # Jinak vezmi nejlepšího následníka lepšího než aktuální stav
            cheapest = self.get_from_fringe

            # Pokud takový nebyl nalezen
            if not cheapest:
                raise Failure("Uvíznuto v lokálním minimu", current_state)

            # Pokud nalezen byl, uzavři aktuální stav, do jednoprvkové fringe
            # přidej aktuální zlepšující a nastav ho i jako aktuální
            # prohledávaný pro další iteraci
            else:
                self.close_state(current_state)
                self.remember_state(cheapest)
                current_state = cheapest
