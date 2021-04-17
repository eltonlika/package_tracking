from typing import List
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(eq=True, frozen=True)
class PackageEvent:
    event_datetime: datetime
    event_description: str
    is_delivery_event: bool

    def __is_same_time__(self, other: 'PackageEvent') -> bool:
        t1 = self.event_datetime.replace(second=0, microsecond=0)
        t2 = other.event_datetime.replace(second=0, microsecond=0)
        return t1 == t2

    def __is_same_description__(self, other: 'PackageEvent') -> bool:
        d1 = self.event_description.strip().upper()
        d2 = other.event_description.strip().upper()
        return d1 in d2 if len(d1) < len(d2) else d2 in d1

    def is_same_as(self, other: 'PackageEvent') -> bool:
        return isinstance(other, type(self)) \
            and self.is_delivery_event == other.is_delivery_event \
            and self.__is_same_time__(other) \
            and self.__is_same_description__(other)

    def __repr__(self) -> str:
        return f'{self.event_datetime.strftime("%Y-%m-%d %H:%M:%S")}  {self.event_description}'


class TrackerInterface(ABC):
    @abstractmethod
    def supports(self, tracking_number: str) -> bool:
        """Returns true if this tracker supports the given tracking number."""

    @abstractmethod
    def track(self, tracking_number: str) -> List[PackageEvent]:
        """Returns tracking events for given tracking number."""
