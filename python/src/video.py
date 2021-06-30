"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        self._flagged = False
        self._flagreason = ""

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flagged(self) -> bool:
        """Returns whether video is flagged."""
        return self._flagged

    @property
    def flagreason(self) -> str:
        """Returns reason for flagging the video."""
        return self._flagreason

    def flagvideo(self, flag_reason: str):
        self._flagged = True
        self._flagreason = flag_reason
        return self

    def allowvideo(self):
        self._flagged = False
        self._flagreason = ""
        return self
