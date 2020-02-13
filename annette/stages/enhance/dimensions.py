import time
from datetime import datetime as dt, timedelta

import requests

from annette.db.models import Metrics, RunLog
from ._base import BaseEnhancer


class DimensionsEnhancer(BaseEnhancer):
    def get_metadata(self, citation):
        # find any previous entries for this doi
        previous = self.session_manager.session.query(Metrics).filter(
            Metrics.doi == citation.doi).first()

        # Throttle query rate to comply with API terms of use
        time.sleep(1)
        url = f'https://metrics-api.dimensions.ai/doi/{citation.doi}'

        try:
            r = requests.get(url)
            if not r.ok:
                r.raise_for_status()
        except requests.HTTPError:
            return []

        row_values = {
            'times_cited': r.json()['times_cited'] or 0,
            'recent_citations': r.json()['recent_citations'] or 0,
            'relative_citation_ratio': r.json()['relative_citation_ratio'] or 0,
            'field_citation_ratio': r.json()['field_citation_ratio'] or 0,
            'doi': citation.doi
            }

        if previous is None:
            return [Metrics(**row_values)]
        else:
            changed = False
            for k, v in row_values.items():
                if str(getattr(previous, k)) == str(v):
                    continue
                setattr(previous, k, v)
                changed = True
            return [previous] if changed else []

    @property
    def run_now(self):
        """
        Run every four weeks.
        :return:
        """
        last_run = self.session_manager.session.query(Metrics).join(RunLog).order_by(
            RunLog.end.desc()).first()
        if last_run is None:
            return True
        else:
            return last_run.log.end < (dt.now() - timedelta(weeks=4))
