import re
from typing import List
from datetime import datetime
from requests import post
from bs4 import BeautifulSoup
from .utils import retry
from .core import PackageEvent, TrackerInterface
from .errors import UnsupportedTrackingNumber


class AlbanianPostTracker(TrackerInterface):

    __regex__ = re.compile('[A-Z]{2}[0-9]{9}[A-Z]{2}')

    @staticmethod
    @retry
    def __service_call__(tracking_number: str) -> str:
        url = 'https://gjurmo.postashqiptare.al/tracking.aspx'
        params = (
            ('__EVENTTARGET', ''),
            ('__EVENTARGUMENT', ''),
            ('__VIEWSTATE', '/wEPDwUKMTA5MDYxMDcyNmRkLoI0bv4OtYSs+SNHWAurZpro+shddZtGwTEJPz4YTKM='),
            ('__VIEWSTATEGENERATOR', '414E4794'),
            ('__EVENTVALIDATION', '/wEdAAVX79ubPRAUo7W5OXia5q+xs/foFj56M4JV9YiCGX9Oya9U1URXbQkTl8PXilbzpbKyuB7QXXlyP7hBJbH/uNLRemgLggfoCsFv2TROt6obiWaWX0R5eBUKjq7BF/x9MQlTdf3GqVq/aFEERDWyRKe2'),
            ('hBarCodes', tracking_number),
            ('txt_barcode', tracking_number),
            ('btn_track', 'Gjurmo/Submit'))
        with post(url, data=params) as response:
            return response.text

    def supports(self, tracking_number: str) -> bool:
        return self.__regex__.fullmatch(tracking_number)

    def track(self, tracking_number: str) -> List[PackageEvent]:
        if not self.supports(tracking_number):
            raise UnsupportedTrackingNumber(self, tracking_number)

        response = self.__service_call__(tracking_number)

        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find(id='gvTraking')
        if not table:
            return []

        return [
            PackageEvent
            (
                event_datetime=datetime.strptime(dt.text, '%d-%m-%Y %H:%M %p'),
                event_description=descr.text,
                is_delivery_event='Objekti u dorezua' in descr.text
            )
            for row in table.select("tr")[1:]
            for dt, descr, *_ in [row.select("td font")]
        ]
