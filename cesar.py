#!/usr/bin/env python3
"""
Bot Imperador César
"""

# -------------------------------------------------------------
#  importar bibliotecas
# -------------------------------------------------------------

# módulo de log no console
import logging

# módulo de expressões regulares
import re

import os
import random
import string
import shelve

# módulo do telegram bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# módulo de emojis
from emoji import emojize

from Quotes import Quotes

# -------------------------------------------------------------
# criando o updater e dispatcher para o BOT
# -------------------------------------------------------------
f = open('token.txt')
token = f.read()
f.close()

updater = Updater(
    token=token.strip(),
    use_context=True
)
job = updater.job_queue
dispatcher = updater.dispatcher

# ativando log de console, mudar para logging.DEBUG se quiser depurar
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----------------------------------------------------------------
# SEÇÃO DE TRATADORES DE COMANDOS (command handlers)
# ----------------------------------------------------------------


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá!")


def decommand(message):
    """
    Desconstrói uma linha de comando, retornando o comando e conteúdo
    """
    pattern = '^\/([^\s]*)[\s\n](.*)$'
    res = re.search(pattern, message, flags=re.S)

    if not res:
        pattern = '^\/([^\s]*)'
        res = re.search(pattern, message, flags=re.S)

    try:
        comando = res.group(1)
    except Exception:
        comando = ''

    try:
        conteudo = res.group(2)
    except Exception:
        conteudo = ''
    return [comando, conteudo]


def ajuda(update, context):
    """
    Menu de ajuda
    """
    html = """
Digite:

/ajuda - para obter ajuda

<strong>LISTA DE COMANDOS DO BOT</strong>

/nick - exibe seu nome de jogador no Dominations
/setnick - configura seu nome de jogador no Dominations

/guerra - exibe informações da guerra atual
/reservar - reserva uma base para atacar
/cancelar - cancela a reserva de uma base
/eliminar - elimina uma base da lista de guerra
/atualizar - atualiza informações sobre determinada base
/legendas - exibe as legendas da lista de guerra
/abrirbase - dica de como abrir uma base em guerra

/find &lt;jogador&gt; - para encontrar o contato de um jogador
/regras - para acessar a lista de regras da aliança


<strong>LISTA DE COMANDOS DE OFICIAIS</strong>

/users - lista todos os membros da aliança
/modelo - imprime um modelo para registro de nova guerra
/novaguerra - registra uma nova guerra
/apagarguerra - apaga a guerra atual
/obs - atualiza observações sobre a guerra
/delobs - apaga observações sobre a guerra
/up - atualiza qto de glórias a vencer
/down - atualiza qto de glórias a perder
/inimigo - atualiza o nome do adversário de guerra
/adicionar - adiciona uma base à lista de guerra

--

<i>Imperador César
Criado por Mestre Fábio ( @vivaolinux )
https://github.com/users/fberbert</i>
"""
    falar(update, context, html)


def quote():
    """
    Retorna uma frase de efeito
    """
    # importar classe Quotes, arquivo com todas as frases do Fahur
    quotes = Quotes()
    return quotes.quote()


def echo(update, context):
    """
    Recursos de iteração do bot nos canais em que ele participa
    """

    # definição de variáveis locais
    name = ""
    try:
        chat_id = update.effective_chat.id
        username = update.message.from_user.username
        userid = update.message.from_user.id
        name = update.message.from_user.first_name
        surname = update.message.from_user.last_name
        if not surname:
            surname = ""
        name = name + " " + surname
    except Exception:
        pass

    #  context.bot.send_message(chat_id=chat_id, text="test: " + name)

    try:

        msg = update.message.text.upper()

        if re.search(r'C.SAR', msg):
            falar(update, context, quote())

        regjoy = [
            re.compile("KKK"),
            re.compile("HAHAHA"),
            re.compile("HUAHUA")
        ]
        if any(regex.search(msg) for regex in regjoy):
            out = emojize(":joy::joy::joy:", use_aliases=True)
            falar(update, context, out)

        regrage = [
            re.compile("PQP"),
            re.compile("CARALHO"),
            re.compile("VTNC"),
            re.compile("PUTZ")
        ]
        if any(regex.search(msg) for regex in regrage):
            out = emojize(":rage:", use_aliases=True)
            falar(update, context, out)

        regcoffee = [re.compile("CAFÉ"), re.compile("CAFE")]
        if any(regex.search(msg) for regex in regcoffee):
            out = emojize(":coffee::coffee::coffee:", use_aliases=True)
            falar(update, context, out)

    except Exception:
        pass

    # verificar se o usuário possui username configurado
    if not username:
        output = "Por favor " + name + ", configure um username no Telegram!\n\nNo aplicativo, clique em <strong>Configurações > Nome de usuário</strong>. Basta escolher um nome de sua preferência, ele será seu ID no Telegram, usado para entrarmos em contato contigo sem a necessidade de saber seu número de telefone."
        falar(update, context, output)

    # armazena os dados do usuário em nossa base de dados
    # ou atualiza se já existir
    try:
        db = shelve.open('membros', writeback=True)
        try:
            nickname = db[username]['nickname']
        except Exception:
            nickname = ''
        db[username] = {"id": userid, "name": name, "nickname": nickname}
        db.close()
    except Exception:
        pass


def find(update, context):
    """
    Encontrar um usuário em nossa base de dados
    """

    # extrair o nome de usuário da linha de comando
    c, q = decommand(update.message.text)

    if len(q) < 3:
        falar(update, context, "Digite uma busca mais específica")
        return False

    # open shelve file
    db = shelve.open('membros')

    cont = 0
    for key in db:
        if q.upper() in db[key]['name'].upper() or q.upper() in db[key]['nickname'].upper():
            output = db[key]['nickname'] + ' | ' + db[key]['name'] + " @" + str(key)
            falar(update, context, output)
            cont += 1

    if cont == 0:
        falar(update, context, "Desculpe, não encontrei nenhum meliante com esse nome")
    db.close()


def setnick(update, context):
    """
    Configura um nickname do jogo para o membro
    """
    username = update.message.from_user.username
    c, nick = decommand(update.message.text)

    if len(nick) > 0:
        # open shelve file
        db = shelve.open('membros', writeback=True)
        db[username]['nickname'] = nick
        db.close()
        falar(update, context, "Nome de jogador configurado com sucesso: <b>{}</b>".format(nick))
    else:
        falar(update, context, "Informe um nome de jogador válido!")


def nick(update, context):
    """
    Exibe seu nickname
    """
    username = update.message.from_user.username

    try:
        # open shelve file
        db = shelve.open('membros')
        nick = db[username]['nickname']
        db.close()
        falar(update, context, "Olá <b>{}</b>, pronto para seguir o imperador César no campo de batalha?".format(nick))
    except Exception:
        falar(update, context, "Você ainda não configurou seu nick. Digite:\n\n/setnick")


def is_admin(user):
    """
    Checa se o usuário atual é admin
    """
    # usuários que terão permissão de acesso a comandos especiais
    authorized = ("vivaolinux", "CelloBit")

    #  if update.message.from_user.username not in authorized:
    if user not in authorized:
        return False
    return True


def users(update, context):
    """
    Listar todos os usuários de nossa base de dados
    """

    # open shelve file
    db = shelve.open('membros')

    if not is_admin(update.message.from_user.username):
        falar(update, context, "Você não tem permissão para este recurso!")
        return False

    users = list()
    for key in sorted(db):
        nickname = db[key]['nickname'] if len(db[key]['nickname']) > 1 else 'Não configurado'
        name = db[key]['name'] if len(db[key]['name']) > 1 else 'Sem nome'
        output = nickname + " | " + name + " => @" + str(key)
        users.append(output)

    db.close()

    total = len(users)
    users.sort()

    # limitar cada mensagem a 29 membros para não estourar o limite de caracteres de uma msg do Telegram
    sorted_output = ""
    cont = 0
    for user in users:
        sorted_output = sorted_output + user + "\n"
        cont = cont + 1
        if cont % 29 == 0:
            sorted_output = sorted_output + "::-::"

    sorted_output = sorted_output + "\n\n" + str(total) + " usuários"
    sorted_list = sorted_output.split("::-::")

    for line in sorted_list:
        falar(update, context, line)
    return True


def chatid(update, context):
    """
    Retorna o chat_id do canal
    """
    falar(update, context, str(update.effective_chat.id) + '\n' + update.effective_chat.type)


def regras(update, context):

    import glob

    for file in sorted(glob.glob("./regras/regra[123456].txt")):

        f = open(file, "r")
        output = f.read()
        f.close()

        falar(update, context, output)


def abrirbase(update, context):
    file = "./regras/abrirbase.txt"
    f = open(file, "r")
    output = f.read()
    f.close()
    falar(update, context, output)


def repeat(update, context):
    """
    Repetir o que você escreveu
    """
    if not is_admin(update.message.from_user.username):
        falar(update, context, "Você não tem permissão para este recurso!")
        return False

    c, output = decommand(update.message.text)
    context.bot.send_message(
        chat_id='-1001424488840',
        parse_mode='HTML',
        text=output
    )


def novaguerra(update, context):
    """
    Registra uma nova guerra
    """

    if not is_admin(update.message.from_user.username):
        falar(update, context, "Você não tem permissão para este recurso!")
        return False

    try:
        c, modelo = decommand(update.message.text)
    except Exception:
        return False

    if modelo == '':
        falar(update, context, """
Informe um modelo válido de guerra. Digite:

/modelo

para ter acesso a um modelo/template de guerra válido.
""")
        return False

    # processar texto
    # número de bases
    try:
        pattern = 'bases: ([0-9]+)\ninimigo: (.*)\nup: (.*)\ndown: (.*)\nobs:\n(.*)\n--- fim obs\n'
        res = re.search(pattern, modelo, re.S)
        jogadores = res.group(1)
        inimigo = res.group(2)
        up = res.group(3)
        down = res.group(4)
        obs = res.group(5)

        # gravar guerra no banco de dados
        db = shelve.open('guerra', writeback=True)
        db['jogadores'] = jogadores
        db['inimigo'] = inimigo
        db['up'] = up
        db['down'] = down
        db['obs'] = obs
        db['inicio'] = ''
        db['fim'] = ''

        bases = []
        for i in range(int(jogadores)):
            pattern = '^(' + "{:02d}".format(i+1) + '.*)$'
            res = re.search(pattern, modelo, flags=re.M)
            if res:
                bases.append(res.group(1))
                db["{:02d}".format(i+1)] = res.group(1)

        bases_string = ''
        for base in bases:
            bases_string += re.sub(r'^(..)', r'\1. ', base) + '\n'

        falar(update, context, "Guerra registrada com sucesso! Para maiores informações, digite:\n\n/guerra")
        db.close()
    except Exception:
        falar(update, context, "Modelo de guerra inválido. Digite:\n\n/modelo\n\ne tente novamente.")
    return True


def apagarguerra(update, context):
    """
    Deleta informações sobre a guerra atual
    """

    if not is_admin(update.message.from_user.username):
        falar(update, context, "Você não tem permissão para este recurso!")
        return False

    os.remove('guerra.db')
    falar(update, context, "Guerra removida com sucesso!")


def guerra(update, context):
    """
    Exibe informações da guerra atual
    """
    db = shelve.open('guerra')
    try:
        inimigo = db['inimigo']
        jogadores = db['jogadores']
        up = db['up']
        down = db['down']
        obs = db['obs']
        inicio = db['inicio']
        fim = db['fim']
    except Exception:
        falar(update, context, "Nenhuma guerra encontrada! Digite:\n\n/novaguerra\n\npara registrar uma.")
        return False

    bases_string = ''
    for i in range(int(jogadores)):
        try:
            bases_string += re.sub(r'^(..)', r'\1. ', db["{:02d}".format(i+1)]) + '\n'
        except Exception:
            pass

    falar(update, context, "CWB-LIS 🆚 {}\n🔼 {} 🔽 {}\n{}\n\n{}\n\n<pre>Início: {}\nFim: {}\n<i>* horário de Brasília</i></pre>".format(inimigo, up, down, obs, bases_string, inicio, fim))
    db.close
    return True


def pegar_nickname(user):
    """
    Retorna o nome de jogador de user
    """
    db = shelve.open('membros')
    try:
        nickname = db[user]['nickname']
        return nickname
    except Exception:
        return ''


def falar(update, context, msg):
    """
    Envia msg para o chat
    Sala de guerra: -456778807
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode='HTML',
        text=msg
    )


def reservar(update, context):
    """
    Reserva uma base
    """
    c, b = decommand(update.message.text)
    base_arr = b.split()
    #  base = re.sub(r'\s', '', b)
    #  base = '{:02d}'.format(int(b))
    nickname = pegar_nickname(update.message.from_user.username)

    if len(nickname) == 0:
        msg = "Você precisa registrar seu nickname no jogo. Digite:\n\n/nickname"
        falar(update, context, msg)
        return False

    if len(base_arr) == 0:
        msg = "Você precisa informar uma base válida."
        falar(update, context, msg)
        return False

    db = shelve.open("guerra", writeback=True)
    try:
        msg = ''
        for base in base_arr:
            base = '{:02d}'.format(int(base))
            base_desc = db[base]
            db[base] = base_desc + ' - ' + nickname
            msg += "Base {} reservada com sucesso!\n".format(base_desc)
    except Exception:
        base = ''
    db.close()

    if len(base) == 0:
        msg = "Você precisa informar uma base válida."

    falar(update, context, msg)
    return True


def cancelar(update, context):
    """
    Cancela a reserva de uma base
    """
    c, b = decommand(update.message.text)
    base_arr = b.split()
    #  base = re.sub(r'\s', '', b)
    #  base = '{:02d}'.format(int(b))
    nickname = pegar_nickname(update.message.from_user.username)

    if len(nickname) == 0:
        msg = "Você precisa registrar seu nickname no jogo. Digite:\n\n/nickname"
        falar(update, context, msg)
        return False

    db = shelve.open("guerra", writeback=True)
    try:
        msg = ''
        for base in base_arr:
            base = '{:02d}'.format(int(base))
            base_desc = re.sub(r' -.*$', '', db[base])
            db[base] = base_desc
            msg += "Reserva {} cancelada com sucesso!\n".format(base_desc)
    except Exception:
        base = ''
    db.close()

    if len(base) == 0:
        msg = "Você precisa informar bases válidas."

    falar(update, context, msg)
    return True


def eliminar(update, context):
    """
    Elimina determinada base da lista de guerra
    """
    c, b = decommand(update.message.text)
    base_arr = b.split()
    #  base = re.sub(r'\s', '', b)

    if len(base_arr) == 0:
        msg = "Você precisa informar uma base válida."
    else:
        db = shelve.open("guerra", writeback=True)
        try:
            msg = ''
            for base in base_arr:
                base = '{:02d}'.format(int(base))
                base_desc = db[base]
                del db[base]
                msg += 'Base {} eliminada com sucesso!\n'.format(base_desc)
        except Exception:
            msg = 'Erro ao eliminar a base. Informe uma base válida!'
        db.close()
    falar(update, context, msg)


def atualizar(update, context):
    """
    Atualiza informações sobre determinada base
    """
    c, b = decommand(update.message.text)
    base = re.sub(r'\s', '', b)
    pattern = '^([0-9]*)'
    res =  re.search(pattern, base)
    base_num = '{:02d}'.format(int(res.group(1)))

    if len(base_num) == 0:
        msg = "Você precisa informar uma base válida."
    else:
        db = shelve.open("guerra", writeback=True)
        try:
            res = re.search(r'^([0-9]*)([^\s]*)(.*)$', base)
            #  base_num = res.group(1)
            base_desc = re.sub(r'\.', '', res.group(2))
            db[base_num] = base_num + base_desc
            msg = 'Base {} atualizada com sucesso!'.format(base_desc)
        except Exception:
            msg = 'Erro ao atualizar a base!'
        db.close()
    falar(update, context, msg)


def estrelas(update, context):
    """
    Atualiza estrelas sobre determinada base
    """
    pattern = '^\/([^\s]*)\s([\d]*)\s(\d*)$'
    res = re.search(pattern, update.message.text)
    #  comando = res.group(1)
    base = res.group(2)
    base = '{:02d}'.format(int(base))
    estrelas = res.group(3)

    if len(base) == 0:
        msg = "Você precisa informar uma base válida."
    else:
        db = shelve.open("guerra", writeback=True)
        try:
            estrelas = int(estrelas) * '⭐️'
            base_desc = re.sub(r'\s.*$', '', db[base])
            txt = base_desc + ' ' + estrelas
            db[base] = txt
            msg = 'Base {} atualizada com sucesso!'.format(base_desc)
        except Exception:
            msg = 'Erro ao atualizar a base!'
        db.close()
    falar(update, context, msg)


def atualizar_info(update, context):
    """
    Atualiza observações da guerra
    """

    if not is_admin(update.message.from_user.username):
        falar(update, context, "Você não tem permissão para este recurso!")
        return False

    comando, conteudo = decommand(update.message.text)

    if len(conteudo) == 0 and comando != 'delobs':
        msg = "Você precisa informar observações válidas."
        falar(update, context, msg)
        return False

    db = shelve.open("guerra", writeback=True)
    try:
        if comando == 'delobs':
            comando = 'obs'
            conteudo = ''
        db[comando] = conteudo
        msg = 'Informações atualizadas com sucesso!'
    except Exception:
        msg = 'Erro ao atualizar as observações!'
    db.close()
    falar(update, context, msg)
    return True


def legendas(update, context):
    """
    Legendas da lista de guerra
    """
    falar(update, context, """
⛩ Cidade proibida
🛡 Coalizões de defesa
😈 Torre de bazucas
🚫 Não atacar
🕐 Baixar o tempo
🚁 Base de helicópteros
⭐ Estrelas conquistadas
""")


def modelo(update, context):
    """
    Imprime um modelo/template de guerra
    """
    modelo = """
bases: 15
inimigo: Os Bárbaros
up: 178
down: 99
obs:

3🛡 Bit, Siri, Deus, bobao
2🛡
1🛡 Seik, Rui

--- fim obs

01EI346F 🛡
02EI322
03DG298 🛡
04DG306
05EE293⛩🛡🛡🛡
06EI328⛩
07GF258
08EE244
09EE234⛩
10AT194
11GL197
12IN159
13IN150
14IL105
15PV95
"""
    falar(update, context, modelo)


# bloco principal
# lista de administradores do bot

# command handlers
find_handler = CommandHandler('find', find)
dispatcher.add_handler(find_handler)

users_handler = CommandHandler('users', users)
dispatcher.add_handler(users_handler)

chatid_handler = CommandHandler('chatid', chatid)
dispatcher.add_handler(chatid_handler)

help_handler = CommandHandler(['help', 'ajuda'], ajuda)
dispatcher.add_handler(help_handler)

regras_handler = CommandHandler('regras', regras)
dispatcher.add_handler(regras_handler)

repeat_handler = CommandHandler('repeat', repeat)
dispatcher.add_handler(repeat_handler)

novaguerra_handler = CommandHandler('novaguerra', novaguerra)
dispatcher.add_handler(novaguerra_handler)

guerra_handler = CommandHandler('guerra', guerra)
dispatcher.add_handler(guerra_handler)

apagarguerra_handler = CommandHandler('apagarguerra', apagarguerra)
dispatcher.add_handler(apagarguerra_handler)

reservar_handler = CommandHandler('reservar', reservar)
dispatcher.add_handler(reservar_handler)

eliminar_handler = CommandHandler('eliminar', eliminar)
dispatcher.add_handler(eliminar_handler)

cancelar_handler = CommandHandler('cancelar', cancelar)
dispatcher.add_handler(cancelar_handler)

atualizar_handler = CommandHandler('atualizar', atualizar)
dispatcher.add_handler(atualizar_handler)

setnick_handler = CommandHandler('setnick', setnick)
dispatcher.add_handler(setnick_handler)

nick_handler = CommandHandler('nick', nick)
dispatcher.add_handler(nick_handler)

modelo_handler = CommandHandler('modelo', modelo)
dispatcher.add_handler(modelo_handler)

legendas_handler = CommandHandler('legendas', legendas)
dispatcher.add_handler(legendas_handler)

estrelas_handler = CommandHandler('estrelas', estrelas)
dispatcher.add_handler(estrelas_handler)

abrirbase_handler = CommandHandler('abrirbase', abrirbase)
dispatcher.add_handler(abrirbase_handler)

atualizar_info_handler = CommandHandler(['obs', 'delobs', 'inimigo', 'jogadores', 'up', 'down', 'inicio', 'fim'], atualizar_info)
dispatcher.add_handler(atualizar_info_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# iniciar looping do bot
try:
    updater.start_polling()
except Exception:
    pass
