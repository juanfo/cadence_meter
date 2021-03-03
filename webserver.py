##############################################################################
#
# Example of using Python and XlsxWriter to create an Excel XLSX file in an in
# memory string suitable for serving via SimpleHTTPRequestHandler or Django or
# with the Google App Engine.
#
# Copyright 2013-2020, John McNamara, jmcnamara@cpan.org
#

# Note: This is a Python 3 example. For Python 2 see http_server_py2.py.

import http.server
import socketserver
import io
from urllib import parse
import serial
import threading


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/cu.usbmodem143101'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600

cadence = 0


def decode_serial():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    global cadence
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline().decode('utf-8')
        # reading is a string...do whatever you want from here
        cadence = reading.split()[1]


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        parsed_path = parse.urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message_parts.append('cadence ' + str(cadence))
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


x = threading.Thread(target=decode_serial)
x.start()

print('Server listening on port 8000...')
httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()
