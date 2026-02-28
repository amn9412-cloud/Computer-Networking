from socket import *

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port)) # [cite: 13, 77, 78]

    recv = clientSocket.recv(1024).decode()

    clientSocket.send('HELO Alice\r\n'.encode()) # [cite: 73]
    recv1 = clientSocket.recv(1024).decode()

    clientSocket.send('MAIL FROM:<alice@alice.com>\r\n'.encode())
    recv2 = clientSocket.recv(1024).decode()

    clientSocket.send('RCPT TO:<bob@bob.com>\r\n'.encode())
    recv3 = clientSocket.recv(1024).decode()

    clientSocket.send('DATA\r\n'.encode())
    recv4 = clientSocket.recv(1024).decode() # [cite: 55]

    clientSocket.send(msg.encode())
    clientSocket.send(endmsg.encode()) # [cite: 56, 58]
    recv5 = clientSocket.recv(1024).decode()

    clientSocket.send('QUIT\r\n'.encode()) # [cite: 62]
    recv6 = clientSocket.recv(1024).decode()
    
    clientSocket.close()

if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')