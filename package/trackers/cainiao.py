import re
from typing import List
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from json import loads
from .utils import retry
from .core import PackageEvent, TrackerInterface
from .errors import UnsupportedTrackingNumber


class CainiaoTracker(TrackerInterface):

    __regex__ = re.compile('([A-Z]{2}[0-9]{9}[A-Z]{2}|[A-Z][0-9]{14})')

    @staticmethod
    @retry
    def __service_call__(tracking_number: str) -> str:
        url = 'https://global.cainiao.com/detail.htm'
        params = {'mailNoList': tracking_number}
        with get(url, params) as response:
            return response.text

    def supports(self, tracking_number: str) -> bool:
        return self.__regex__.fullmatch(tracking_number)

    def track(self, tracking_number: str) -> List[PackageEvent]:
        if not self.supports(tracking_number):
            raise UnsupportedTrackingNumber(self, tracking_number)

        response = self.__service_call__(tracking_number)

        soup = BeautifulSoup(response, 'html.parser')
        element = soup.find(id='waybill_list_val_box')
        if not element:
            return []

        json = loads(element.text)

        return [
            PackageEvent
            (
                event_datetime=datetime.fromisoformat(detail.get('time')),
                event_description=detail.get('desc'),
                is_delivery_event=(detail.get('status') == 'SIGNIN')
            )
            for data in json.get('data', [])
            for section in [data.get('section1', {}), data.get('section2', {})]
            for detail in section.get('detailList', [])
        ]
