HOST = "192.168.1.15"
PORT = 81
GET = "GET /livestream.cgi?user=admin&pwd=123456&streamid=3&audio=1&filename= HTTP/1.1\r\nHost: 192.168.1.15:81\r\n\r\n"



audio_hex = "00:00:00:00:08:00:00:00:d4:52:fe:15:17:00:00:00:00:01:00:00:00:00:00:00:00:00:00:00:00:00:00:00"
audio_hex_cap = "f7:fb:0e:00:4b:c6:08:a1:18:0b:24:8b:01:82:a0:15:9c:81:3d:e0:22:28:be:88:10:41:83:80:c9:98:28:79:15:bb:06:90:8b:19:00:04:b0:0b:35:0b:41:b0:a8:5b:a7:19:0a:00:94:8d:10:a0:16:18:9a:a9:71:a4:a8:91:1a:9b:29:15:d0:92:0b:39:4d:01:93:91:9c:d3:6a:1a:c1:22:a9:90:3c:49:91:95:d1:0a:88:21:60:c8:b1:14:2a:2f:83:a9:82:90:48:1b:20:1b:a7:81:9d:10:2b:c2:84:5a:a3:90:88:8d:38:12:f0:89:81:89:3b:8c:91:37:8a:3a:a8:72:09:10:e3:99:02:1c:48:0a:9a:d2:0b:37:2c:80:12:a0:8c:12:80:9e:00:08:01:c9:41:b8:2b:96:9a:02:9c:86:09:91:d9:48:00:09:f2:29:00:00:1a:1f:92:a9:34:a1:3a:0b:02:f1:89:58:0a:3d:94:91:0a:ab:83:7a:08:f3:09:81:3b:11:b9:07:80:99:2f:02:89:02:f2:1b:20:08:18:c9:13:b2:7a:9b:23:b2:89:05:9f:08:93:48:a0:88:12:1b:17:8a:92:0c:22:f0:40:c8:10:3a:9a:a0:87:10:9b:18:82:59:b3:99:87:1c:3a:92:08:d2"

AUDIO = "".join([chr(int(h, 16)) for h in audio_hex.split(":")])

# Echo client program
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket opened"
try:
    s.connect((HOST, PORT))
    print "Connected"
    s.send(GET)
    print "Sent"
    
    while 1:
        print len(s.recv(1024)) # Dump this
        s.send(AUDIO)
finally:
    s.close()