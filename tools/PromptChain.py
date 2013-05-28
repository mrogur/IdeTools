import sublime

from ..IdeToolsError import IdeToolsError

class PromptChainItem(object):
    def __init__(self, prompt, key, default='', validatorCallback=None, errorMessage='', errorType='status'):
        

        self.prompt = prompt
        self.key = key
        self.value = None
        self.default = default
        self.listMode = False
        self.errorMessage = errorMessage if errorMessage else "Wrong value"


        if errorType not in ['error', 'status']:
            raise ValueError("Unsupported error type")
        self.errorType = errorType    


        if isinstance(default, list):
            self.listMode = True

        def emptyValidator(name):
            print(name)
            return True

        def listValidator(value):
            try:
                x = self.default[value]
                return True
            except IndexError:
                return False    

        if self.listMode: 
            validatorCallback = listValidator 

        self.validatorCallback = validatorCallback if hasattr(validatorCallback, '__call__') else emptyValidator

class PromptChain(object):
    def __init__(self, window, onFinishCallback):
        self.window = window
        self.commands = []
        self.counter = 0
        self.result = {}
        self.onFinishCallback = onFinishCallback
        self.events = []
        
    def getActiveItem(self):
        if not len(self.commands):
            return None
        try:
            return self.commands[self.counter]    
        except IndexError:
            return None    

    

    def add(self, prompt:str, key:str, default='', validatorCallback=None, errorMessage='', errorType='status'):
        item = PromptChainItem(prompt, key, default, validatorCallback, errorMessage, errorType)
        self.commands.append(item)



    def _createItemFromDictionary(self, item:dict):
        requiredArgs = {'prompt', 'key'}
        possibleArgs = {'prompt', 'key', 'default', 'validatorCallback', 'errorMessage', 'errorType'}
        if not isinstance(item, dict):
            raise IdeToolsError("Item is not dictionary instance")
        keys = set(item.keys())    
        if not requiredArgs.issubset(keys):        
            raise IdeToolsError("Item must have keys prompt and key")
        if keys.difference(possibleArgs):
            raise IdeToolsError("Wrong dictionary keys in command list item")   
        return PromptChainItem(**item)



    def addList(self, items:list):
        for item in items:
            try:
                chainItem = self._createItemFromDictionary(item)
            except IdeToolsError as e:
                print(e)
            else:
                self.commands.append(chainItem)
            
                
                
    def addItems(self, items:list):
        for item in items:
            if not isinstance(item, PromptChainItem):
                raise IdeToolsError("Can't add item to prompt chain")
        self.commands.extend(items)

    def insertItems(self, items:list, afterItem=None, atIndex=None):
        for item in items:
            print(type(item))
            try:
                if isinstance(item, dict):
                    item = self._createItemFromDictionary(item)
                elif not isinstance(item, PromptChainItem):
                     raise IdeToolsError("Can't add item to prompt chain")
            except IdeToolsError as e:
                print(e)
            else:
                if afterItem != None and isinstance(afterItem, PromptChainItem):
                    index = self.commands.index(afterItem)+1
                elif atIndex!=None and atIndex>=0 and atIndex < len(self.commands):
                     index = atIndex
                else:
                    index = self.counter+1
                self.commands.insert(index,item)                
    """
        Even handle methods
    """

    def on(self, key, value, callback):
        if not hasattr(callback, '__call__'):
            raise IdeToolsError("callback argument is not callable")

        self.events.append((key, value, callback))

    def checkEvents(self, key, value):
        for k,v,cb in self.events:
            if k==key and v==value:
                cb(self) 

    """
        Prompt related methods
    """

    def showInputPanel(self, item, cb):
        value = item.value if item.value else item.default 
        sublime.set_timeout(lambda: self.window.show_input_panel(item.prompt, value, cb, None, None), 10)        

    def showQuickPanel(self, item, cb):
        sublime.set_timeout(lambda: self.window.show_quick_panel(item.default, cb), 10)    


    def call(self,value):
        try:
            item = self.commands[self.counter]
            
            validation = item.validatorCallback(value)
            if validation:
                self.checkEvents(item.key, value)
                self.result[item.key] = value
                self.counter += 1
                item = self.commands[self.counter]
            else:
                item.value = value
                errorMethod = getattr(sublime, item.errorType+'_message') 
                errorMethod(item.errorMessage)

            if item.listMode:
                self.showQuickPanel(item, self.call)
            else:
                self.showInputPanel(item, self.call)

        except IndexError as e:
            self.onFinishCallback(self.result) 

    def run(self):
        if not len(self.commands):
            return
        self.counter = 0
        item = self.commands[0]
        if item.listMode:
            self.showQuickPanel(item, self.call)
        else:
            self.showInputPanel(item, self.call)    
