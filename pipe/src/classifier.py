import dill as pickle
import os
import sklearn
import scipy
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
        df = pd.read_sql_table('vw_data', engine)
        return df

    def shape_data(self, df):
        df2 = df[['doi', 'nhm_sub', 'snippet_match', 'highlight_length',
                  'label_id']]
        df3 = df2.drop_duplicates().copy()
        df4 = pd.get_dummies(df3, columns=['label_id'], prefix='L')
        aggregations = {'nhm_sub': 'max',
                        'snippet_match': 'mean',
                        'highlight_length': 'mean',
                        'L_Label_1': 'max',
                        'L_Label_2': 'max',
                        'L_Label_3': 'max',
                        'L_Label_4': 'max',
                        'L_Label_5': 'max',
                        'L_Label_8': 'max'}

        return df4.groupby(['doi']).agg(aggregations).reset_index()

    def classify(self):
        classification_sql = "UPDATE citation_store SET classification_id = %s WHERE doi = %s"
        preds = self.model.predict(self.data)
        self.grouped_data['classification_id'] = pd.Series(preds, index=self.grouped_data.index)
        results = list(zip(self.grouped_data.classification_id, self.grouped_data.doi))

        return classification_sql, results

