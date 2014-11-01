import sublime
import sublime_plugin
import string
from qpython import qconnection
from qpython.qtype import QException
from socket import error as socket_error

class QSendCommand(sublime_plugin.TextCommand):
    @staticmethod
    def transfrom(s):
        if (s[0] == "\\"):
            return "value\"\\" + s + "\""
        else:
            return ".Q.s " + s
    
    def send(self, s):
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')
        pwd = settings.get('pwd')

        try:
            q = qconnection.QConnection(host = host, port = int(port), username = user, password = pwd)
            q.open()
            self.view.set_status('q', 'OK: ' + Q.toStr(host, port, user, pwd))

            statement = QSendCommand.transfrom(s)
            print statement
            res = q(statement)
        except QException, msg:
            print msg
            res = "error: `" + str(msg)
        except socket_error as serr:
            self.view.set_status('q', 'FAIL: ' + Q.toStr(host, port, user, pwd))
            raise serr
        finally:
            print "close"
            q.close()
        
        #return itself if query is define variable or function
        if res is None:
            res = s

        #print(res)
        self.show_output_panel()
        self.append_data(str(res))
        
    def run(self, edit):
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

        s = s.encode('ascii')  # qpy needs ascii
        print s

        self.send(s)

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

    def show_output_panel(self):
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
        settings = sublime.load_settings('sublime-q.sublime-settings')
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')
        pwd = settings.get('pwd')

        self.window.show_input_panel(
            'connect to', Q.toStr(host,port,user,pwd), self.q_server_input, None, None)

    def q_server_input(self, conn):
        settings = sublime.load_settings('sublime-q.sublime-settings')
        settings.set('host', Q.host(conn))
        settings.set('port', Q.port(conn))
        settings.set('user', Q.user(conn))
        settings.set('pwd', Q.user(conn))
        sublime.save_settings('sublime-q.sublime-settings')
        print('saved ' + conn)

        try:
            q = qconnection.QConnection(host = Q.host(conn), port = int(Q.port(conn)), username = Q.user(conn), password = Q.pwd(conn))
            q.open()
            sublime.active_window().active_view().set_status('q', 'OK: ' + conn)
        except socket_error as serr:
            print serr
            sublime.active_window().active_view().set_status('q', 'FAIL: ' + conn)
        finally:
            q.close()


class Q():
    @staticmethod
    def toStr(host, port, usr, pwd):
        s = host + ':' + port + ':' + usr + ':' + pwd
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
    @staticmethod
    def pwd(s):
        return s.split(':')[3]
