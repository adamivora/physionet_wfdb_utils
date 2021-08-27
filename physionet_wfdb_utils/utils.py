from pathlib import Path
from pprint import pformat

from wfdb import Annotation, Record
from wfdb.processing import Comparitor


def pprint_repr(record):
    return type(record).__name__ + pformat(vars(record))


def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def set_pprint():
    Record.__repr__ = pprint_repr
    Annotation.__repr__ = pprint_repr
    Comparitor.__repr__ = pprint_repr


def read_wfdb_records(directory):
    prefix_len = len(directory)
    if not directory.endswith('/'):
        prefix_len += 1

    files = list(Path(directory).glob('*.hea'))
    files.extend(Path(directory).glob('*/*.hea'))
    files = [str(file)[prefix_len:] for file in files]

    records = [h.split('.hea')[0] for h in files]
    records.sort()

    return records
