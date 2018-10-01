from datetime import date
from requests import HTTPError
import requests


class Unpaywall:
    def __init__(self, citation_dois):
        self.citation_dois = citation_dois
        self.date_retrieved = date.today().strftime('%Y-%m-%d')

    def get_access_data(self):
        """
        Uses list of DOIs used to instantiate the class to query Unpaywall
        and return metrics.
        :return: string sql_query + a list of tuples holding data retrieved from Unpaywall
        """
        insert_sql = "INSERT INTO open_access(best_oa_url, updated_date, retrieved_date, " \
                     "pdf_url, is_oa, doi, doi_url, host_type, version) " \
                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        results = []
        print("Checking access...")

        # For each DOI in list, retrieve citation metrics
        for doi in self.citation_dois:
            url = f"https://api.unpaywall.org/v2/{doi[0]}?email=s.vincent@nhm.ac.uk"
            try:
                r = requests.get(url)
                r.raise_for_status()
                if r.json()['is_oa'] is True:
                    best_oa_location = r.json()['best_oa_location']
                    results.append((best_oa_location['url'] or None,
                                    best_oa_location['updated'][:10] or r.json()['updated'][:10],
                                    self.date_retrieved,
                                    best_oa_location['url_for_pdf'] or None,
                                    r.json()['is_oa'],
                                    doi[0],
                                    r.json()['doi_url'] or None,
                                    best_oa_location['host_type'] or None,
                                    best_oa_location['version'] or None
                                    ))
                else:
                    results.append((None,
                                    r.json()['updated'][:10] or None,
                                    self.date_retrieved,
                                    None,
                                    r.json()['is_oa'],
                                    doi[0],
                                    r.json()['doi_url'] or None,
                                    None,
                                    None
                                    ))

            # Skip over DOIs which aren't found
            except HTTPError:
                continue

        print(f"Access data found for {len(results)} DOIs.")
        print("")

        return insert_sql, results
