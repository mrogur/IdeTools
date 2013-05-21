import sublime, sublime_plugin, sys, os, re, imp

#Some imports reload not be available in retail 
import IdeTools.projects.Project
imp.reload(IdeTools.projects.Project)
import IdeTools.helpers.JsonSettings
imp.reload(IdeTools.helpers.JsonSettings)

from .projects.Project import Project
from .projects.PhpProject import PhpProject
from .helpers.JsonSettings import JsonSettings

class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window) 
        tools.create()

class IdeToolsCommand(sublime_plugin.WindowCommand):
#Cut here
    class AskChainItem(object):
        def __init__(self, prompt, key, default='', validatorCallback=None):
            def emptyValidator(name):
                print(name)
                return True

            self.prompt = prompt
            self.key = key
            self.default = default

            self.validatorCallback = validatorCallback if hasattr(validatorCallback, '__call__') else emptyValidator

    class AskChain(object):
        def __init__(self, window, onFinishCallback):
            self.window = window
            self.commands = []
            self.counter = 0
            self.result = {}
            self.onFinishCallback = onFinishCallback
            
        def add(self, prompt, key, default='', validatorCallback=None):
            item = IdeToolsCommand.AskChainItem(prompt, key, default, validatorCallback)
            self.commands.append(item)

        def call(self,value):
            try:
                item = self.commands[self.counter]

                validation = item.validatorCallback(value)
                if validation:
                    self.result[item.key] = value
                    self.counter += 1
                    item = self.commands[self.counter]

                self.showInputPanel(item, self.call)

            except IndexError as e:
                self.onFinishCallback(self.result) 

        def showInputPanel(self, item, cb):
            self.window.show_input_panel(item.prompt, item.default, cb, None, None)        

            

        def run(self):
            if not len(self.commands):
                return
            self.counter = 0
            item = self.commands[0]
            self.window.show_input_panel(item.prompt, item.default, self.call, None, None)
            

#Cut here            
    def run(self, **args):
        # config = JsonSettings()  
        # config.data = '{"dom": "otwarty", "fuck":"me", "help":[{"value": "ąąąą"}]}'
        # print(config.data)  
        # print(type(config.data))
        def mu(result):
            print(result)

        def vc(value):
            return re.match(r'^[a-zA-Z]\w+$',value) 

        chain = self.AskChain(self.window, mu)
        chain.add("First", "key", "ciułała")
        chain.add("Second", "key3", "kardaśmon", vc)
        chain.run()


class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")