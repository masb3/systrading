import logging

import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DataMeta:
    source: str
    date_col_name: str
    price_col_name: str


class DataLoader(ABC):
    @abstractmethod
    def load_data(self, data_meta: DataMeta) -> pd.DataFrame:
        pass


class CSVLoader(DataLoader):
    def load_data(self, data_meta: DataMeta) -> pd.DataFrame:
        logger.info("Loading datasets ...")
        df = pd.read_csv(
            data_meta.source,
            parse_dates=[data_meta.date_col_name],
            index_col=data_meta.date_col_name,
        )
        df.sort_index(inplace=True)
        return df
