import sublime
import sublime_plugin
import re
import os


class SublimeOnSaveBuild(sublime_plugin.EventListener):
    def on_post_save(self, view):
        global_settings = sublime.load_settings(self.__class__.__name__+'.sublime-settings')
        # See if we should build. A project level build_on_save setting
        # takes precedence. To be backward compatible, we assume the global
        # build_on_save to be true if not defined.
        should_build = view.settings().get('build_on_save', global_settings.get('build_on_save', True))

        # Load filename filter. Again, a project level setting takes precedence.
        filename_filter = view.settings().get('filename_filter', global_settings.get('filename_filter', '.*'))

        # filename_ignore
        filename_ignore = view.settings().get('filename_ignore', global_settings.get('filename_ignore'))

        if not should_build:
            return

        if not re.search(filename_filter, view.file_name()):
            return

        if filename_ignore and re.search(filename_ignore, os.path.basename(view.file_name())):
            return

        view.window().run_command('build')



class SublimeOnSaveBuildToggleCommand(sublime_plugin.TextCommand):
    def run(self, view, enable=True):
        setting_filename = "SublimeOnSaveBuild.sublime-settings"
        settings = sublime.load_settings(setting_filename)
        settings.set('build_on_save', enable)
        sublime.save_settings(setting_filename)