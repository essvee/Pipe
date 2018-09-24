import dill as pickle
import pandas as pd
from sqlalchemy import create_engine


class Classifier:
    def __init__(self, records):
        self.dois = [i[0] for i in records]
        self.model = self.load_model()
        self.data = self.load_data()
        self.grouped_data = self.shape_data(self.data)

    def load_model(self):
        with open('src/model_forest.pk', 'rb') as f:
            loaded_forest = pickle.load(f)
        return loaded_forest

    def load_data(self):
        engine = create_engine('mysql+pymysql://root:r3ptar@localhost/pipe_db')
        df = pd.read_sql_table('vw_classifier', engine)
        return df

    def shape_data(self, df):
        df3 = df.drop_duplicates().copy()

        labels = ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5', 'Label_8']

        for l in labels:
            if l in df3.iloc[:, -1:].values:
                labels.remove(l)

        df4 = pd.get_dummies(df3, columns=['label_id'], prefix='L')

        for label in labels:
            df4[f"L_{label}"] = 0

        aggregations = {'nhm_sub': 'max',
                        'snippet_match': 'mean',
                        'highlight_length': 'mean',
                        'L_Label_1': 'max',
                        'L_Label_2': 'max',
                        'L_Label_3': 'max',
                        'L_Label_4': 'max',
                        'L_Label_5': 'max',
                        'L_Label_8': 'max'}

        grouped_data = df4.groupby(['doi']).agg(aggregations).reset_index()

        return grouped_data


    def classify(self):
        classification_sql = "UPDATE citation_store SET classification_id = %s WHERE doi = %s"
        preds = self.model.predict(self.grouped_data.iloc[:, 1:].values)

        self.grouped_data['classification_id'] = pd.Series(preds, index=self.grouped_data.index)
        results = list(zip(self.grouped_data.classification_id.astype(str), self.grouped_data.doi))

        return classification_sql, results

