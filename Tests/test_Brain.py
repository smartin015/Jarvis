from Brain import JarvisBrain

#TODO: Create test jarvis for each test
jarvis = JarvisBrain()

def test_binary_on():
  jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'turn', 'projector', 'on', 'please'])
  
def test_binary_off():
  jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'turn', 'projector', 'off', 'please'])
  
def test_mode():
  jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'party', 'mode'])

def test_no_command():
  jarvis.processInput(0, ['hey', 'Jarvis', 'hows', 'it', 'going'])
