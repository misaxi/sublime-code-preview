import subprocess, os
import sublime, sublime_plugin

def compile(view, source_file_ext, target_file_ext, cmd):
    source = view.file_name()
    folder, filename = os.path.split(source)
    name   = filename[0:filename.rfind('.' + source_file_ext)]
    ext    = filename.rsplit('.',1)[1]
    target = os.path.join(folder, name + '.' + target_file_ext)
    window = view.window()

    if ext != source_file_ext:
        return

    print '[codepreview]', '%s detected...' % source_file_ext

    if(window.num_groups() == 1):
        print '[codepreview]', 'stop because of single view'
        return

    cmd = cmd.replace('{{source}}', source)
    cmd = cmd.replace('{{target}}', target)
    print '[codepreview]', cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    if retval != 0:
        print '[codepreview]', 'error occured while compiling the file', source
        output = p.stdout.readlines()
        with open(target, 'w') as f:
            f.write(''.join(output))
        f.close()

    window.focus_group(1)
    window.open_file(target)
    window.focus_view(view)

class CoffeeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, 'coffee', 'js', 'coffee --compile "{{source}}"'), 0)

class IcedCoffeeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, 'iced', 'js', 'iced --compile "{{source}}"'), 0)
        
class TypeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, 'ts', 'js', 'tsc "{{source}}"'), 0)

class Less(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, 'less', 'css', 'lessc "{{source}}" "{{target}}"'), 0)
