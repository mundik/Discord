import socket
import os
import time


def probe(typ):
    response = ""
    stat = -1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if typ == "S":
        try:
            s.connect(('25.106.72.55', int('25565')))
            s.shutdown(1)
            response = 'Standart server: Running'
            stat = 1
        except ConnectionRefusedError:
            response = 'Standart server: Offline'
            stat = 0
        finally:
            return stat, response
    elif typ == "T":
        try:
            s.connect(('25.106.72.55', int('25566')))
            s.shutdown(1)
            response = 'Testing server: Running'
            stat = 1
        except ConnectionRefusedError:
            response = 'Testing server: Offline'
            stat = 0
        finally:
            return stat, response


def start(typ):
    if typ == "T":
        os.system('cmd /k "start C:\\Server_new\\Server.bat"')
        print(str('Server shut down at: ' + time.asctime(time.localtime())[-13:-5]))
    elif typ == "S":
        os.system('cmd /k D:\\Server\\Server.bat')
        print(str('Server shut down at: ' + time.asctime(time.localtime())[-13:-5]))