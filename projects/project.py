import sublime, sublime_plugin, os, sys, re

class Project(object):
	def __init__(self, window):
		self.window = window
		self.settings = self.load_settings()
		self.project_data = None
		self.project_name = None

	def create(self):		
		self.window.run_command("prompt_open_folder")
		self.window = sublime.active_window()
		self.project_data = self.window.project_data()
		self.prompt_name()

	def load_settings(self):
		return sublime.load_settings('IdeTools.sublime-settings')

	def prompt_name(self, name=''):
		self.window.show_input_panel("Project name:",name,self.assign_name, None, None)

	def assign_name(self, name):
		if self.check_name(name): 
			self.project_name = name
			self.make_project()
		else:
			sublime.message_dialog("Project name must not have spaces")
			self.prompt_name(name)			

	def check_name(self, name):
		return re.match(r'^[a-zA-Z]\w+$',name)	

	def make_project(self):
		print (self.project_data['folders'][0]['path'])		
