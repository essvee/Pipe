from pygbif import species
from pipe.src.db_objects import Name, Taxonomy

class ResolveName:
    def __init__(self, names):
        self.names = names
        self.results = []

    def gbif_name_resolve(self):
        for name in self.names:

            # Get gbif-resolved name
            result = species.name_backbone(name=name.label)

            # Ignore any names which don't find a match
            if 'usageKey' in result:
                print(f"match for {name.label}: {result['scientificName']}")

                self.results.append(Taxonomy(usageKey=result['usageKey'],
                                             scientificName=result['usageKey'],
                                             canonicalName=result.get('canonicalName', None),
                                             rank=result.get('rank', None),
                                             status=result.get('status', None),
                                             kingdom=result.get('kingdom', None),
                                             phylum=result.get('phylum', None),
                                             order=result.get('order', None),
                                             family=result.get('family', None),
                                             species=result.get('species', None),
                                             genus=result.get('genus', None),
                                             kingdomKey=result.get('kingdomKey', None),
                                             phylumKey=result.get('phylumKey', None),
                                             classKey=result.get('classKey', None),
                                             orderKey=result.get('orderKey', None),
                                             familyKey=result.get('familyKey', None),
                                             genusKey=result.get('genusKey', None),
                                             speciesKey=result.get('speciesKey', None),
                                             class_name=result.get('class', None)
                                             ))
            else:
                print(f"No match for: {name.label}")
                continue

        return self.results
