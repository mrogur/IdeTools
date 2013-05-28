import sublime, sublime_plugin, os, sys,  json

from .JsonSettings import JsonSettings
from .PromptChain import *


class Project(object):
	
	def __init__(self, window):
		self.window = window
		self.settings = None
		self.projectData = None
		self.projectFolder = None
		self.projectName = None
		self.projectPath = None
		
		self.loadSettings()

	def create(self):		
		self.window.run_command("prompt_open_folder")
		self.window = sublime.active_window()
		self.projectData = self.window.project_data()

		prompts = [
			{
				"prompt": "Insert project folder name: (new folder will be created)",
				"key": "projectFolder"		
			},
			{
				"prompt": "Insert project name:",
				"key": "projectName"		
			}
		]
		self.promptChain = PromptChain(self.window, self.makeProject)
		self.promptChain.addList(prompts)
		self.promptChain.run()


	def loadSettings(self):
		self.settings = sublime.load_settings('IdeTools.sublime-settings')


	# def promptName(self, name=''):
	# 	self.window.show_input_panel("Project name:",name,self.promptFolder, None, None)
		
	# def promptFolder(self, name):
	# 	self.projectName = name	
	# 	self.window.show_input_panel("Project folder:",'',self.assignFolderName, None, None)

	def assignFolderName(self, name):
		if re.match(r'^[a-zA-Z]\w+$',name): 
			self.projectFolder = name
			self.makeProject()
		else:
			sublime.message_dialog("Project fol must not have spaces")
			self.promptName(name)			

	def checkFolderName(self, name):
		return re.match(r'^[a-zA-Z]\w+$',name)	

	def makeProject(self, promptResult):
		"""Vars acquired from PromptChain"""
		projectFolder = promptResult['projectFolder']
		projectName = promptResult['projectName']

		if not (projectFolder and projectName):
			raise IdeToolsError("No apropriate project data")

		parentDir = self.projectData['folders'][0]['path']
		projectPath = os.path.join(parentDir, projectFolder)

		try: 
			os.mkdir(projectPath)
			self.projectData['folders'][0]['path'] = projectPath
			
			jsonSettings = JsonSettings(
				path=os.path.join(projectPath, projectName+'.sublime-project'),
				data=self.projectData
			)
			jsonSettings.save()
			self.openProject()	
		except OSError as e:
			print (e)

	def openProject(self):
		sublime.active_window().set_project_data(self.projectData)

