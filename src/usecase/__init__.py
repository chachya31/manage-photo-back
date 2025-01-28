from abc import abstractmethod
from typing import Any


class Usecase:
    """
    Usecase base class
    """

    @abstractmethod
    def execute(self, *args: Any):
        """
        execute single usecase
        """
        raise NotImplementedError("must override usecase execute")  # pragma: no cover
