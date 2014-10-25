import sublime
import sublime_plugin
import string
from qpython import qconnection
from qpython.qtype import QException

class QSendCommand(sublime_plugin.TextCommand):

    @staticmethod
    def send(s):
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')

        # Split s into lines
        s = s.encode('ascii')  # qpy needs ascii
        print s
        #q = qpy.conn(host=host, port=int(port))
        q = qconnection.QConnection(host = host, port = int(port))
        q.open()
        try:
            res = q('.Q.s ' + s)
        except QException, msg:
            res = " `" + str(msg)
        finally:
            print "close"
            q.close()

        return res
        

    def run(self, edit):
        global settings
        settings = sublime.load_settings('sublime-q.sublime-settings')
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')
        self.view.set_status('q', 'q: ' + Q.toStr(host, port, user))

        # get s
        s = ""
        for region in self.view.sel():
            if region.empty():
                s += self.view.substr(self.view.line(region))
                # self.advanceCursor(region)
            else:
                s += self.view.substr(region)

        # only proceed if s is not empty
        if(s == "" or s == "\n"):
            return

        res = self.send(s)
        print(res)
        self.show_tests_panel()
        self.append_data(res)
        

    def advanceCursor(self, region):
        (row, col) = self.view.rowcol(region.begin())

        # Make sure not to go past end of next line
        nextline = self.view.line(self.view.text_point(row + 1, 0))
        if nextline.size() < col:
            loc = self.view.text_point(row + 1, nextline.size())
        else:
            loc = self.view.text_point(row + 1, col)

        # Remove the old region and add the new one
        self.view.sel().subtract(region)
        self.view.sel().add(sublime.Region(loc, loc))

    def window(self):
        return self.view.window()

    def append_data(self, data):
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.insert(edit, self.output_view.size(), data)
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)

    def show_tests_panel(self):
        if not hasattr(self, 'output_view'):
            self.output_view = self.window().get_output_panel("tests")
        self.output_view.set_syntax_file("Packages/Ocaml/OCamlyacc.tmLanguage")
        self.clear_test_view()
        self.window().run_command("show_panel", {"panel": "output.tests"})

    def clear_test_view(self):
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)


class QConnectCommand(sublime_plugin.WindowCommand):

    def run(self):
        global settings
        settings = sublime.load_settings('sublime-q.sublime-settings')
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')

        self.window.show_input_panel(
            'connect to', Q.toStr(host,port,user), self.q_server_input, None, None)

    def q_server_input(self, conn):
        global settings
        settings = sublime.load_settings('sublime-q.sublime-settings')
        settings.set('host', Q.host(conn))
        settings.set('port', Q.port(conn))
        settings.set('user', Q.user(conn))
        sublime.save_settings('sublime-q.sublime-settings')
        print('save')

class Q():
    @staticmethod
    def toStr(host, port, usr):
        s = host + ':' + port + ':' + usr
        return s
    @staticmethod
    def host(s):
        return s.split(':')[0]
    @staticmethod
    def port(s):
        return s.split(':')[1]
    @staticmethod
    def user(s):
        return s.split(':')[2]
