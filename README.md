# Use Sublime Text 2 as q IDE

Cmd + Enter or Cmd + e to send highlighted text or block text.<br>
Cmd + Alt + s to quickly switch between connections (configured in Preferences->Package Settings->sublime-q)
Cmd + Alt + c to edit selected kdb connection<br>
Syntax higlighing (based on kimtang's https://github.com/kimtang/sublime-q)<br>
shows rows, column, time at status bar <br>
<ul>super convenient shortcut (I got this idea from Tinn-R)
<li>f1 open help (this is actually on a different plugin, I will need to migrate it here)</li>
<li>f2 print variable</li>
<li>f3 show type</li>
<li>f4 show environments (variable, function, etc)</li>
<li>shift + f4 show memory usage (.Q.w)</li>
</ul>
![Image of screenshot](https://github.com/komsit37/sublime-q/blob/master/screenshot.png)

Use Exxeleron's python q api http://www.devnet.de/exxeleron/qpython <br>
Only works with Sublime 2.<br>

## Installation

Clone this git repository into your `Sublime Text 2/Packages` or `Sublime Text 3/Packages` directory. 

* Windows: `%APPDATA%\Sublime Text 2\Packages`
* OS X: `~/Library/Application Support/Sublime Text 2/Packages`
* Linux: `~/.config/sublime-text-2`

```
git clone https://github.com/komsit37/send-q.git
```
Then you will need to download and install for python2.6<br>
* https://github.com/exxeleron/qPython - download .tar.gz and install using python2.6 setup.py install
* numpy 1.8 (required by qPython)

*You need Python 2.6 since this is what sublime text uses
Installing the correct version of numpy in osx mavericks is a pain since maverick came with numpy 1.6. I removed numpy 1.6 first (by going to your python2.6 package folder and remove the folder directly). I downloaded .tar.gz from http://sourceforge.net/projects/numpy/files/NumPy/1.8.1/ and then run (if i remembered correctly)
```
python2.6 setup.py install
```

Only tested on MAC OSX Mavericks
