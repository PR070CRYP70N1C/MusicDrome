import os
from typing import List


class Config:
    def __init__(self):
        # Обязательные параметры без значений по умолчанию
        self.API_TOKEN = os.getenv("API_TOKEN")
        self.MUSIC_FOLDER = os.getenv("MUSIC_FOLDER", "/music")
        self.TMP_DIR = os.getenv("TMP_DIR", "/tmp")

        # Last.fm credentials
        self.LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
        self.LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET")

        # Опциональные параметры
        self.LOCAL_TELEGRAM_SERVER = os.getenv("LOCAL_TELEGRAM_SERVER", "http://localhost:9091")
        self.MUSIC_COMMENT = os.getenv("MUSIC_COMMENT", "https://t.me/LosslessRobot?start=_tgr_E5_6u11iMzNi")
        self.LOG_FILE = os.getenv("LOG_FILE", "/app/logs/app.log")

        # Параметры с преобразованием типа
        self.GENRES = os.getenv("GENRES", "rock,pop,jazz,electronic,hip hop,classical,metal,blues,reggae,folk").split(
            ",")

        # Валидация обязательных полей
        self._validate()

    def _validate(self):
        required = {
            'API_TOKEN': self.API_TOKEN,
            'LASTFM_API_KEY': self.LASTFM_API_KEY,
            'LASTFM_API_SECRET': self.LASTFM_API_SECRET
        }

        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


config = Config()