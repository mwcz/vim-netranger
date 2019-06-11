import inspect
import os
import shutil
import subprocess

import _thread as thread
import vim
from netranger.Vim import VimAsyncRun, VimErrorMsg


class Shell():
    userhome = os.path.expanduser('~')

    @classmethod
    def ls(cls, dirname):
        return os.listdir(dirname)

    @classmethod
    def abbrevuser(cls, path):
        return path.replace(Shell.userhome, '~')

    @classmethod
    def run(cls, cmd):
        try:
            return subprocess.check_output(
                cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            VimErrorMsg(e)

    @classmethod
    def run_async(cls, cmd, cbk_stdout=None, cbk_exit=None):
        def print_error(err_msg):
            msg = '\n'.join(err_msg)
            if msg:
                VimErrorMsg(msg)

        VimAsyncRun(cmd,
                    cbk_stdout=cbk_stdout,
                    cbk_exit=cbk_exit,
                    cbk_stderr=print_error)

    @classmethod
    def touch(cls, name):
        Shell.run('touch "{}"'.format(name))

    @classmethod
    def rm(cls, name):
        Shell.run('rm -r ' + name)

    @classmethod
    def shellrc(cls):
        return os.path.expanduser('~/.{}rc'.format(
            os.path.basename(os.environ['SHELL'])))

    @classmethod
    def cp(cls, src, dst):
        shutil.copy2(src, dst)

    @classmethod
    def mkdir(cls, name):
        if not os.path.isdir(name):
            os.makedirs(name)

    @classmethod
    def chmod(cls, fname, mode):
        os.chmod(fname, mode)

    @classmethod
    def isinPATH(cls, exe):
        return any(
            os.access(os.path.join(path, exe), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep))

    @classmethod
    def urldownload(cls, url, dst):
        import sys
        if sys.version_info[0] < 3:
            import urllib2 as urllib
        else:
            import urllib.request as urllib

        hstream = urllib.urlopen(url)
        with open(dst, 'wb') as f:
            f.write(hstream.read())


def c256(msg, c, background):
    if background:
        return '[38;5;{};7m{}[0m'.format(c, msg)
    else:
        return '[38;5;{}m{}[0m'.format(c, msg)
