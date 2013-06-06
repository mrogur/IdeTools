import sublime, sublime_plugin, sys, os, re, imp, pprint

#Some imports reload not be available in retail 

import IdeTools.tools.Project


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
        self._reload()
        print (args)
        project = Project(self.window, args)
        project.assignBundle()

        
        # project.create()
        # view = self.window.create_output_panel("haha")
        # view.run_command('insert', {'characters': 'text'})
        # self.window.run_command('show_panel', {"panel": "output.haha"})        

        # template = Template('php','composer', '/Users/mrogur/Code/test/vc')
        # template.scanTemplateFiles()
        # template.copyTemplateFiles()
        # template.process()

        # bundle = Bundles()
        # b = bundle.loadBundle('php')
        # print(b)

        
  

        #template.copyFiles()
        # def mu(result):
        #     print(result)

        # def vc(value):
        #     return re.match(r'^[a-zA-Z]\w+$',value) 

        # chain = PromptChain(self.window, mu)
        
        # chain.add("Select focus", "key8", [['lick','select lick'],'second', 'third'])
        # chain.add("First", "key", "ciułała")
        # chain.add("Second", "key3", "kardaśmon", vc, errorType='error', errorMessage="Ni ni ni")
        # chain.add("Third", "ming", ['first','second', 'third'])
        # chain.add("Name", "key99", "none")

        # def fakeAdd(chain):
        #     items =[PromptChainItem('hello','mile','rocks')]
        #     activeItem = chain.commands[chain.counter]
        #     chain.insertItems(items,activeItem)

        # chain.on('key', 'ciułała', fakeAdd)

        # def fakeAdd2(chain):
        #     items = [{
        #         'prompt': 'Daj se siana',
        #         'key': 'klucz_do_szczescia'
        #     },
        #     {
        #         'prompt': "Podaj powód dla którego nie miałbym cię zabić",
        #         'key': 'klucz_do_klozetu'
        #     },
        #     {
        #         'prompt': "i co?",
        #         'key': 'klucz_do_klucza',
        #         'default': [['a','a'],'b','c',['d','eee']]

        #     }]
        #     activeItem = chain.getActiveItem()
        #     chain.insertItems(items, activeItem)

        # chain.on('key8',0, fakeAdd2)    
        # chain.run()
    
    def _reload(self):
        imp.reload(IdeTools.tools.Project)


class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")