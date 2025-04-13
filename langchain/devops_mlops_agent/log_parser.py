import pandas as pd
import json

def parse_logs(file):
    if file.name.endswith('.json'):
        logs = json.load(file)
        return pd.json_normalize(logs)
    elif file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.DataFrame([{"log": line.strip()} for line in file.readlines()])
