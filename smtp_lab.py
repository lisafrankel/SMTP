from socket import *
import ssl
import base64

msg = '\r\n I love computer networks!'
endmsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
port = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, port))

recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
	print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
	print '250 reply not received from server.'


clientSocket.send('STARTTLS\r\n')
recv6 = clientSocket.recv(1024)
print('START TLS: ' + recv6)
if recv6[:3] != '220':
	print 'mail from 220 reply not received from server'

securedSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

securedSocket.send('AUTH LOGIN\r\n')
recv7 = securedSocket.recv(1024)
print('auth login: ' + recv7)
if recv7[:3] != '334':
	print 'auth login 334 reply not received from server'

securedSocket.send(base64.b64encode('user@gmail.com') + '\r\n')
securedSocket.send(base64.b64encode('userpassword') + '\r\n')


# Send MAIL FROM command and print server response.
mailFrom = 'MAIL FROM:<user@gmail.com>\r\n'
securedSocket.send(mailFrom)
recv2 = securedSocket.recv(1024)
print('Mail from command: ' + recv2)
if recv2[:3] != '334':
	print 'mail from 334 reply not received from server'


# Send RCPT TO command and print server response.
rcptTo = 'RCPT TO:<user@gmail.com>\r\n'
securedSocket.send(rcptTo)
recv3 = securedSocket.recv(1024)
print('Receipt to command: ' + recv3)
if recv3[:3] != '235':
	print 'rcpt to 235 reply not received from server'

# Send DATA command and print server response.
data = 'DATA\r\n'
securedSocket.send(data)
recv4 = securedSocket.recv(1024)
print('Data: ' + recv4)
if recv4[:3] != '250':
	print 'DATA 250 reply not received from server'

securedSocket.send(msg)

securedSocket.send(endmsg)

quit = 'QUIT\r\n'
securedSocket.send(quit)
recv5 = securedSocket.recv(1024)
print('Quit command: ' + recv5)
if recv5[:3] != '250':
	print 'quit 250 reply not received from server'
