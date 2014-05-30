class BinaryObject:
    def __init__(self):
        print "Initializing " + self.name
        self.state = 0
        self.turnOff() # On init, resets everything to off (since can't guess current state)
        
    def parse(self, room, input):
        oldState = self.state
        if 'on' in input:
            self.state = 1
        elif 'off' in input:
            self.state = 0
        
        # Only run change state if state has changed
        if self.state != oldState:
            self.updateState()
        
    def updateState(self):
        print "Default updateState called for " + self.name
        if self.state:
            self.turnOn()
        else:
            self.turnOff()
        
    def turnOn(self):
        print "TODO (ON) for " + self.name
        
    def turnOff(self):
        print "TODO (OFF) for " + self.name


class Projector(BinaryObject):
    name = "Projector"
        
    def updateState(self):
        if self.state:
            self.turnOn()
        else:
            self.turnOff()
    

# MODE OBJECTS
class ModeObject(BinaryObject):
    def parse(self, room, input):
        self.state = not self.state
        self.updateState()
        
        
class PartyMode(ModeObject):
    name = "Party Mode"
    
        
# JARVIS CENTRAL PROCESSING
class JarvisBrain:
    def __init__(self):
        print "Initializing Jarvis Virtual Control Matrix"
        
        # object name -> synonyms
        self.objectMap = {
            'party': ['party', 'fiesta', 'rave'],
            'movie': ['movie', 'film', 'video', 'tv'] ,
        	'lights': ['lights', 'light', 'lighting'],
        	'projector': ['projector', 'screen'],
        	'music': ['music', 'song', 'audio', 'sound'],
        	'environment': ['warm', 'hot', 'cool', 'cold', 'warmer', 'hotter', 'cooler', 'colder', 'AC', 'heater', 'fan']
        }
        
        # object name -> actual object to command
        self.objects = {}
        self.objects['projector'] = Projector()
        self.objects['party'] = PartyMode()

    def processInput(self, room, input):
        for word in input:
            for k in self.objectMap.keys():
                if word in self.objectMap[k]:
                    print "Commanding " + word
                    self.objects[word].parse(room, input)
                    return True
        # TODO if no command detected, keep listening?
        
        
jarvis = JarvisBrain()
print "TEST 1: Binary On"
jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'turn', 'projector', 'on', 'please'])
print "TEST 2: Binary Off"
jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'turn', 'projector', 'off', 'please'])
print "TEST 3: Mode"
jarvis.processInput(0, ['test', 'sentence', 'Jarvis', 'party', 'mode'])
print "TEST 4: No command"
jarvis.processInput(0, ['hey', 'Jarvis', 'hows', 'it', 'going'])

# Other tests: different rooms