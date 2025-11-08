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
