import attr
from datetime import datetime
from uuid import uuid4
import pandas as pd

@attr.s
class Sequence:
    filename: str = attr.ib()
    date: datetime = attr.ib()
    lc_settings: pd.DataFrame = attr.ib()
    gradient: pd.DataFrame = attr.ib()
    comments: dict = attr.ib()
    samples: list = attr.ib()
    table: pd.DataFrame = attr.ib()
    batch_id: str = attr.ib(default=attr.Factory(lambda: str(uuid4())[:5].upper()))

    @property
    def run_time(self):
        df = self.table
        gradient = self.gradient
        dur = ((len(df[df['Sample Type'] != 'QC']) * (gradient['duration'].sum() / 60 + 30)) + (
                    len(df[df['Sample Type'] == 'QC']) * (15 + 30))) / 60.
        return dur

