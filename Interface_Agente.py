from abc import ABC, abstractmethod
from typing import Any, Tuple

class Agente(ABC):
    """ Interface para o Agente Autónomo. """

    @abstractmethod
    def observacao(self, obs: Any):
        pass

    @abstractmethod
    def age(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self, recompensa: float):
        pass