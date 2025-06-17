import pandas as pd
from sklearn.ensemble import IsolationForest

def compute_threat_scores(df):
    if not {"source_ip", "event_type"}.issubset(df.columns):
        return None, "Log file must include 'source_ip' and 'event_type'."

    df_copy = df.copy()
    df_copy["source_ip"] = pd.factorize(df_copy["source_ip"])[0]
    df_copy["event_type"] = pd.factorize(df_copy["event_type"])[0]

    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    df_copy["threat_score"] = model.fit_predict(df_copy[["source_ip", "event_type"]])
    
    df["threat_score"] = df_copy["threat_score"].map({1: "Normal", -1: "Anomalous"})
    
    return df, None
