from enum import Enum

import numpy as np

NORMAL_BEATS = {'N', 'L', 'R', 'B', '/', 'f', 'Q', '?'}
ATRIAL_BEATS = {'A', 'a', 'J', 'S', 'e', 'j', 'n'}
VENTRICULAR_BEATS = {'V', 'r', 'F', 'E'}
BEAT_ANNOTATIONS = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e',
                    'j', 'n', 'E', '/', 'P', 'f', 'Q', '?']


class BeatType(Enum):
    Unknown = -1
    Normal = 0
    Atrial = 1
    Ventricular = 2


BeatTypes = [BeatType.Normal, BeatType.Atrial, BeatType.Ventricular]


def annotation_to_category(annotation):
    if annotation in NORMAL_BEATS:
        return BeatType.Normal
    if annotation in ATRIAL_BEATS:
        return BeatType.Atrial
    if annotation in VENTRICULAR_BEATS:
        return BeatType.Ventricular
    return BeatType.Unknown


def annotations_to_categories(annotations, samples, ignore=[BeatType.Unknown]):
    categories = np.array([annotation_to_category(
        annotation).value for annotation in annotations])
    result = {}

    for beat_type in BeatType:
        if beat_type in ignore:
            continue
        beats_loc = np.where(categories == beat_type.value)
        beats_samples = samples[beats_loc]
        result[beat_type] = beats_samples

    return result
