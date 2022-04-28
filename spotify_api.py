import requests
import os
import uuid
from settings import IMG_DIRECTORY


class SpotifyApi:
    def __init__(self):
        self.header_api_host = "spotify23.p.rapidapi.com"
        self.header_api_key = "f6250cb747msh480c4d13cc9923ap12c595jsn68a406f337ff"

    def search(self, track_name):
        split_track_name = track_name.split("-")
        artist = split_track_name[0].strip()
        track = split_track_name[1].strip()
        headers = {
            "X-RapidAPI-Host": self.header_api_host,
            "X-RapidAPI-Key": self.header_api_key
        }
        url = f"https://spotify23.p.rapidapi.com/search/?q=artist:{artist}+track:{track}&type=tracks&numberOfTopResults=1"

        search_result = requests.get(url, headers=headers)
        if search_result.status_code != 200:
            raise ValueError("Неудалось найти трек")
        search_json = search_result.json()
        if search_json["tracks"]["totalCount"] == 0:
            raise ValueError("Неудалось найти трек")
        track = search_json["tracks"]["items"][0]
        track_id = track["data"]["id"]
        return self.get_track(track_id)

    def get_track(self, id):
        headers = {
            "X-RapidAPI-Host": self.header_api_host,
            "X-RapidAPI-Key": self.header_api_key
        }
        url = f"https://spotify23.p.rapidapi.com/tracks/?ids={id}"
        track = requests.get(url, headers=headers)
        if track.status_code != 200:
            raise ValueError("Неудалось найти трек")
        track_json = track.json()
        track = track_json["tracks"][0]
        img_url = track["album"]["images"][1]["url"]
        track_url = track["external_urls"]["spotify"]
        try:
            img_name = self.save_image(img_url)
            return img_name, track_url
        except ValueError as error:
            raise error

    def save_image(self, img_url):
        name = f"{uuid.uuid4()}.png"
        img = requests.get(img_url)
        if img.status_code != 200:
            raise ValueError("Неудалось найти картинку")
        with open(f"{IMG_DIRECTORY}/{name}", "wb") as file:
            file.write(img.content)
        return name
