import pandas as pd

def fetch_dataset(csv_path):
    df = pd.read_csv(csv_path)
    return df
