from typing import List
from concurrent.futures import Executor, as_completed
from .core import PackageEvent, TrackerInterface
from .errors import UnsupportedTrackingNumber


class MultiTracker(TrackerInterface):
    def __init__(
            self,
            executor: Executor,
            tracker1: TrackerInterface,
            tracker2: TrackerInterface,
            *other_trackers: List[TrackerInterface]):
        self.__executor__ = executor
        self.__trackers__ = [tracker1, tracker2, *other_trackers]

    def supports(self, tracking_number: str) -> bool:
        return any(t.supports(tracking_number) for t in self.__trackers__)

    def track(self, tracking_number: str) -> List[PackageEvent]:
        if not self.supports(tracking_number):
            raise UnsupportedTrackingNumber(self, tracking_number)

        futures = as_completed([self.__executor__.submit(tracker.track, tracking_number)
                                for tracker in self.__trackers__
                                if tracker.supports(tracking_number)])

        # get first tracker's events
        unique_events = next(futures).result()

        # merge all other new events to the unique list of events
        for future in futures:
            for event in future.result():
                if not any(unique_event.is_same_as(event)
                           for unique_event in unique_events):
                    unique_events.append(event)

        # return merged events unique across different tracker results
        return sorted(
            unique_events,
            key=lambda e: e.event_datetime,
            reverse=True)
