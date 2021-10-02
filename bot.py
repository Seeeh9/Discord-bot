import discord
import random as rd
import re
from discord.ext import commands

client = commands.Bot(command_prefix="<")

replay_list = ['Лучше бы что-то умное написал...', 'Мда...', 'Сам придумал?', 'Ага, поверю', 'Гениальная мысль',
               'Полностью согласен!', 'Жертва соционики', 'Таков гоблидеализм', 'Ты случайно не Джексон?',
               'Это многое говорит об обществе...', 'Чел...', 'Типичный подсос паука', 'Хохла спросить забыли',
               'Хрю-хрю', 'Woman moment', 'Хрюса порвало)', 'Это пропаганда, не бьётся же!',
               'Либераху порвало', 'Типичный порвак', 'Забудь кнопку чата']

rp_roles_list = ['Монархист', 'Анархист', 'Нс', 'Социал-Демократ', 'Социалист', 'Фашист', 'Коммунист', 'Либерал',
                 'Консерватор', 'Традиционалист', 'Этнонационалист', 'Минархист', 'Прогрессивист', 'Левый', 'Правый',
                 'Либертарианец', 'Гражданский', 'Центрист', 'Зеленый', 'Верующий', 'Агностик', 'Атеист']

admin_roles = ['Администрация', 'Модератор', 'Хелпер']
high_iq_role = ['Высший']
lector_role = ['Лектор']
active_role = ['Активный']
donater_role = ['Донатер']
member_role = ['Участник']
mute_role = ['Мут']

all_available_lists = rp_roles_list + admin_roles + high_iq_role + lector_role \
                      + active_role + donater_role + member_role + mute_role
ignore_list = ['разум', 'и', 'Националист', ',' ' , ', ' ,', ', ']

emoji_list = [794621244729196554, 793789448680243200, 793789448373534730, 826799073356414976,
              793789448109817868, 793789448206024704, 793789449053798431, 784465005596114977,
              784376179675234305, 793789448403157012, 848145066844225547, 793789448349417496,
              793789448105623614, 793789448307474432, 793789448193703937, 843506456316739615,
              793789448437235743, 848145067284758558, 785382838064250880, 793789448139702273,
              848145065427992576, 848327336000618546, 848145067293278240]


@client.event
async def on_ready():
    print('Бот запущен')


lock_commands = False

admins = ['Seh9#3887', '***']


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    global lock_commands

    # "Выключение" и "Включение" бота
    if message.content == '!status' and str(message.author) in admins:
        if lock_commands is False: await message.reply('Бот работает')
        if lock_commands is True: await message.reply('Бот не работает')

    if message.content == '!off' and str(message.author) in admins:
        if lock_commands is not True:
            lock_commands = True
            await message.reply('Бот выключен')
        else: await message.reply('Бот уже выключен')

    if message.content.startswith('!on') and str(message.author) in admins:
        if lock_commands is not False:
            lock_commands = False
            await message.reply('Бот включен')
        else:
            await message.reply('Бот уже включен')

    given_roles = []
    existing_roles = []

    taken_roles = []
    notexisting_roles = []

    notfounded_roles = []

    # Выдача ролей
    give_phrases = ('Бот дай рол', 'Бот, дай рол', 'бот, дай рол', 'бот дай рол')
    if message.content.startswith(give_phrases) and lock_commands is False:
        member = message.author
        message_list = re.split("; |, | |,", message.content.title())
        roles_in_msg = list(set(rp_roles_list) & set(message_list))

        for msg in message_list[3:]:
            if (msg not in all_available_lists) and (msg not in ignore_list):
                notfounded_roles.append(msg)
            elif msg not in rp_roles_list:
                print(f'{member} запросил дать не ботовую роль: {msg}')

            if msg in admin_roles: await message.reply(f'Роль "{msg}" может выдать только Комрад!')
            if msg in high_iq_role: await message.reply('Роль "Высший разум" дают за победу в дебатах 😎')
            if msg in lector_role: await message.reply(f'Роль "{msg}" дают за проведение лекций!')
            if msg in active_role: await message.reply(f'Роль "{msg}" ты получишь за активность на сервере!')
            if msg in donater_role: await message.reply(f'Роль "{msg}" вручают за финансовую помощь серверу 😉')
            if msg in member_role: await message.reply(f'Роль "{msg}" получают за прочтение <#767800114982813756>')
            if msg in mute_role: await message.reply(f'Роль "{msg}" дают тем, кто себя плохо ведёт :)')

        if len(roles_in_msg) > 0:
            print(f'{member} просит дать роли: {roles_in_msg}')
            for role_in_msg in roles_in_msg:
                if role_in_msg == 'Гражданский': role_in_msg = 'Гражданский националист'
                if role_in_msg == 'Нс': role_in_msg = 'НС'
                if role_in_msg == 'Социал-Демократ': role_in_msg = 'Социал-демократ'

                role = discord.utils.get(message.guild.roles, name=role_in_msg)

                if role in member.roles:
                    existing_roles.append(role_in_msg)
                else:
                    await member.add_roles(role)
                    given_roles.append(role_in_msg)

        if len(given_roles) > 0:
            list_of_given_roles = ", ".join(given_roles)
            await message.reply(f'Выдал роли: {list_of_given_roles}')
            print(f'{member} получил роли: {list_of_given_roles}')
        if len(existing_roles) > 0:
            list_of_existing_roles = ", ".join(existing_roles)
            await message.reply(f'У тебя уже есть роли: {list_of_existing_roles}')
            print(f'{member} уже имел роли: {list_of_existing_roles}')
        if len(notfounded_roles) > 0:
            list_of_notfounded_roles = ", ".join(notfounded_roles)
            await message.reply(f'Не могу найти такие роли: {list_of_notfounded_roles}')
            print(f'{member} запросил ненайденные роли: {list_of_notfounded_roles}')

    # Забор ролей
    take_phrases = ('Бот забери рол', 'Бот, забери рол', 'бот, забери рол', 'бот забери рол')
    if message.content.startswith(take_phrases) and lock_commands is False:
        member = message.author
        message_list = re.split("; |, | ", message.content.title())
        roles_in_msg = list(set(rp_roles_list) & set(message_list))

        for msg in message_list[3:]:
            if (msg not in all_available_lists) and (msg not in ignore_list): notfounded_roles.append(msg)
            if msg in list(set(all_available_lists) - set(rp_roles_list)):
                await message.reply(f'Я не могу забрать "{msg}"!')
                print(f'{member} запросил забрать не ботовую роль: {msg}')

        if len(roles_in_msg) > 0:
            print(f'{member} просит забрать роли: {roles_in_msg}')
            for role_in_msg in roles_in_msg:
                if role_in_msg == 'Гражданский': role_in_msg = 'Гражданский националист'
                if role_in_msg == 'Нс': role_in_msg = 'НС'
                if role_in_msg == 'Социал-Демократ': role_in_msg = 'Социал-демократ'
                role = discord.utils.get(message.guild.roles, name=role_in_msg)

                if role in member.roles:
                    await member.remove_roles(role)
                    taken_roles.append(role_in_msg)
                else:
                    notexisting_roles.append(role_in_msg)

        if len(taken_roles) > 0:
            list_of_taken_roles = ", ".join(taken_roles)
            await message.reply(f'Забрал роли: {list_of_taken_roles}')
            print(f'{member} потерял роли: {list_of_taken_roles}')
        if len(notexisting_roles) > 0:
            list_of_notexisting_roles = ", ".join(notexisting_roles)
            await message.reply(f'У тебя нет ролей: {list_of_notexisting_roles}')
            print(f'{member} не имел ролей: {list_of_notexisting_roles}')
        if len(notfounded_roles) > 0:
            list_of_notfounded_roles = ", ".join(notfounded_roles)
            await message.reply(f'Не могу найти такие роли: {list_of_notfounded_roles}')
            print(f'{member} запросил ненайденные роли: {list_of_notfounded_roles}')

    # Шанс на рандомный ответ или эмодзи
    speaking_chats = [768054267667808257, 789604912648421377, 768055307753619457, 800967622488489984]
    if message.channel.id in speaking_chats and lock_commands is False:
        if rd.randint(1, 1000) == 3:
            await message.reply(rd.choice(replay_list))
        if rd.randint(1, 200) == 2:
            await message.add_reaction(client.get_emoji(rd.choice(emoji_list)))
        if rd.randint(1, 2) == 1:
            await message.add_reaction("🐷")


client.run('***')
