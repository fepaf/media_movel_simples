import requests

from datetime import datetime, timedelta

from .models import DailySummaryPrice

PRECISION = '1d'
HEADERS = {'User-Agent': '*'}
URL = '''https://mobile.mercadobitcoin.com.br/v4/{pair}/candle?\
from={start_timestamp}&to={end_timestamp}&precision={precision}'''
VALID_RANGES = [20, 50, 200]

class Utils:
    def __init__(self):
        self.url = URL

    def _make_url(self, pair: str, start_timestamp: int, end_timestamp: int, precision: str):
        url = URL.replace('{pair}', pair)
        url = url.replace('{start_timestamp}', str(start_timestamp))
        url = url.replace('{end_timestamp}', str(end_timestamp))
        url = url.replace('{precision}', str(precision))
        return url

    def _get_closes(self, pair: str, days_ago: int):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_ago)

        end_timestamp = int(datetime.timestamp(end_date))
        start_timestamp = int(datetime.timestamp(start_date))

        self.url = self._make_url(
            pair=pair,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            precision=PRECISION
        )

        response = requests.get(url=self.url, headers=HEADERS)
        response_json = response.json()

        return response_json

    def _calculate_mmss(self, candles):
        prefix_sum_array = [{'sum': 0}]
        
        for ind, candle in enumerate(candles, start=1):
            day_price = candle.get('close')
            timestamp = candle.get('timestamp')
            
            prefix_sum_array.append(
                {
                    'sum': prefix_sum_array[-1]['sum'] + day_price,
                    'price': day_price,
                    'timestamp': timestamp
                }
            )

            for day_range in VALID_RANGES:
                if ind >= day_range:
                    range_sum = prefix_sum_array[ind]['sum']
                    range_sum -= prefix_sum_array[ind-day_range]['sum']
                    prefix_sum_array[ind][f'mms_{day_range}'] = range_sum / day_range
        prefix_sum_array.pop(0)

        return prefix_sum_array

    def load_closes(self, pair: str, days_ago: int = 365):
        response_json = self._get_closes(pair, days_ago)
        
        candles = response_json.get('candles', {})

        mms_objects = self._calculate_mmss(candles)

        for candle in mms_objects:
            register = DailySummaryPrice(
                pair=pair,
                timestamp=candle.get('timestamp', None),
                mms_20=candle.get('mms_20', None),
                mms_50=candle.get('mms_50', None),
                mms_200=candle.get('mms_200', None),
            )
            register.save()
            print(register, datetime.fromtimestamp(candle.get('timestamp', None)))
