import teamspeak3
import time

teamspeak = teamspeak3.teamspeak3()
teamspeak.connect()

teamspeak.command('login', {'client_login_name': 'serveradmin', 'client_login_password': 'travis_test'})
teamspeak.command('use', {'sid': '1'})

print(teamspeak.command('hostinfo'))

teamspeak.command('quit')
