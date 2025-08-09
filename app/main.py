from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self,
                 min_value: int,
                 max_value: int
                 ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self,
                     owner: type,
                     name: str
                     ) -> None:
        self.protected_name = "_" + name

    def __get__(self,
                instance: "Visitor",
                owner: type
                ) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self,
                instance: "Visitor",
                value: int
                ) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not range(self.min_value <= value <= self.max_value):
            raise ValueError(f"Value must be between {self.min_value} "
                             f"and {self.max_value}")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (ValueError, TypeError):
            return False
        return True
