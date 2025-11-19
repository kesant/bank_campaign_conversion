from Bank_Campaign_Conversion.utils.paths import data_raw_dir,models_dir
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import duckdb
import sklearn
from sklearn.feature_extraction import DictVectorizer#uses dictionaries DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle

print(f'pandas=={pd.__version__}')
print(f'numpy=={np.__version__}')
print(f'sklearn=={sklearn.__version__}')

def load_data():
    df=pd.read_csv(data_raw_dir("bank-full.csv"),sep=';')
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    categorical_columns = list(df.dtypes[df.dtypes == 'object'].index)

    for c in categorical_columns:
        df[c] = df[c].str.lower().str.replace(' ', '_')
    df.y = (df.y == 'yes').astype(int)
    print(f"dataset loaded")
    return df 
def train_model(df):
    numerical=["poutcome","month","contact"]
    categorical=["duration","pdays","balance","previous","age"]
    dv = DictVectorizer(sparse=False)
    train_dict = df[categorical + numerical].to_dict(orient='records')
    y_train=df.y.values
    pipeline = make_pipeline(
        DictVectorizer(),
        LogisticRegression(solver='liblinear')
    )
    pipeline.fit(train_dict, y_train)
    print(f"Model trained")
    return pipeline
def save_model(model):

    # Ruta donde quieres guardar el pipeline
    output_file = models_dir("logistic_regresion.pkl")

    # Guardar el pipeline usando pickle
    with open(output_file, 'wb') as f_out:
        pickle.dump(pipeline, f_out)

    print(f"Pipeline save in : {output_file}")
df=load_data()
pipeline=train_model(df)
save_model(pipeline)




