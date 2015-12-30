# Use Sublime Text 2 as q IDE

:exclamation:DEPRECATED: A new version which works with sublime text 3 is available [here](https://github.com/komsit37/sublime-q-3). I won't be updating this version anymore. Use this only if you specifically need sublime text 2, otherwise, use the new version.

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
git clone https://github.com/komsit37/sublime-q.git
```
Then you will need to download and install numpy 1.8 for python2.6. OSX yosemite comes with default numpy 1.6 for python 2.6<br>

*You need Python 2.6 since this is what sublime text uses
Installing the correct version of numpy in osx is a pain since it came with numpy 1.6. I removed numpy 1.6 first (by going to your python2.6 package folder and remove the folder directly). I downloaded .tar.gz from http://sourceforge.net/projects/numpy/files/NumPy/1.8.1/ and then run (if i remembered correctly)
```
python2.6 setup.py install
```

Only tested on OSX

## Troubleshoot
to check your numpy version and installed directory, open console from sublime text cmd + ` (sublimetext may use different versions from your osx terminal)
>>> import numpy<br>
>>> numpy.__version__<br>
'1.6.2'<br>
>>> numpy.__file__<br>
'/System/Library/Frameworks/Python.framework/Versions/2.6/Extras/lib/python/numpy/__init__.pyc'<br>

to remove numpy 1.6.2<br>
open terminal<br>
cd /System/Library/Frameworks/Python.framework/Versions/2.6/Extras/lib/python/<br>
sudo mv numpy numpy_old<br>

Update: Since OSX El Captain, you can't remove default python package with root. You will need to reboot into recovery mode (Command-R at startup logo), and run `csrutil disable` in terminal. see below link for more details 
https://apple.stackexchange.com/questions/193368/what-is-the-rootless-feature-in-el-capitan-really
