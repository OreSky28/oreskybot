import discord
from discord.ext import commands, tasks

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix = '!F', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Ready !")
    realStatus.start()

@tasks.loop(seconds = 5)
async def realStatus():
	game = discord.Game("Etre le meilleur Bot foot")
	await bot.change_presence(status = discord.Status.online, activity = game)

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(1021103693753491506)
    await channel.send(f"Bienvenue à {member.mention} ! :wave:")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(1021103693753491506)
    await channel.send(f"{member} nous a quitté ! :cry:")

@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfChannels = numberOfVoiceChannels + numberOfTextChannels
	userName = ctx.message.author.name
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	await ctx.channel.purge(limit=1)
	embed = discord.Embed(title =  "**Informations du serveur**", description = f"{userName} veut voir les informations du serveur !", color = 0x07B1BC)
	embed.set_thumbnail(url = "https://i.pinimg.com/564x/4d/0b/44/4d0b441e287fdd290a17d8dcffcd9c53.jpg")
	embed.add_field(name = "Nom du serveur :", value = f"**{serverName}**", inline = False)
	embed.add_field(name = "Nombre de membre :", value = f"Il y'a **{numberOfPerson}** footeux dans ce serveur !", inline = False)
	embed.add_field(name = "Nombre de salons :", value = f"Il y'a **{numberOfChannels}** salons footballistiques !", inline = False)
	embed.add_field(name = "Ecrit :", value = f"Dont **{numberOfTextChannels}** écrits", inline = True)
	embed.add_field(name = "Vocaux :", value = f"Et **{numberOfVoiceChannels}** vocaux", inline = True)
	await ctx.send(embed = embed)

@bot.command()
async def getInfo(ctx, info):
	server = ctx.guild
	await ctx.channel.purge(limit=1)
	messageMemberCount= f"Le serveur contient {server.member_count} footeux."
	messageNumberOfChannel= f"Le serveur contient {len(server.voice_channels)+len(server.text_channels)} salons footballistiques."
	messageServerName= f"Le serveur se nomme {server.name}."
	if info == "memberCount":
		await ctx.send(messageMemberCount)
	elif info == "numberOfChannel":
		await ctx.send(messageNumberOfChannel)
	elif info == "name":
		await ctx.send(messageServerName)
	else:
		await ctx.send("Ton message est comme si tu signé en MLS alors que t'es jeunes, **je ne comprend pas** \n(N'est ce pas Puig) \n*Si le problème persiste veuillez contacter un modérateur.*")

@bot.command()
async def say(ctx, *texte):
	await ctx.channel.purge(limit=1)
	await ctx.send(" ".join(texte))

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx , nombre : int):
 	await ctx.channel.purge(limit=nombre+1)
 	numberMessageClear=nombre
 	userName = ctx.message.author.name
 	message = f"{userName} a clear {numberMessageClear} messages !"
 	await ctx.send(message)


@bot.command(description="Mute certaines personnes.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Mute")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Mute")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="**Mute**", description=f"Un modérateur a frappé !", colour=0xff0000)
    embed.add_field(name="Membre mute :", value=member.name, inline=False)
    embed.add_field(name="Raison :", value=reason, inline=False)
    embed.add_field(name="Modérateur :", value=ctx.author.name, inline=False)
    embed.set_footer(text = "Pour toutes réclamation, veuillez contacter un Admin/Modo")
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member, *, reason=None):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Mute")
	await member.remove_roles(mutedRole)
	await ctx.channel.purge(limit=1)
	embed = discord.Embed(title="**Unmute**", description=f"Un modérateur a frappé !", colour=0x07B1BC)
	embed.add_field(name="Membre unmute :", value=member.name, inline=False)
	embed.add_field(name="Raison :", value=reason, inline=False)
	embed.add_field(name="Modérateur :", value=ctx.author.name, inline=False)
	embed.set_footer(text = "Pour toutes réclamation, veuillez contacter un Admin/Modo")
	await ctx.send(embed=embed) 
    
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.channel.purge(limit=1)
	embed = discord.Embed(title =  "**Kick**", description = "Un modérateur a frappé !", color = 0xff0000)
	embed.set_thumbnail(url = "https://www.pngmart.com/files/17/Ban-Stamp-PNG-Photos.png")
	embed.add_field(name = "Membre kick :", value = user.name, inline = False)
	embed.add_field(name = "Raison :", value = reason, inline = False)
	embed.add_field(name = "Modérateur :", value = ctx.author.name, inline = False)
	embed.set_footer(text = "Pour toutes réclamation, veuillez contacter un Admin/Modo")
	await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason ):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.channel.purge(limit=1)
	embed = discord.Embed(title =  "**Banissement**", description = "Un modérateur a frappé !", color = 0xff0000)
	embed.set_thumbnail(url = "https://www.pngmart.com/files/17/Ban-Stamp-PNG-Photos.png")
	embed.add_field(name = "Membre banni :", value = user.name, inline = False)
	embed.add_field(name = "Raison :", value = reason, inline = False)
	embed.add_field(name = "Modérateur :", value = ctx.author.name, inline = False)
	embed.set_footer(text = "Pour toutes réclamation, veuillez contacter un Admin/Modo")
	await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    await ctx.channel.purge(limit=1)
    async for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} a été débanni. :white_check_mark:')
            return
    await ctx.send(f"L'utilsateur {member} n'est pas dans la liste. :x:")


bot.run("MTAyMTA2MjY1MDYzOTE2MzQ5Mw.GKkEWO.4nHN1Bw9zU5ZJs7jTU3oThpiT6AxsJCCHq1AbQ")