# Use Sublime Text 2 as q IDE

Cmd + Enter to send highlighted text or block text.<br>
Cmd + Alt + c to connect to kdb.<br>
Bring up console window to see output from kdb.

Use Exxeleron's python q api http://www.devnet.de/exxeleron/qpython <br>
Only works with Sublime 2.<br>
Inspired by https://github.com/wch/SendText

## Installation

Clone this git repository into your `Sublime Text 2/Packages` or `Sublime Text 3/Packages` directory. 

* Windows: `%APPDATA%\Sublime Text 2\Packages`
* OS X: `~/Library/Application Support/Sublime Text 2/Packages`
* Linux: `~/.config/sublime-text-2`

```
git clone https://github.com/komsit37/send-q.git
```
Then you will need to download and install for python2.6<br>
* https://github.com/exxeleron/qPython
* numpy 1.8 (required by qPython)

*You need Python 2.6 since this is what sublime text uses

Only tested on MAC OSX Mavericks
