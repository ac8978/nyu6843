from socket import *

#import time

msg = "\r\n hi from SMTP"
endmsg = "\r\n.\r\n"

mailserver = ("mail.smtp2go.com", 2525) #Fill in start #Fill in end

clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket = ssl.wrap_socket(clientSocket)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
recv = recv.decode()
#print("Message after connection request:" + recv)
if recv[:3] != '220':
    #print('220 reply not received from server.')

heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
#print("Message after EHLO command:" + recv1)
if recv1[:3] != '250':
    #print('250 reply not received from server.')


mailFrom = "MAIL FROM: <ac8978@nyu.edu> \r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()


rcptTo = "RCPT TO: <ac8978@nyu.edu> \r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
recv3 = recv3.decode()


data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()

subject = "Subject is here \r\n\r\n"
clientSocket.send(subject.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)


quit = "QUIT\r\n"
clientSocket.send(quit.encode())
recv5 = clientSocket.recv(1024)

clientSocket.close()
