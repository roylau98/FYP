from enum import Enum


class Filters(Enum):
    __order__ = "NONE BUTTERWORTH HAMPEL DWT_CA DWT_CD"
    NONE = "None"
    BUTTERWORTH = "Low Pass"
    HAMPEL = "Hampel"
    DWT_CA = "DWT (cA)"
    DWT_CD = "DWT (cD)"


class CSItype(Enum):
    __order__ = "AMPLITUDE PHASE"
    AMPLITUDE = "Amplitude"
    PHASE = "Phase"


class Graphtype(Enum):
    __order__ = "PLOT HEATMAP PCA"
    PLOT = "Plot"
    HEATMAP = "Heatmap"
    PCA = "PCA"

