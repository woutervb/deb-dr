#!/usr/bin/env python
"""
This file will implement the dpkg class
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import subprocess

class Dpkg:
    """This class will implement the internals of the dpkg handling"""
    def __init__(self, dpkg_exe='/usr/bin/dpkg', dpkg_dir='/var/lib/dpkg/'):
        """Set some local variables"""
        self._dpkg_exe = dpkg_exe
        self._dpkg_dir = dpkg_dir

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

if __name__ == '__main__':
    # No unit test implemented yet
    pass
