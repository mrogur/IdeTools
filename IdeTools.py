import sublime, sublime_plugin, sys, os, re, imp, pprint, shutil, ftplib

#Some imports reload not be available in retail 


from pprint import pprint
from .tools.JsonSettings import JsonSettings
from .tools.AskChain import AskChain
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

        bundle = Bundles()
        b = bundle.loadBundle('php')
        print(b)

        
  

        #template.copyFiles()
        # def mu(result):
        #     print(result)

        # def vc(value):
        #     return re.match(r'^[a-zA-Z]\w+$',value) 

        # chain = AskChain(self.window, mu)
        # chain.add("Select focus", "key5", [['lick','select lick'],'second', 'third'])
        # chain.add("First", "key", "ciułała")
        # chain.add("Second", "key3", "kardaśmon", vc, errorType='error', errorMessage="Ni ni ni")
        # chain.add("Third", "ming", ['first','second', 'third'])
        # chain.add("Select focus", "key5", ['lick','second', 'third'])
        # chain.run()


class CreatePhpProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        tools = PhpProject(self.window)
        tools.create()  
        print("foo me")