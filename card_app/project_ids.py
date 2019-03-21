import pandas as pd
import requests
from requests.auth import HTTPBasicAuth


def download_projectids(url, username, password):
    """Returns a list of project ids from project id from a 'Mann Department Projects' webpage."""
    r = requests.get(url, auth=HTTPBasicAuth(username, password))
    if not r.ok:
        r.raise_for_status()
    df = pd.read_html(r.text)[0]
    project_ids = df.values.flatten().tolist()
    return project_ids
