import sublime
import sublime_plugin
import logging
import re
from .src import common

import time

settings = {'scope2command':{}}
log = logging.getLogger('root')
scope2command = {}
load_settings_timestamp = 0

def load_new_settings():
	# global load_settings_timestamp
	global settings
	global log
	global scope2command
	# load_settings_timestamp = time.time()
	log.debug("loaded formatter autoselect")
	log.disabled = not settings.get('debug', False)
	s2c = settings.get('scope2command', [])
	s2caliases = settings.get('aliases', [])
	for key in s2c:
		if s2c[key]['command']:
			_re = key;
			if key in s2caliases:
				for skey in s2caliases[key]:
					_re += '|' + re.escape(skey)
			s2c[key]['_re'] = re.compile(' (' + _re + ') ')
			log.debug(s2c[key]['_re'].pattern)
			scope2command[key] = s2c[key]
	# s2c["-timestamp"] = load_settings_timestamp
	# settings.set('scope2command', s2c)

def plugin_loaded():
	global settings
	settings = common.settings()
	# settings = sublime.load_settings('FormatterAutoselect.sublime-settings')
	load_new_settings()
	# log.disabled = not common.settings().get('debug', False)
	# log.debug("loaded formatter autoselect")
	# s2c = common.settings().get('scope2command', [])
	# for key in s2c:
	# 	if s2c[key]['command']:
	# 		s2c[key]['_re'] = re.compile(' '+key+' ')
	# 		log.debug(s2c[key]['_re'].pattern)
	# 		scope2command[key] = s2c[key]

class RunFormatterAutoselectCommand(sublime_plugin.TextCommand):
	def exec_command(self,command):
		args = None
		if 'args' in command:
			args = command['args']

		context = self.view
		if 'context' in command:
			context_name = command['context']
			if context_name == 'window':
				context = context.window()
			elif context_name == 'app':
				context = sublime
			elif context_name == 'text':
				pass
			else:
				# Workaround for sublime-evernote package, modified by Chien Chun
				pass
				# values = ','.join(str(v) for v in context_name)
				# raise Exception('Invalid command context "'+values+'".')

		if args is None:
			context.run_command(command['command'])
		else:
			context.run_command(command['command'], args)

		return

	def run(self, edit):
		global log
		global scope2command
		view = self.view

		load_new_settings()

		first_point = view.sel()[0].a
		scope = ' '+view.scope_name(first_point)+' '
		log.debug('Current scope: '+scope)

		command = False

		for key in scope2command:
			_re = scope2command[key]['_re']
			result = _re.search(scope)
			if result:
				command = scope2command[key]
				break

		if not command:
			log.debug('Can\'t find assigned command')
			return

		log.debug('Command: '+command['command'])
		if command['args']:
			log.debug('Args:')
			log.debug(command['args']);

		self.exec_command(command)

		return
#		if commands is None:
#			return # not an error
#		for command in commands:
#			self.exec_command(command)
