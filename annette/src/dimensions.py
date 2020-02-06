from datetime import date
from annette.src.db_objects import Metric
from requests import HTTPError
import requests
import time
import logging


class Dimensions:
    def __init__(self, citation_dois):
        self.citation_dois = citation_dois
        self.date_retrieved = date.today()

    def get_citations(self):
        """
        Uses list of Citations to query Dimensions
        and return metrics.
        :return: List of Metric objects
        """

        results = []
        print(f"Checking impact metrics for {len(self.citation_dois)} citations...")
        # For each DOI in list, retrieve citation metrics
        no_result_found = 0

        for citation in self.citation_dois:

            # Throttle query rate to comply with API terms of use
            time.sleep(1)
            url = f"https://metrics-api.dimensions.ai/doi/{citation.doi}"
            print(url)

            try:
                r = requests.get(url)
                r.raise_for_status()

                results.append(Metric(times_cited=r.json()['times_cited'] or 0,
                                      recent_citations=r.json()['recent_citations'] or 0,
                                      retrieved_date=self.date_retrieved,
                                      relative_citation_ratio=r.json()['relative_citation_ratio'] or 0,
                                      field_citation_ratio=r.json()['field_citation_ratio'] or 0,
                                      doi=citation.doi))
            # Skip over DOIs which aren't found
            except HTTPError:
                no_result_found += 1
                continue

        logging.info(f"Impact metrics found for {len(results)} DOIs.")
        logging.info(f"Impact metrics not found for {no_result_found} DOIs.")

        return results
