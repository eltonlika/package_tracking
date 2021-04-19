from sys import argv
from concurrent.futures import ThreadPoolExecutor

from package.trackers.multi_tracker import MultiTracker
from package.trackers.cainiao import CainiaoTracker
from package.trackers.albanian_post import AlbanianPostTracker

from db import connect

db = connect("sqlite:///:memory:")


db.insert_package(tracking_number='RB069131513SG',
                  package_name='inner tubes',
                  last_checked=None)

db.insert_package(tracking_number='RB083371157SG',
                  package_name='usb-c hub',
                  last_checked=None)

db.insert_package(tracking_number='UA002876183FR',
                  package_name='dielectric',
                  last_checked=None)


def tracking_numbers():
    if len(argv) >= 2:
        for num in argv[1:]:
            yield (num, num)
        return

    for pkg in db.get_active_packages():
        yield (pkg['tracking_number'], pkg['package_name'])


def main():
    with ThreadPoolExecutor() as executor:
        tracker = MultiTracker(executor,
                               AlbanianPostTracker(),
                               CainiaoTracker())

        nums = [(num, name, executor.submit(tracker.track, num))
                for num, name in tracking_numbers()]

        for num, name, future in nums:
            print(f'[ {num} {name} ]')
            for e in future.result():
                print(e)
            print()


if __name__ == "__main__":
    main()
