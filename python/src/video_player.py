"""A video player class."""

from video_library import VideoLibrary
from video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    currently_playing = None
    video_paused = False
    playlists = {}
    videodict = {}

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currently_playing = None
        self.video_paused = False
        self.playlists = {}
        for video in self._video_library.get_all_videos():
            self.videodict[video.video_id] = video


    def number_of_videos(self):
        num_videos = len(self.videodict.keys())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        """Returns all videos."""
        all_videos = {}
        for vid in self.videodict.keys():
            all_videos[self.videodict[vid].title] = self.videodict[vid]
        sortednames = sorted(all_videos.keys(), key=lambda x: x.lower())
        print("Here's a list of all available videos:")
        for vid in sortednames:
            if not all_videos[vid].flagged:
                print(all_videos[vid].title + ' (' + all_videos[vid].video_id + ') [' + (' '.join([tag for tag in all_videos[vid].tags if isinstance(tag, str)])) + ']')
            else:
                print(all_videos[vid].title + ' (' + all_videos[vid].video_id + ') [' + (
                    ' '.join([tag for tag in all_videos[vid].tags if isinstance(tag, str)])) + '] - FLAGGED (reason: ' + all_videos[vid].flagreason +")")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video and not video.flagged:
            if not self.currently_playing:
                self.currently_playing = video
                print('Playing video: ' + self.currently_playing.title)
                self.video_paused = False
            else:
                print('Stopping video: ' + self.currently_playing.title)
                self.currently_playing = video
                print('Playing video: ' + self.currently_playing.title)
                self.video_paused = False
        elif video and video.flagged:
            print("Cannot play video: Video is currently flagged (reason: " + video.flagreason + ")")
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if not self.currently_playing:
            print("Cannot stop video: No video is currently playing")
        else:
            print('Stopping video: ' + self.currently_playing.title)
            self.currently_playing = None
            self.video_paused = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = [key for key in self.videodict.keys()]
        if all_videos:
            vid = random.choice(all_videos)
            if not self.videodict[vid].flagged:
                self.play_video(self.videodict[vid].video_id)
            else:
                count = 0
                while(self.videodict[vid].flagged and count < len(list(all_videos))):
                    vid = random.choice(all_videos)
                    count+=1
                if not self.videodict[vid].flagged:
                    self.play_video(self.videodict[vid].video_id)
                else:
                    print("No videos available")

        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self.currently_playing and not self.video_paused:
            self.video_paused = True
            print("Pausing video: " + self.currently_playing.title)
        elif not self.currently_playing:
            self.video_paused = False
            print("Cannot pause video: No video is currently playing")
        else:
            print("Video already paused: " + self.currently_playing.title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.currently_playing and self.video_paused:
            self.video_paused = False
            print("Continuing video: " + self.currently_playing.title)
        elif not self.currently_playing:
            self.video_paused = False
            print("Cannot continue video: No video is currently playing")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.currently_playing:
            if self.video_paused:
                print("Currently playing: " + self.currently_playing.title + ' (' + self.currently_playing.video_id + ') [' + (' '.join([tag for tag in self.currently_playing.tags if isinstance(tag, str)])) + '] - PAUSED')
            else:
                print("Currently playing: " + self.currently_playing.title + ' (' + self.currently_playing.video_id + ') [' + (' '.join([tag for tag in self.currently_playing.tags if isinstance(tag, str)])) + ']')
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            playlist = Playlist(playlist_name.lower(),playlist_name)
            self.playlists[playlist.playlistid] = playlist
            print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() in self.playlists.keys():
            playlist = self.playlists.get(playlist_name.lower())
            video = self._video_library.get_video(video_id)
            if video and not video.flagged:
                if playlist.videolist:
                    if video in playlist.videolist:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        newplaylist = playlist.addvideo(video)
                        self.playlists.update(playlist_name = newplaylist)
                        print("Added video to " + playlist_name + ": " + video.title)
                else:
                    videolist = playlist.videolist.append(video)
                    self.playlists.update(playlist_name = playlist)
                    print("Added video to " + playlist_name + ": " + video.title)
            elif video and video.flagged:
                print("Cannot add video to my_playlist: Video is currently flagged (reason: " + video.flagreason + ")")
            else:
                print("Cannot add video to " + playlist_name + ": Video does not exist")
        else:
            print("Cannot add video to another_playlist: Playlist does not exist")


    def show_all_playlists(self):
        """Display all playlists."""
        if self.playlists:
            print("Showing all playlists:")
            sortednames = sorted(self.playlists.keys(), key=lambda x: x.lower())
            for name in sortednames:
                playlist = self.playlists.get(name)
                print(playlist.playlistname)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            playlist = self.playlists.get(playlist_name.lower())
            print("Showing playlist: " + playlist_name)
            if playlist.videolist:
                for video in playlist.videolist:
                    if not video.flagged:
                        print(video.title + ' (' + video.video_id + ') [' + (
                            ' '.join([tag for tag in video.tags if isinstance(tag, str)])) + ']')
                    else:
                        print(video.title + ' (' + video.video_id + ') [' + (
                            ' '.join([tag for tag in video.tags if
                                      isinstance(tag, str)])) + '] - FLAGGED (reason: ' + video.flagreason + ")")
            else:
                print("No videos here yet")
        else:
            print("Cannot show playlist "+ playlist_name +": Playlist does not exist")


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() in self.playlists.keys():
            playlist = self.playlists.get(playlist_name.lower())
            video = self._video_library.get_video(video_id)
            if video:
                if video in playlist.videolist:
                    newplaylist = playlist.removevideo(video)
                    self.playlists.update(playlist_name=newplaylist)
                    print("Removed video from " + playlist_name + ": " + video.title)
                else:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            playlist = self.playlists.get(playlist_name.lower())
            newplaylist = playlist.clearplaylist()
            self.playlists.update(playlist_name=newplaylist)
            print("Successfully removed all videos from " + playlist_name)
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() in self.playlists.keys():
            self.playlists.pop(playlist_name.lower())
            print("Deleted playlist: " + playlist_name)
        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        searchresults= {}
        counter = 0
        for name in sorted(self.videodict.keys(), key=lambda x: x.lower()):
            if search_term.lower() in name and not self.videodict[name].flagged:
                counter+=1
                searchresults[str(counter)] = self.videodict[name]
        if searchresults:
            print("Here are the results for " + search_term +":")
            for key,value in searchresults.items():
                print(key + ") " + value.title + ' (' + value.video_id + ') [' + (
                        ' '.join([tag for tag in value.tags if isinstance(tag, str)])) + ']')
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            command = input()
            if command in searchresults:
                self.play_video(searchresults[command].video_id)
        else:
            print("No search results for " + search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        searchresults = {}
        counter = 0
        for name in sorted(self.videodict.keys(), key=lambda x: x.lower()):
            if video_tag.lower() in self.videodict[name].tags and not self.videodict[name].flagged:
                counter+=1
                searchresults[str(counter)] = self.videodict[name]
        if searchresults:
            print("Here are the results for " + video_tag + ":")
            for key, value in searchresults.items():
                print(key + ") " + value.title + ' (' + value.video_id + ') [' + (
                    ' '.join([tag for tag in value.tags if isinstance(tag, str)])) + ']')
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            command = input()
            if command in searchresults:
                self.play_video(searchresults[command].video_id)
        else:
            print("No search results for " + video_tag)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if video_id in self.videodict.keys():
            if self.currently_playing:
                if str(self.currently_playing.video_id) == str(video_id):
                    self.stop_video()
            video = self.videodict[video_id]
            if not video.flagged:
                flaggedvideo = video.flagvideo(flag_reason)
                self.videodict.update(video_id = flaggedvideo)
                print("Successfully flagged video: "+ flaggedvideo.title + " (reason: " + flaggedvideo.flagreason + ")")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if video_id in self.videodict.keys():
            if self.currently_playing:
                if str(self.currently_playing.video_id) == str(video_id):
                    self.stop_video()
            video = self.videodict[video_id]
            if not video.flagged:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                allowedvideo = video.allowvideo()
                self.videodict.update(video_id=allowedvideo)
                print("Successfully removed flag from video: " + allowedvideo.title)
        else:
            print("Cannot remove flag from video: Video does not exist")
