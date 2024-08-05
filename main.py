import asyncio
import logging


from aiogram import Bot,Dispatcher
from aiogram.filters import Command,CommandStart
from aiogram.types import Message
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

TOKEN = "7187016788:AAGmeE7OmOmtELfI8_67f9Fma_icDak-ciM"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback/"
SPOTIFY_CLIENT_ID = "6aa5a5f924aa414a90976c33631a4388"
SPOTIFY_CLIENT_SECRET = "13de252f85974fc4b113199dd673042d"
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=TOKEN)

user_tokens = {}

@dp.message(CommandStart())
async def command_start_handler(message: Message)-> None:
    auth_url = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                            client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=SPOTIFY_REDIRECT_URI,
                            scope=SCOPE).get_authorize_url()
    await message.answer(f"Привет, для начала пройди авторизацию в СПОТИФАЙ: {auth_url}")
    return

@dp.message(Command(commands=['auth']))
async def auth_handler(message:Message)-> None:
    code = message.get_args()
    if not code:
        await message.answer("Пожалуйста, предоставьте код из URL после авторизации.")
        return

    oauth = auth_url = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                            client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=SPOTIFY_REDIRECT_URI,
                            scope=SCOPE)
    token_info = oauth.get_access_token(code)
    user_tokens[message.from_user.id]=token_info
    await message.answer("Вы успешно авторизованы")

@dp.message(Command(commands=['current']))
async def current_song_handler(message:Message)->None:
    user_id = message.from_user.id
    if user_id not in user_tokens:
        await message.answer("Пожалуйста, авторизуйтесь сначала с помощью команды /start и следуйте инструкциям.")
        return

    token_info = user_tokens[user_id]
    sp = Spotify(auth=token_info['access_token'])
    current_track=sp.current_playback()
    if current_track is not None and current_track['is_playing']:
        track_name = current_track['item']['name']
        artists = ', '.join(artist['name']for artist in current_track['item']['artists'])
        await message.answer(f"Сейчас играет: {track_name} - {artists}")
    else:
        await message.answer("Сейчас ничего не играет.")

async def main()-> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    print("bot working")