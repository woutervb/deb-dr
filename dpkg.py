#!/usr/bin/env python
"""
This file will implement the dpkg class
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import subprocess
import checkers
import logging

class Dpkg:
    """This class will implement the internals of the dpkg handling"""
    def __init__(self, log_level, dpkg_exe='/usr/bin/dpkg', dpkg_dir='/var/lib/dpkg/'):
        """Set some local variables"""
        self.log = logging.getLogger("Dpkg")
        self.log.setLevel(log_level)
        self.loglevel = log_level
        self._dpkg_exe = dpkg_exe
        self._dpkg_dir = dpkg_dir
        self._config_checker_list = list()
        for checker in checkers.checkerslist:
            self._config_checker_list.append(checker)

    def make_dpkg_listing(self):
        """Make a listing of installed packages"""
        process = subprocess.Popen([self._dpkg_exe, '--get-selections'], 
            stdout=subprocess.PIPE)
        output =  process.communicate()[0]
        _new_list = list()
        for line in output.splitlines():
            (pkg, status) = line.split()
            if status == 'install':
                _new_list.append(pkg)
        return _new_list

    def find_altered_config(self, pkg):
        """Return a list of config files to be included based on the package
        name.
        """
        files = list()
        for checker in self._config_checker_list:
            checker.set_debug(self.loglevel)
            retval = checker.do_check(pkg, self._dpkg_exe, self._dpkg_dir)
            if retval:
                files.extend(retval)
                self.log.debug('Config file (%s) is changed' % (retval))
        return files

if __name__ == '__main__':
    # No unit test implemented yet
    pass
