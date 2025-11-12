# src/models.py

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Artist:
    """Класс артиста для примера работы с Elasticsearch."""
    artist_id: int
    name: str
    artist_biography: Optional[str] = None

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для передачи данных в Elasticsearch"""
        return {
            "artist_id": self.artist_id,
            "name": self.name,
            "artist_biography": self.artist_biography,
        }


# Набор тестовых данных пока нет базы
ARTISTS_DATA: List[Artist] = [
    Artist(artist_id=1, name="Adele", artist_biography="British singer and songwriter."),
    Artist(artist_id=2, name="Drake", artist_biography="Canadian rapper and producer."),
    Artist(artist_id=3, name="Eminem", artist_biography="American rapper, songwriter, and producer."),
    Artist(artist_id=4, name="Rihanna", artist_biography="Barbadian singer, actress, and businesswoman."),
    Artist(artist_id=5, name="The Weeknd", artist_biography="Canadian singer and record producer."),
]



# === GENRES ===
@dataclass
class Genre:
    genre_id: int
    name: str

    def to_dict(self) -> dict:
        return {"genre_id": self.genre_id, "name": self.name}


GENRES_DATA: List[Genre] = [
    Genre(genre_id=1, name="Pop"),
    Genre(genre_id=2, name="Hip-Hop"),
    Genre(genre_id=3, name="R&B"),
    Genre(genre_id=4, name="Rock"),
]


# === ALBUMS ===
@dataclass
class Album:
    album_id: int
    name: str
    release_date: Optional[str]
    cover_art_url: Optional[str]
    disc_count: Optional[int]
    f_key_artist_id: int
    f_key_genre_id: Optional[int]

    def to_dict(self) -> dict:
        return {
            "album_id": self.album_id,
            "name": self.name,
            "release_date": self.release_date,
            "cover_art_url": self.cover_art_url,
            "disc_count": self.disc_count,
            "f_key_artist_id": self.f_key_artist_id,
            "f_key_genre_id": self.f_key_genre_id,
        }


ALBUMS_DATA: List[Album] = [
    Album(album_id=1, name="25", release_date="2015-11-20", cover_art_url=None, disc_count=1, f_key_artist_id=1, f_key_genre_id=1),
    Album(album_id=2, name="Scorpion", release_date="2018-06-29", cover_art_url=None, disc_count=2, f_key_artist_id=2, f_key_genre_id=2),
    Album(album_id=3, name="Revival", release_date="2017-12-15", cover_art_url=None, disc_count=1, f_key_artist_id=3, f_key_genre_id=2),
    Album(album_id=4, name="Anti", release_date="2016-01-28", cover_art_url=None, disc_count=1, f_key_artist_id=4, f_key_genre_id=3),
]


# === SONGS ===
@dataclass
class Song:
    song_id: int
    name: str
    track_number_album: Optional[int]
    duration: int
    file_url: str
    f_key_artist_id: int
    f_key_album_id: int
    disc_number: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "song_id": self.song_id,
            "name": self.name,
            "track_number_album": self.track_number_album,
            "duration": self.duration,
            "file_url": self.file_url,
            "f_key_artist_id": self.f_key_artist_id,
            "f_key_album_id": self.f_key_album_id,
            "disc_number": self.disc_number,
        }


SONGS_DATA: List[Song] = [
    Song(song_id=1, name="Hello", track_number_album=1, duration=295, file_url="/music/adele_hello.mp3", f_key_artist_id=1, f_key_album_id=1),
    Song(song_id=2, name="Nice For What", track_number_album=3, duration=210, file_url="/music/drake_niceforwhat.mp3", f_key_artist_id=2, f_key_album_id=2),
    Song(song_id=3, name="River", track_number_album=5, duration=221, file_url="/music/eminem_river.mp3", f_key_artist_id=3, f_key_album_id=3),
    Song(song_id=4, name="Work", track_number_album=2, duration=219, file_url="/music/rihanna_work.mp3", f_key_artist_id=4, f_key_album_id=4),
]