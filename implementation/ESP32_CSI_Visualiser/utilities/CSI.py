class CSIDATA:
    def __init__(self, amplitude, phase, timestamp):
        self.phase = phase
        self.amplitude = amplitude
        self.timestamp = timestamp

    def getAmplitude(self):
        return self.amplitude

    def getPhase(self):
        return self.phase

    def getTimeStamp(self):
        return self.timestamp