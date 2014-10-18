import sublime
import sublime_plugin
import string
import qpy

class QSendCommand(sublime_plugin.TextCommand):

    @staticmethod
    def escapeString(s):
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        s = s.replace('\n', '')  # for multiple line
        s = s.encode('ascii')  # qpy needs ascii
        return s

    @staticmethod
    def send(selection):
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')

        # Split selection into lines
        selection = QSendCommand.escapeString(selection)
        print(selection)
        q = qpy.conn(host=host, port=int(port))
        print(q(selection))
        q.close()

    def run(self, edit):
        print('run')
        global settings
        settings = sublime.load_settings('SendQ.sublime-settings')
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')
        self.view.set_status('q', 'q: ' + Q.toStr(host, port, user))

        # get selection
        selection = ""
        for region in self.view.sel():
            if region.empty():
                selection += self.view.substr(self.view.line(region)) + "\n"
                # self.advanceCursor(region)
            else:
                selection += self.view.substr(region) + "\n"

        # only proceed if selection is not empty
        if(selection == "" or selection == "\n"):
            return

        self.send(selection)

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


class QConnectCommand(sublime_plugin.WindowCommand):

    def run(self):
        global settings
        settings = sublime.load_settings('SendQ.sublime-settings')
        host = settings.get('host')
        port = settings.get('port')
        user = settings.get('user')

        self.window.show_input_panel(
            'connect to', Q.toStr(host,port,user), self.q_server_input, None, None)

    def q_server_input(self, conn):
        global settings
        settings = sublime.load_settings('SendQ.sublime-settings')
        settings.set('host', Q.host(conn))
        settings.set('port', Q.port(conn))
        settings.set('user', Q.user(conn))
        sublime.save_settings('SendQ.sublime-settings')
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
