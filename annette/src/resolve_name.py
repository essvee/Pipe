from datetime import date
from pygbif import species
from annette.db.models import Taxonomy


class ResolveName:
    def __init__(self, names):
        self.names = names
        self.taxonomy_results = []

    def gbif_name_resolve(self):
        for name in self.names:

            # Get gbif-resolved name
            result = species.name_lookup(q=name.label, limit=1)

            # Ignore any names which don't find a match (aka result is not empty)
            if result['results']:
                # Update Name with usageKey
                name.usage_key = result['results'][0]['key']

                # Create records for Taxonomy table
                self.taxonomy_results.append(Taxonomy(usageKey=result['results'][0]['key'],
                                             scientificName=result['results'][0].get('scientificName', None),
                                             canonicalName=result['results'][0].get('canonicalName', None),
                                             rank=result['results'][0].get('rank', None),
                                             status=result['results'][0].get('status', None),
                                             kingdom=result['results'][0].get('kingdom', None),
                                             phylum=result['results'][0].get('phylum', None),
                                             order=result['results'][0].get('order', None),
                                             family=result['results'][0].get('family', None),
                                             species=result['results'][0].get('species', None),
                                             genus=result['results'][0].get('genus', None),
                                             kingdomKey=result['results'][0].get('kingdomKey', None),
                                             phylumKey=result['results'][0].get('phylumKey', None),
                                             classKey=result['results'][0].get('classKey', None),
                                             orderKey=result['results'][0].get('orderKey', None),
                                             familyKey=result['results'][0].get('familyKey', None),
                                             genusKey=result['results'][0].get('genusKey', None),
                                             speciesKey=result['results'][0].get('speciesKey', None),
                                             class_name=result['results'][0].get('class', None),
                                             rundate=date.today())
                                             )
            else:
                print(f"No match for: {name.label}")
                continue

        return self.taxonomy_results, self.names
