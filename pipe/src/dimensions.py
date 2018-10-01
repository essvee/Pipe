from datetime import date
from requests import HTTPError
import requests
import time


class Dimensions:
    def __init__(self, citation_dois):
        self.citation_dois = citation_dois
        self.date_retrieved = date.today().strftime('%Y-%m-%d')

    def get_citations(self):
        """
        Uses list of DOIs used to instantiate the class to query Dimensions
        and return metrics.
        :return: string sql_query + a list of tuples holding data retrieved from Dimensions
        """
        insert_sql = "INSERT INTO bibliometrics(times_cited, recent_citations, retrieved_date, " \
                     "relative_citation_ratio, field_citation_ratio, doi) " \
                     "VALUES(%s, %s, %s, %s, %s, %s)"

        results = []
        print("Checking impact metrics...")
        # For each DOI in list, retrieve citation metrics
        for doi in self.citation_dois:
            # Throttle query rate to comply with API terms of use
            time.sleep(1)
            url = f"https://metrics-api.dimensions.ai/doi/{doi[0]}"
            try:
                r = requests.get(url)
                r.raise_for_status()

                results.append((r.json()['times_cited'] or 0,
                                r.json()['recent_citations'] or 0,
                                self.date_retrieved,
                                r.json()['relative_citation_ratio'] or 0,
                                r.json()['field_citation_ratio'] or 0,
                                doi))
            # Skip over DOIs which aren't found
            except HTTPError:
                continue

        # Return
        print(f"Impact metrics found for {len(results)} DOIs.")
        print("")

        return insert_sql, results
