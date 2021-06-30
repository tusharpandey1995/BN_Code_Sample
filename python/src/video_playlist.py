"""A video playlist class."""
from video import Video

class Playlist:

    def __init__(self,playlistid: str,playlistname: str, videolist: list()):
        self._playlistid = playlistid
        self._playlistname = playlistname
        self._videolist = list((videolist))

    def __init__(self,playlistid: str,playlistname: str):
        self._playlistid = playlistid
        self._playlistname = playlistname
        self._videolist = []

    @property
    def playlistid(self) -> str:
        """Returns the id of the playlist."""
        return self._playlistid

    @property
    def playlistname(self) -> str:
        """Returns the name of the playlist."""
        return self._playlistname

    @property
    def videolist(self) -> []:
        """Returns the list of the videos added in the playlist."""
        return self._videolist

    def addvideo(self, video: Video):
        self._videolist.append(video)
        return self

    def removevideo(self, video: Video):
        self._videolist.remove(video)
        return self

    def clearplaylist(self):
        self._videolist.clear()
        return self