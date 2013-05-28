import sublime, sublime_plugin, sys, os, re, imp, pprint, shutil, ftplib

#Some imports reload not be available in retail 


from pprint import pprint
from .tools.JsonSettings import JsonSettings
from .tools.PromptChain import *
from .tools.Project import Project
from .tools.Template import *
from .tools.Bundle import *
#from .tools.TemplateTools import *


class CreateProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = Project(self.window) 
        tools.create()

class IdeToolsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        #self.window.create_output_panel("haha")
        #self.window.run_command('show_panel', {"panel": "output.haha"})        
        # template = Template('php','composer', '/Users/mrogur/Code/test/vc')
        # template.scanTemplateFiles()
        # template.copyTemplateFiles()
        # template.process()

        # bundle = Bundles()
        # b = bundle.loadBundle('php')
        # print(b)

        
  

        #template.copyFiles()
        def mu(result):
            print(result)

        def vc(value):
            return re.match(r'^[a-zA-Z]\w+$',value) 

        chain = PromptChain(self.window, mu)
        
        chain.add("Select focus", "key8", [['lick','select lick'],'second', 'third'])
        chain.add("First", "key", "ciułała")
        chain.add("Second", "key3", "kardaśmon", vc, errorType='error', errorMessage="Ni ni ni")
        chain.add("Third", "ming", ['first','second', 'third'])
        chain.add("Name", "key99", "none")

        def fakeAdd(chain):
            items =[PromptChainItem('hello','mile','rocks')]
            activeItem = chain.commands[chain.counter]
            chain.insertItems(items,activeItem)

        chain.on('key', 'ciułała', fakeAdd)

        def fakeAdd2(chain):
            items = [{
                'prompt': 'Daj se siana',
                'key': 'klucz_do_szczescia',
            }]
            activeItem = chain.commands[chain.counter]
            chain.insertItems(items, activeItem)

        chain.on('key8',0, fakeAdd2)    
        chain.run()



class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")