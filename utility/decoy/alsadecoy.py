import platform

if platform.platform().startswith('Darwin'):
    import osascript
else:
    raise ImportError


class Mixer:
    """a decoy for alsaaudio on Raspbian"""
    def __init__(self, mode='PCM'):
        self._vol = 100
        self._mode = mode
        print('[WARNING] using alsaaudio decoy!')

    def getvolume(self):
        return self._vol

    def setvolume(self, v):
        self._vol = int(v)
        scr = 'set volume output volume ' + str(self._vol)
        osascript.osascript(scr)
