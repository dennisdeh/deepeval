from abc import ABC, abstractmethod
from typing import Optional, Dict
from guardrails.types import GuardType


class BaseDecorativeGuard(ABC):
    score: Optional[float] = None
    score_breakdown: Dict = None
    reason: Optional[str] = None
    success: Optional[bool] = None
    evaluation_model: Optional[str] = None
    error: Optional[str] = None
    guard_type: GuardType

    @property
    def __name__(self):
        return "Base Decorative Guard"


class BaseGuard(BaseDecorativeGuard):
    @abstractmethod
    def guard_input(self, input: str, *args, **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    async def a_guard_input(self, input: str, *args, **kwargs) -> float:
        raise NotImplementedError(
            f"Async execution for {self.__class__.__name__} not supported yet."
        )

    @abstractmethod
    def guard_response(self, input: str, *args, **kwargs) -> float:
        raise NotImplementedError

    @abstractmethod
    async def a_guard_response(self, input: str, *args, **kwargs) -> float:
        raise NotImplementedError(
            f"Async execution for {self.__class__.__name__} not supported yet."
        )

    @property
    def __name__(self):
        return "Base Guard"
