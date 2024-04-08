import disnake
from disnake.ext import commands
import asyncio

intents = disnake.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

muted_users = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    #приветствие, при заходе на сервер приветствует нового участника
    if channel is not None:
        await channel.send(f'Привет, {member.mention}! Добро пожаловать на сервер!')

@bot.slash_command(name="kick", description="Кикнуть участника с сервера")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    #кик. Просто удаляем чувака с сервера
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был кикнут с сервера.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        #ошибка по кику пользователя, для тех у кого нет прав
        await ctx.send("У вас нет прав на эту команду!")

@bot.slash_command(name="ban", description="Забанить участника на сервере")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    #бан команда, прописана с помощью добавления некоторых функцый и прописи причины со временем
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} был забанен на сервере.')

@ban.error
async def ban_error(ctx, error):
    #ошибка бана . Создана для тех у кого нет прав  на команду
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав на эту команду!")

@bot.slash_command(name="unban", description="Разбанить участника на сервере")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    #разбан участника, кодом даём доступ входить ему на сервер
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} был разбанен на сервере.')
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        #ошибка разбана, чтобы те у кого нету прав на выполнение команды не могли её вводить
        await ctx.send("У вас нет прав на эту команду!")

@bot.slash_command(name="mute", description="Выдать мут участнику сервера")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: disnake.Member, duration: int, reason: str = None):
    #Выдать мут участнику на сервере
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'{member.mention} был замучен на {duration} минут.')

    muted_users[member.id] = muted_role

    await asyncio.sleep(duration * 60)

    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} был размучен после истечения времени.')

    del muted_users[member.id]
bot.run('MTE4MDc3NDg5MzQ0MTI1MzM3Ng.Gzw4Qs.smTI5tDvFwmo_qhpfGmUmCVKd_M5fdtDYh4ij0')