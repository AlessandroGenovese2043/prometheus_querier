import os

import requests

from lib.utils.logger import set_logger
from lib.utils.time import TimeUtils

logger = set_logger(__name__)


class Querier(object):
    def __init__(self):
        self.endpoint = os.environ.get("METRIC_ENDPOINT",
                                       "http://localhost:9090")

    def make_query_range(self, query, minute_ago=60, step='1m'):
        try:
            now_str = TimeUtils.format_rfc3339(TimeUtils.get_utc_now())
            ago_str = TimeUtils.get_past_time(minute_ago)
            resp = requests.get(
                # TODO prometheus specific
                url=f'{self.endpoint}/api/v1/query_range',
                params={
                    'query': query,
                    'start': ago_str,
                    'end': now_str,
                    'step': '1m'
                }
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise Exception('query failed: ' + data.get('error', ''))

            return data['data']['result']

        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {e}')
        except Exception as e:
            logger.error(f'Error: {e}')

    def make_query(self, query):
        try:
            resp = requests.get(
                url=f'{self.endpoint}/api/v1/query',
                params={'query': query}
            )
            resp.raise_for_status()
            data = resp.json()

            if data['status'] != 'success':
                raise Exception('query failed: ' + data.get('error', ''))

            return data['data']['result']

        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {e}')
        except Exception as e:
            logger.error(f'Error: {e}')
