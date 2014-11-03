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
            return ".Q.s .tmp.res:" + s
    
    def send(self, s):
        Q.init()
        try:
            q = qconnection.QConnection(host = Q.host, port = Q.port, username = Q.user, password = Q.pwd)
            q.open()
            self.view.set_status('q', 'OK: ' + Q.con)

            statement = QSendCommand.transfrom(s)
            print statement
            q('.tmp.start:.z.T')
            res = q(statement)
            time = q('3_string `second$.z.T-.tmp.start')

            #get row count and set it to status text
            count = q('" x " sv string (count @[cols;.tmp.res;()]),count .tmp.res')
            self.view.set_status('result', 'Result: ' + str(count) + ', ' + str(time))
        except QException, msg:
            print msg
            res = "error: `" + str(msg)
        except socket_error as serr:
            self.view.set_status('q', 'FAIL: ' + Q.con)
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
        s = self.selectText()

        # only proceed if s is not empty
        if(s == "" or s == "\n"):
            return

        s = s.encode('ascii')  # qpy needs ascii
        print s

        self.send(s)

    def selectText(self):
        s = ""
        for region in self.view.sel():
            if region.empty():
                s += self.view.substr(self.view.line(region))
                # self.advanceCursor(region)
            else:
                s += self.view.substr(region)
        return s

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
            self.output_view = self.window().get_output_panel("q")
        self.output_view.set_syntax_file("Packages/Ocaml/OCamlyacc.tmLanguage")
        self.output_view.settings().set("word_wrap", False)
        self.clear_output()
        self.window().run_command("show_panel", {"panel": "output.q"})

    def clear_output(self):
        self.output_view.set_read_only(False)
        edit = self.output_view.begin_edit()
        self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
        self.output_view.end_edit(edit)
        self.output_view.set_read_only(True)


class QConnectCommand(sublime_plugin.WindowCommand):

    def run(self):
        Q.init()
        self.window.show_input_panel(
            Q.last, Q.con, self.on_done, None, None)

    def on_done(self, conn):
        Q.save(conn)
        print('saved ' + Q.con)
        Q.test()

class QSwitchCommand(sublime_plugin.WindowCommand):

    def run(self):
        settings = sublime.load_settings('sublime-q.sublime-settings')
        connections = settings.get('connections')
        self.window.show_quick_panel(connections, self.on_done)

    def on_done(self, x):
        Q.saveLast(x)
        Q.init()
        Q.test()

class QPrintCommand(QSendCommand):
    """
    Search the selected text or the current word
    """
    def preSend(self, s):
        return s

    def run(self, edit, flip):
        print "q_print " + str(flip)
        # grab the word or the selection from the view
        for region in self.view.sel():
            location = False
            if region.empty():
                # if we have no selection grab the current word
                location = self.view.word(region)
            else:
                # grab the selection
                location = region

            if location and not location.empty():
                s = self.view.substr(location)
                scope = self.view.scope_name(location.begin()).rpartition('.')[2].strip()

            # only proceed if s is not empty
            if(s == "" or s == "\n"):
                return

            s = s.encode('ascii')  # qpy needs ascii
            if (flip): s = 'flip ' + s
            s = self.preSend(s)
            print s

            self.send(s)

class QTypeCommand(QPrintCommand):
    """
    figure type for q object. use different command for table, functions, and other objects
    """
    def preSend(self, s):
        return "{$[.Q.qt x;meta x;100h=type x;value x;.Q.ty each x]} " + s

class QEnvCommand(QSendCommand):
    def run(self, edit):
        self.send('((enlist `ns)!(enlist(key `) except `q`Q`h`j`o)),{(`$/:x )! system each x } \"dvabf\"')

class QMemCommand(QSendCommand):
    def run(self, edit):
        self.send('.Q.w[]')


class Q():
    @staticmethod
    def init():
        settings = sublime.load_settings('sublime-q.sublime-settings')
        connections = settings.get('connections')
        Q.last = settings.get('last')
        Q.con = connections[0][1]
        for c in connections:
            if c[0] == Q.last: Q.con = c[1]

        s = Q.con.split(':')
        Q.host = s[0]
        Q.port = int(s[1])
        Q.user = s[2]
        Q.pwd  = s[3]

    @staticmethod
    def save(x):
        settings = sublime.load_settings('sublime-q.sublime-settings')
        Q.last = settings.get('last')
        Q.con = x
        connections = settings.get('connections')
        i = 0
        for c in connections:
            if c[0] == Q.last: break
            i += 1
        connections[i][1] = x
        settings.set('connections', connections)
        sublime.save_settings('sublime-q.sublime-settings')

    @staticmethod
    def saveLast(x):
        settings = sublime.load_settings('sublime-q.sublime-settings')
        connections = settings.get('connections')
        settings.set('last', connections[x][0])
        sublime.save_settings('sublime-q.sublime-settings')

    @staticmethod
    def test():
        try:
            q = qconnection.QConnection(host = Q.host, port = Q.port, username = Q.user, password = Q.pwd)
            q.open()
            sublime.active_window().active_view().set_status('q', 'OK: ' + Q.con)
        except socket_error as serr:
            print serr
            sublime.active_window().active_view().set_status('q', 'FAIL: ' + Q.con)
        finally:
            q.close()
   