from abc import ABC, abstractmethod
from typing import Tuple, Any


class Ambiente(ABC):
    """ Interface para o Ambiente de Simulação. """

    @abstractmethod
    def observacaoPara(self) -> Any:
        pass

    @abstractmethod
    def agir(self, accao: Tuple[int, int]) -> float:
        pass

    @abstractmethod
    def jogo_terminou(self) -> bool:
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def reset(self):
        pass