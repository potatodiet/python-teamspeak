import teamspeak3
import time

teamspeak = teamspeak3.teamspeak3()
teamspeak.connect()

teamspeak.command('login', {'client_login_name': 'serveradmin', 'client_login_password': 'K7Y8PqyE'})
teamspeak.command('use', {'sid': '1'})

while True:
    for user in teamspeak.command('clientlist'):
        user_info = teamspeak.command('clientinfo', {'clid': user['clid']})[0]

        if user_info.get('connection_client_ip') == '127.0.0.1':
            teamspeak.command('clientpoke', {'clid': user['clid'], 'msg': 'Good luck!'})
    time.sleep(5)

teamspeak.command('quit')