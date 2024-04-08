import disnake
from disnake.ext import commands
import youtube_dl

intents = disnake.Intents.all()

# Создание экземпляра бота
bot = commands.Bot(command_prefix='!', intents=intents)

# Функция для загрузки музыки с YouTube
def get_youtube_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']
    return url

# Команда для проигрывания музыки
@bot.command()
async def play(ctx, *, query):
    voice_state = ctx.author.voice
    if not voice_state or not voice_state.channel:
        await ctx.send("Вы не находитесь в голосовом канале.")
        return

    voice_channel = voice_state.channel
    voice_client = ctx.guild.voice_client

    if not voice_client:
        voice_client = await voice_channel.connect()
    else:
        if voice_client.is_playing():
            voice_client.stop()

    url = get_youtube_url(query)
    voice_client.play(disnake.FFmpegPCMAudio(url), after=lambda e: print('Проигрывание завершено', e))
    await ctx.send(f'Проигрывается музыка: {query}')

# Запуск бота
bot.run('MTE4MDc3NDg5MzQ0MTI1MzM3Ng.Gzw4Qs.smTI5tDvFwmo_qhpfGmUmCVKd_M5fdtDYh4ij0')