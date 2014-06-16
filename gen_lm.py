import urllib2
import poster.encode
import poster.streaminghttp
import re

FOLDER = "Brain"
BASE_URL = "http://www.speech.cs.cmu.edu"
UPLOAD_PATH = "/cgi-bin/tools/lmtool/run"
UPLOAD_FILE = "commands.txt"

opener = poster.streaminghttp.register_openers()
params = {'formtype': 'simple', 'corpus': open(FOLDER + "/" + UPLOAD_FILE,'rb')}
datagen, headers = poster.encode.multipart_encode(params)
response = opener.open(urllib2.Request(BASE_URL + UPLOAD_PATH, datagen, headers))

text = response.read()

path_m = re.search("<title>Index of (.+?)</title>", text)
if not path_m:
  raise Exception("Could not find path")
download_path = path_m.group(1) + "/"

base_m = re.search("The base name for this set is <b>(.+?)</b>", text)
if not base_m:
  raise Exception("Could not find set base name")
base_id = base_m.group(1)

# Grab the language model
lm_path = BASE_URL + download_path + base_id + ".lm"
response = urllib2.urlopen(lm_path)
html = response.read()
with open(FOLDER + "/commands.lm", "w") as f:
  f.write(html)

dic_path = BASE_URL + download_path + base_id + ".dic"
response = urllib2.urlopen(dic_path)
html = response.read()
with open(FOLDER + "/commands.dic", "w") as f:
  f.write(html)


