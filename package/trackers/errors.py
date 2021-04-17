from .core import TrackerInterface


class UnsupportedTrackingNumber(Exception):
    """Raised when tracker does not support a given tracking number."""

    def __init__(self, tracker: TrackerInterface, num: str) -> None:
        super().__init__(f'{type(tracker)} does not support {num}')


class UnknownTrackingNumber(Exception):
    """Raised when tracker does not find information for a given tracking number."""

    def __init__(self, tracker: TrackerInterface, num: str) -> None:
        super().__init__(f'{type(tracker)}: no information found for {num}')
