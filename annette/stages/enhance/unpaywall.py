import requests

from annette.db.models import Access
from ._base import BaseEnhancer


class UnpaywallEnhancer(BaseEnhancer):
    def get_metadata(self, citation):
        # find any previous entries for this doi
        previous = self.session_manager.session.query(Access).filter(
            Access.doi == citation.doi).first()

        url = f'https://api.unpaywall.org/v2/{citation.doi}?email=s.vincent@nhm.ac.uk'

        try:
            r = requests.get(url)
            if not r.ok:
                r.raise_for_status()
        except requests.HTTPError:
            return []

        is_open = r.json()['is_oa']
        best_oa_location = r.json()['best_oa_location'] if is_open else {}

        row_values = {
            'best_oa_url': best_oa_location.get('url', None),
            'updated_date': best_oa_location.get('updated', r.json().get('updated', ''))[:10],
            'pdf_url': best_oa_location.get('url_for_pdf', None),
            'is_oa': is_open,
            'doi': citation.doi,
            'host_type': best_oa_location.get('host_type', None),
            'version': best_oa_location.get('version', None)
            }

        if previous is None:
            return [Access(**row_values)]
        else:
            for k, v in row_values.items():
                setattr(previous, k, v)
            return [previous]
