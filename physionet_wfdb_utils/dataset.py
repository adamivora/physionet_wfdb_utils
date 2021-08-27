from pathlib import Path

import numpy as np
import wfdb
from torch.utils.data import Dataset

from .annotation import annotations_to_categories
from .utils import read_wfdb_records


class WFDBDataset(Dataset):
    @staticmethod
    def download_database(database, directory):
        download_path = Path(directory, database.replace('/', '-'))
        print(f'Downloading database {database} to {download_path}...')
        wfdb.dl_database(database, download_path)
        print('Done.')

    def __init__(self, database, directory, download=True, channel=0, atr_extension='atr'):
        self.database = database
        self.directory = str(Path(directory, self.database))
        self.channel = channel
        self.atr_extension = atr_extension

        self.records = read_wfdb_records(self.directory)
        if not any(self.records) and download:
            WFDBDataset.download_database(self.database, directory)
            self.records = read_wfdb_records(self.directory)

    def __len__(self):
        return len(self.records)

    def __repr__(self):
        return f'WFDBDataset({self.database})'

    def __getitem__(self, item):
        if isinstance(item, slice):
            items = (self[i] for i in range(*item.indices(len(self))))
            return tuple(list(x) for x in zip(*items))

        record_path = str(Path(self.directory, self.records[item]))
        record = wfdb.rdrecord(record_path)

        fs = record.fs
        signal = record.p_signal[:, self.channel]

        try:
            annotation = wfdb.rdann(record_path, extension=self.atr_extension)
        except FileNotFoundError as e:
            print(e)
            return signal, [], fs

        beats = np.array(annotation.symbol)
        beats_samples = annotations_to_categories(beats, annotation.sample)

        return signal, beats_samples, fs

    def info(self, item):
        record_path = Path(self.directory, self.records[item])
        record = wfdb.rdrecord(record_path)
        return record.file_name[0]
