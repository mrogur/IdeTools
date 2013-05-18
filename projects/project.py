import sublime, sublime_plugin, os, sys, re, json

class Project(object):
	def __init__(self, window):
		self.window = window
		self.settings = self.loadSettings()
		self.projectData = None
		self.projectName = None
		self.projectPath = None
	def create(self):		
		self.window.run_command("prompt_open_folder")
		self.window = sublime.active_window()
		self.projectData = self.window.project_data()
		self.promptName()

	def loadSettings(self):
		return sublime.load_settings('IdeTools.sublime-settings')

	def promptName(self, name=''):
		self.window.show_input_panel("Project name:",name,self.assignName, None, None)

	def assignName(self, name):
		if self.checkName(name): 
			print(name)
			self.projectName = name
			self.makeProject()
		else:
			sublime.message_dialog("Project name must not have spaces")
			self.promptName(name)			

	def checkName(self, name):
		return re.match(r'^[a-zA-Z]\w+$',name)	

	def makeProject(self):
		path = self.projectData['folders'][0]['path']
		self.projectPath = os.path.join(path, self.projectName)
		self.saveProject()

	def saveProject(self):
		try: 
			os.mkdir(self.projectPath)
			self.projectData['folders'][0]['path'] = self.projectPath
			os.chdir(self.projectPath)

			with open(self.projectName+'.sublime-project', encoding='utf-8', mode='w+') as file:
				print("file created now")
				file.write(json.dumps(self.projectData, indent=4, separators=(',', ': ')))
				file.close()
			sublime.active_window().set_project_data(self.projectData)
			self.openProject()	
		except OSError as e:
			print (e.errno)

	def openProject(self):
		print(sublime.active_window().project_data())
