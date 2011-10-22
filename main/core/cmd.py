import socket
import json

def SendCMD(cmd,attrs):
  HOST = 'localhost'    # The remote host
  PORT = 8085              # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((HOST, PORT))
    s.send("""["%s",%s]"""%(cmd,json.dumps(attrs)))
    s.close()
  except socket.error,e:
    pass

def SendMail(subject,msg,to):
  SendCMD("SEND_MAIL",{"subject":subject,"message":msg,"to_addr":to})


if __name__ == "__main__":
  SendMail("ProxService Shut Down","Warning: ProxService Shut Down.","zoyoeproject@gmail.com")
  SendCMD("QUIT",{})
