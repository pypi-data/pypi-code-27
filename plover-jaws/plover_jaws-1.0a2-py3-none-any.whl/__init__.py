import string
from pythoncom import CoInitialize
from win32com.client import Dispatch
from plover.engine import StenoEngine
class TypedChars:
    def __init__(self,maxCharsToKeep=512):
        self.maxCharsToKeep = maxCharsToKeep
        self.text = ''
        self.unspokenNewText = ''
        self.unspokenRemovedText = ''
        self.haveAddedNewTextSinceRemove = False

    def add(self,text):
        self.ensureUnspokenNewTextContainsBeginningOfWord(text)
        self.text += text
        self.unspokenNewText += text
        self.unspokenRemovedText = ''
        self.haveAddedNewTextSinceRemove = True
        
    def remove (self,count):
        self.haveAddedNewTextSinceRemove = False
        removed = self.text[-count:]
        self.text = self.text[:-count]
        self.unspokenRemovedText = removed + self.unspokenRemovedText
        self.unspokenNewText = self.unspokenNewText[:-count]
        return removed

    def ensureUnspokenNewTextContainsBeginningOfWord(self, text):
        # When using this module Plover must be set to append spaces to the end of words rather than
        # append them to the beginning. of words.
        # This function andles the situation where a complete word has been inserted and spoken. Then an suffix is typed
        # resulting in backspace being sent followed by the suffix itself and a trailing space.
        # In this situation, the user should hear the complete word. We check for that here and if detected,
# prime unspokenNewText with the  beginning of the word.
        # The above applies if the suffix is alphabetic. If punctuation or digits are being added then only the newly  typed text is spoken.
        if self.haveAddedNewTextSinceRemove or self.unspokenNewText: return
        if not self.text: return
        if self.text[-1].isspace(): return
        if self.isAppendingDigitsOrPunctuation(text): return
        self.unspokenNewText = self.getLastWord()

    def getAndClearUnspokenNewText(self):
        text = self.unspokenNewText
        self.unspokenNewText = ''
        return text
    
    def getAndClearUnspokenRemovedText(self):
        text = self.unspokenRemovedText
        self.unspokenRemovedText = ''
        return text

    def getLastWord(self):
        start = self.text.rfind(' ',0,-1)
        if start == -1:
            return self.text
        return self.text[start+1:]

    def isOnWordBoundary(self):
        return not self.text or self.text[-1].isspace()
    
    def isAppendingDigitsOrPunctuation(self,text):
        if self.text is None or not self.text:
            return False
        if text[0].isdigit() or (text[0] in string.punctuation):
            return True
        return False
    
class PloverJAWS:
    def __init__(self, engine,jawsApi=None):
        super().__init__()
        self.engine = engine
        global classInstance
        classInstance = self
        self.running = False
        CoInitialize()
        self.jaws = jawsApi if jawsApi is not None else Dispatch("freedomsci.jawsapi")
        self.engine.hook_connect('send_string',self.onSendString)
        self.engine.hook_connect('send_backspaces',self.onSendBackspaces)
        self.engine.hook_connect('send_key_combination',self.onSendKeyCombination)
        self.chars = TypedChars()
        self.lastSpoken = ''
        
    def start(self):
        self.running = True
        
    def stop(self):
        self.running = False
        
    def onSendString(self,text):
        self.chars.add(text)
        if self.chars.isOnWordBoundary():
            self.speakNewText()


    def onSendBackspaces(self,count):
        self.chars.remove(count)
        if self.chars.isOnWordBoundary():
            self.speakRemovedText()

    def onSendKeyCombination(self,string):
        pass
    
    def speak(self,text,alwaysSpeak=True):
        if alwaysSpeak or self.lastSpoken != text:
            self.jaws.SayString(text,False)
        self.lastSpoken = text
        
    def speakNewText(self):
        text = self.chars.getAndClearUnspokenNewText()
        if text and len(text.strip()) > 0:
            self.speak('{0} '.format(text))
            
    def speakRemovedText(self):
        text = self.chars.getAndClearUnspokenRemovedText()
        if text and len(text.strip()) > 0:
            self.speak('{0} '.format(text))

# Commands that can be bound to keys on the keyboard

def runScript(engine,scriptName):
    if classInstance:
        classInstance.jaws.runScript(scriptName)

def runFunction(engine,functionName):
    if classInstance:
        classInstance.jaws.runFunction(functionName)

        
class MockJawsApi:
    @staticmethod
    def SayString(text,flush=True):
        print(text)
        
    def runScript(scriptName):
        print('run script {}'.format(scriptName))

    def runFunction(scriptName):
        print('run function {}'.format(scriptName))
        
class Tester:
    def hook_connect(self,name,function):
        pass
    
    def load(self,className):
        self.plugin=  className(self,MockJawsApi)
        
    def sendString(self,text):
        self.plugin.onSendString(text)

    def sendBackspaces(self,count):
        self.plugin.onSendBackspaces(count)
        
    def sendKeyCombination(self,keyName):
        self.plugin.onSendKeyCombination(keyName)
        
        
def test()    :
    engine = Tester()
    engine.load(PloverJAWS)
    engine.sendString("hel")
    engine.sendString("lo ")
    engine.sendString("there")
    engine.sendBackspaces(2)
    engine.sendString("thi")
    engine.sendString("s is a test ")
    engine.sendBackspaces(1)
    engine.sendBackspaces(4)
    engine.sendString('dog ')
    engine.sendString('no ')
    engine.sendBackspaces(1)
    engine.sendString("-no ")
    engine.sendBackspaces(4)
    engine.sendString(' ')
    engine.sendString('another ')
    engine.sendString("what")
    engine.sendBackspaces(4)
    engine.sendString("word ")
    engine.sendBackspaces(1)
    engine.sendString("% ")
    engine.sendString("19 ")
    engine.sendBackspaces(1)
    engine.sendString("8 ")
    engine.sendKeyCombination('alt+ctrl+f')
    jawsRunScript('sayLine')    
if __name__ == "__main__": test()
        

