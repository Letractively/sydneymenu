"""
Argument list:
  run : run the server
  quit : exit the server

Options list:
  -h : show this message
"""



import socket
import smtplib
from email.MIMEText import MIMEText
from core.config import *
import json
import os
import getopt
import sys

HOST = 'localhost'
PORT = 8085

def SendCMD(cmd,attrs):
  HOST = 'localhost'    # The remote host
  PORT = 8085             # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((HOST, PORT))
    s.send("""["%s",%s]"""%(cmd,json.dumps(attrs)))
    s.close()
  except socket.error,e:
    print e 

def SendEMail(subject, message, to_addr = CONFIG.GMAIL_LOGIN,
              from_addr = CONFIG.GMAIL_LOGIN):
  msg = MIMEText(message)
  msg['Subject'] = subject
  msg['From'] = from_addr
  msg['To'] = to_addr
  server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login(CONFIG.GMAIL_LOGIN,CONFIG.GMAIL_PASSWORD)
  server.sendmail(from_addr, to_addr, msg.as_string())
  server.close()  

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:],"h",["help"])
  except getopt.error, msg:
    print msg
    print "for help use --help"
    exit(1)
  for o, a in opts:
    if o in ("-h","--help"):
      print __doc__
      sys.exit(0)
  for arg in args:
    if arg == "run":
      output = open('cmd.log','w')
      f = os.fork()
      if f == 0:
        output.write("Server Is Running...\n")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        s.listen(1)
        while 1:
          conn, addr = s.accept()
          output.write("""Connected by:%s\n""" % addr.__str__())
          while 1:
            data = conn.recv(1024)
            if not data:
              break
            try:
              output.write("data:%s\n"%(data))
              cmd_obj = json.loads(data)
              cmd = cmd_obj[0]
              if cmd == "SEND_MAIL":
                attrs = cmd_obj[1]
                SendEMail(attrs['subject'],attrs['message'],attrs['to_addr'])
              elif cmd == "QUIT":
                output.write("Successfully Quit\n")
                output.close()
                conn.close()
                exit(0) 
              else:
                pass
            except ValueError:
              output.write("ValueError\n")
          conn.close()          
      else:
        exit(0)
    elif arg == "quit":
      SendCMD("QUIT",{})
      exit(0)
    else:
      print ("Argument %s is not valid.\n"%arg)
      exit(0)
  print ("Argument is not provided.\n")

if __name__ == "__main__":
  main()
