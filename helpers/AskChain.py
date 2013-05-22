import sublime

class AskChainItem(object):
    def __init__(self, prompt, key, default='', validatorCallback=None, errorMessage='', errorType='status'):
        

        self.prompt = prompt
        self.key = key
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

class AskChain(object):
    def __init__(self, window, onFinishCallback):
        self.window = window
        self.commands = []
        self.counter = 0
        self.result = {}
        self.onFinishCallback = onFinishCallback
        
    def add(self, prompt, key, default='', validatorCallback=None, errorMessage='', errorType='status'):
        item = AskChainItem(prompt, key, default, validatorCallback, errorMessage, errorType)
        self.commands.append(item)

    def showInputPanel(self, item, cb):
        self.window.show_input_panel(item.prompt, item.default, cb, None, None)        

    def showQuickPanel(self, item, cb):
        sublime.set_timeout(lambda: self.window.show_quick_panel(item.default, cb), 10)    

    def call(self,value):
        try:
            item = self.commands[self.counter]
            
            validation = item.validatorCallback(value)
            if validation:
                self.result[item.key] = value
                self.counter += 1
                item = self.commands[self.counter]
            else:
                item.default = value
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
