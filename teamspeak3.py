import socket

class teamspeak3:
    def __init__(self, host = 'localhost', port = 10011):
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

            first_message = self.sock.recv(8).decode('utf-8').strip()

            if first_message != 'TS3':
                print('This connection is not responding as a TeamSpeak 3 server.')
                print(first_message)
                return False

            self.sock.recv(1024)

        except:
            print('Connection error')
            return False

    def command(self, cmd, params = {}, options = ''):
        out = ''
        response = ''

        out += cmd

        for key in params:
            out += ' %s=%s' % (key, self.encode_param(params[key]))

        out += ' ' + options + '\n'

        self.sock.sendall(out.encode('utf-8'))

        while True:
            response += self.sock.recv(1024).decode('utf-8')
            if 'msg=' in response:
                break

        return self.parse_response(response)

    def encode_param(self, params):
        params = params.replace('\\', '\\\\')
        params = params.replace('/',  '\\/')
        params = params.replace(' ',  '\\s')
        params = params.replace('|',  '\\p')
        params = params.replace('\a', '\\a')
        params = params.replace('\b', '\\b')
        params = params.replace('\f', '\\f')
        params = params.replace('\n', '\\n')
        params = params.replace('\r', '\\r')
        params = params.replace('\t', '\\t')
        params = params.replace('\v', '\\v')
        
        return params

    def decode_param(self, params):
        params = params.replace('\\\\', '\\')
        params = params.replace('\\/',  '/')
        params = params.replace('\\s',  ' ')
        params = params.replace('\\p',  '|')
        params = params.replace('\\a',  '\a')
        params = params.replace('\\b',  '\b')
        params = params.replace('\\f',  '\f')
        params = params.replace('\\n',  '\n')
        params = params.replace('\\r',  '\r')
        params = params.replace('\\t',  '\t')
        params = params.replace('\\v',  '\v')

        params = params.replace('\r',  '')
        params = params.replace('\n',  '')

        return params

    def parse_response(self, response):
        out = []

        response = response[:response.find('error id')]

        for key in response.split('|'):
            data = {}

            for key in key.split(' '):
                value = key.split('=', 1)
                data[value[0]] = self.decode_param(''.join(value[1:]))

            out.append(data.copy())

        return out