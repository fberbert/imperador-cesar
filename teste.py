import shelve

#  db = shelve.open('membros', writeback=True)
#  db['King_Salame']['nickname'] = 'King Salame'
#  db.close()

#  db = shelve.open('guerra', writeback=True)
#  db['message_id'] = 0
#  db.close()

import datetime


def somarhorario(inicio):

    #  h_now, m_now, s_now = list(map(int,datetime.datetime.now().strftime('%H:%M:%S').split(':')))
    #  now_time = datetime.timedelta(hours=h_now, minutes=m_now, seconds=s_now)

    h_war, m_war, s_war = list(map(int,'{}:00'.format(inicio).split(':')))
    war_time = datetime.timedelta(hours=h_war, minutes=m_war, seconds=s_war)

    war_begin = datetime.datetime.now() + war_time
    war_ends  = war_begin + datetime.timedelta(days=1)

    str_inicio = war_begin.strftime('Início: %d/%m às %H:%M')
    str_fim = war_ends.strftime('Fim: %d/%m às %H:%M')
    print('{}\n{}'.format(str_inicio,str_fim))

somarhorario('5:10')
