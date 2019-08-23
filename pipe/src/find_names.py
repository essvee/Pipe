from epitator.annodoc import AnnoDoc
from epitator.resolved_keyword_annotator import ResolvedKeywordAnnotator


class FindNames:
    def __init__(self, doi, title):
        self.title = title
        self.doi = doi

    def get_names(self):
        # Create tiers and return annotations relating to sp. names
        annotations = AnnoDoc(self.title).add_tiers(ResolvedKeywordAnnotator()).tiers["resolved_keywords"].spans

        result = []

        # Flatten annotations (can be > 1 per title), get useful metadata and return
        for a in annotations:
            entities = a.to_dict()['resolutions']
            result.extend([(self.doi, entity['entity']['label']) for entity in entities])

        # Return as set to get rid of duplicates + filter out empty results
        return list(filter(None, list(set(result))))

