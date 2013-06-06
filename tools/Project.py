import sublime, os, re

from .JsonSettings import JsonSettings
from .PromptChain import PromptChain
from ..IdeToolsError import IdeToolsError
from .Bundle import Bundles, BundlesPromptMapper

class Project(object):
	
	def __init__(self, window, args=None):
		self.window = window
		self.settings = None
		self.projectData = None
		self.projectFolder = None
		self.projectName = None
		self.projectPath = None
		
		self.loadSettings()

		#Properties from args 

		self.context = None
		self.template = None


		if args:
			self.assignProperties(args)
		print("hahhaa mahahaha")

	def assignProperties(self, args):
		for (arg, val) in args.items():
			if hasattr(self, arg):
				setattr(self, arg, val)
	

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
			jsonSettings.set('IdeTools',{})
			jsonSettings.save()
			
		except OSError as e:
			print (e)
		else:
			self.projectPath = projectPath
			self.projectName = projectName

			sublime.active_window().set_project_data(self.projectData)
	
	def assignBundle(self):

		if self.context is None:
			self._promptBundle()
		elif self.context:
			try:
				self.bundle = Bundles().loadBundle(self.context)
			except IdeToolsError as e:
				raise e

				
		

	def _promptBundle(self, bundleData=None):
		if bundleData is None:
			items = []
			for item in BundlesPromptMapper():
				items.append(item)
			
			prompt = [{'key':'context', 'default': items, 'prompt': 'Select context'}]
			chain = PromptChain(self.window, self._promptBundle)
			chain.addList(prompt)
			chain.run()
			
		else:
			index = int(bundleData['context'])

			if index>=0:
				self.context = Bundles().bundles[index]
				self.assignBundle()
			else:
				self.context = False	
		
	def promptTemplate(self):
		pass
		

	def errorMsg(self, message):
		sublime.show_error(message)
