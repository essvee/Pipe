import dill as pickle


class Classifier:
    def __init__(self, citations):
        self.citations = citations
        self.model = self.load_model()

    def load_model(self):
        with open('model_forest.pk', 'rb') as f:
            loaded_forest = pickle.load(f)
        return loaded_forest

    def classify(self):
        # TODO implement this method
        pass

