# from subprocess import call
import subprocess, os
import sublime, sublime_plugin

def compile(view, file_ext, cmd):
    fullname = view.file_name()
    folder, filename = os.path.split(fullname)
    name   = filename[0:filename.rfind('.coffee')]
    ext    = filename.rsplit('.',1)[1]
    target = os.path.join(folder, name + '.js')
    window = view.window()
    
    if ext != file_ext:
        return

    print '%s detected...' % file_ext

    if(window.num_groups() == 1):
        print 'stop because of single view'
        return

    cmd = '{0} "{1}"'.format(cmd, fullname)
    print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    print retval
    if retval != 0:
        output = p.stdout.readlines()
        with open(target, 'w') as f:
            f.write(''.join(output))
        f.close()

    window.focus_group(1)
    window.open_file(target)
    window.focus_view(view)

class CoffeeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, "coffee", "coffee --compile"), 0)

class IcedCoffeeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, "iced", "iced --compile"), 0)
        
class TypeScript(sublime_plugin.EventListener):
    def on_post_save(self, view):
        sublime.set_timeout(lambda: compile(view, "ts", "tsc"), 0)
        # folder, filename = os.path.split(view.file_name())
        # name, ext = filename.split('.')
        # target = os.path.join(folder, name + '.js')
        # window = view.window()
        
        # if ext != 'coffee':
        #     return

        # print 'coffeescript detected...'        

        # if(window.num_groups() == 1):
        #     print 'stop because of single view'
        #     return

        # p = subprocess.Popen('coffee --compile "%s"' % view.file_name(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # retval = p.wait()

        # if retval != 0:
        #     output = p.stdout.readlines()
        #     with open(target, 'w') as f:
        #         f.write(''.join(output))
        #     f.close()

        # window.focus_group(1)
        # window.open_file(target)
        # window.focus_view(view)