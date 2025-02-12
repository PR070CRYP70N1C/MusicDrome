import os
import shutil
import pylast
from aiogram.types import Message
from mutagen.flac import FLAC
from config import MUSIC_FOLDER, TMP_DIR, MUSIC_COMMENT,LASTFM_API_SECRET,LASTFM_API_KEY
from worker import add_task_to_queue
import certifi

GENRES = [
    "rock", "pop", "jazz", "electronic", "hip hop",
    "classical", "metal", "blues", "reggae", "folk"
]

os.environ["SSL_CERT_FILE"] = certifi.where()
certifi.where()

network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET
)

async def handle_audio(message: Message, message_queue):
    audio_data = message.audio
    mime_type = audio_data.mime_type
    file_id = audio_data.file_id
    file_name = audio_data.file_name

    await add_task_to_queue(message_queue, message.bot, message.chat.id, "Получен файл, проверяю...", message.message_id)
    if mime_type and "flac" in mime_type.lower():
        await add_task_to_queue(message_queue, message.bot, message.chat.id, "Это FLAC. Начинаю скачивание...", message.message_id)

        # Получаем свежий file_id перед загрузкой
        file_info = await message.bot.get_file(message.audio.file_id)
        file_id = file_info.file_id  # Обновляем file_id
        downloaded_file = await message.bot.download_file(file_info.file_path)

        if not file_name or not file_name.lower().endswith(".flac"):
            file_name = f"{file_id}.flac"

        tmp_file_path = os.path.join(TMP_DIR, file_name)
        with open(tmp_file_path, "wb") as f:
            f.write(downloaded_file.read())

        audio_tags = FLAC(tmp_file_path)
        albumartist, album = "", ""
        for tag_key, tag_value in audio_tags.tags.items():
            if tag_key.lower() == "albumartist":
                albumartist = tag_value[0]
            elif tag_key.lower() == "album":
                album = tag_value[0]
            elif tag_key.lower() == "comment":
                audio_tags["comment"] = [MUSIC_COMMENT]
                audio_tags.save()

                track = network.get_track(audio_tags.tags['artist'][0], audio_tags.tags['title'][0])
                tags = track.get_top_tags()
                audio_tags["GENRE"] = ""
                if tags:
                    for tag in tags:
                        tag_name = tag.item.name.lower()
                        if tag_name in GENRES:

                            audio_tags["GENRE"] += [tag_name]
                audio_tags.save()

        await add_task_to_queue(message_queue, message.bot, message.chat.id, f"Скачан файл: {file_name}", message.message_id)

        artist_path = os.path.join(MUSIC_FOLDER, albumartist)
        album_path = os.path.join(artist_path, album)
        os.makedirs(album_path, exist_ok=True)

        try:
            shutil.move(tmp_file_path, album_path)
        except Exception as e:
            logger.error(f"Не удалось переместить файл: {e}")
            os.remove(tmp_file_path)
    else:
        await add_task_to_queue(message_queue, message.bot, message.chat.id, f"Получен audio, но не FLAC (mime_type={mime_type}).", message.message_id)
