from datetime import date
from requests import HTTPError
import requests
from pipe.src.db_objects import Access


class Unpaywall:
    def __init__(self, records):
        self.records = records
        self.date_retrieved = date.today()

    def get_access_data(self):
        """
        Uses list of DOIs used to instantiate the class to query Unpaywall
        and return metrics.
        :return: string sql_query + a list of tuples holding data retrieved from Unpaywall
        """

        results = []
        print("Checking access...")

        # For each DOI in list, retrieve access details
        for c in self.records:
            url = f"https://api.unpaywall.org/v2/{c.doi}?email=s.vincent@nhm.ac.uk"
            print(url)
            try:
                r = requests.get(url)
                r.raise_for_status()
                if r.json()['is_oa'] is True:
                    best_oa_location = r.json()['best_oa_location']
                    results.append(Access(best_oa_url=best_oa_location['url'] or None,
                                          updated_date=best_oa_location['updated'][:10] or r.json()['updated'][:10],
                                          retrieved_date=self.date_retrieved,
                                          pdf_url=best_oa_location['url_for_pdf'] or None,
                                          is_oa=True,
                                          doi=c.doi,
                                          doi_url=r.json()['doi_url'] or None,
                                          host_type=best_oa_location['host_type'] or None,
                                          version=best_oa_location['version'] or None))
                else:
                    results.append(Access(best_oa_url=None,
                                          updated_date=r.json()['updated'][:10] or None,
                                          retrieved_date=self.date_retrieved,
                                          pdf_url=None,
                                          is_oa=r.json()['is_oa'],
                                          doi=c.doi,
                                          doi_url=r.json()['doi_url'] or None,
                                          host_type=None,
                                          version=None))

            # Skip over DOIs which aren't found
            except HTTPError:
                continue

        print(f"Access data found for {len(results)} DOIs.")
        print("")

        return results
