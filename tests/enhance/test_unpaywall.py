from annette.stages.enhance.unpaywall import UnpaywallEnhancer
from tests.enhance.test_enhancers import TestEnhancer


class TestUnpaywallEnhancer(TestEnhancer):
    enhancer_class = UnpaywallEnhancer
