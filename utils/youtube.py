import os
import requests
import re
from ytmusicapi import YTMusic
from pytube import YouTube as YTDownload
from .general import remove_punctuation, mkdir


def yt_get_query_string(song_name: str) -> bytes:
    return "+".join(song_name.split()).encode("utf-8")


def yt_query(video_title: str, all_ids: bool = False) -> str or None:
    query = yt_get_query_string(video_title)
    url = f"https://www.youtube.com/results?search_query={query}"
    html = requests.get(url)
    vid_ids = re.findall(r"watch\?v=(\S{11})", html.text)
    if len(vid_ids) == 0:
        return None
    return vid_ids if all_ids else vid_ids[0]


def yt_download_audio(vid_id: str, output_dir=os.getcwd(), filename=None, file_type='wav') -> str or None:
    yt_music = YTMusic()
    track = yt_music.get_song(videoId=vid_id)
    song_url = track['microformat']['microformatDataRenderer']['urlCanonical']
    vid = YTDownload(song_url)
    vid_audio = vid.streams.get_audio_only()
    if vid_audio is None: return None
    filename = track['videoDetails']['title'] if filename is None else filename
    filename = remove_punctuation(filename)
    output_dir = mkdir(output_dir)
    return vid_audio.download(output_path=output_dir, filename=f"{filename}.{file_type}"), track['videoDetails']['lengthSeconds']