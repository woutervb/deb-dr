"""
This is the basic checker class. It tries to figure out which of the default
configu files (as shipped by the packager) are changed.
For this function the status file is used.

Deinstalled packages are omitted.
"""
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import re
import sys
import hashlib

global _status_data
_status_data = False    # caching
global _checked_list
_checked_list = set()   # caching

class Base(object):
    """
        Base class for all other checkers. The goal of the checker is to
        determine which files should end up in a backup.
        In this case based on md5 hash change.
    """
    def do_check(self, pkg, dpkg_exe, dpkg_dir):
        """
            This function wil perform the check and return a list of file
            that should end up in the backup.
        """
        _ret_list = list()
        self._retrieve_status(dpkg_dir)
        _file_md5 = self.find_cfg_files(pkg, dpkg_dir)
        for _file in _file_md5:
            if _file not in _checked_list:
                if self.file_changed(_file, _file_md5[_file]):
                    _ret_list.append(_file)
                    _checked_list.add(_file)
            else:
                return list()
        return _ret_list

    def hashfile(self, afile, hasher, blocksize=65536):
        "Helper function to calculate the hash from the give filehandle"
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher

    def file_changed(self, file_, md5_):
        """
        Helper function to determin if the file has a different md5 sum,
        or should be excluded based on other 'settings'
        """
        if md5_ == 'newconffile':
            return False
        md5 = hashlib.md5()
        try:
            self.hashfile(file(file_, 'rb'), md5)
        except IOError:
            return False
        except:
            print "Uexpected error:", sys.exc_info()[0]
            raise
        return md5.hexdigest() != md5_

    def _retrieve_status(self, dpkg_dir):
        "Private function to cache the status file"
        global _status_data
        if _status_data:
            return
        try:
            fh = open(dpkg_dir + 'status', 'r')
        except:
            pass
        _status_data = fh.readlines()
        fh.close()

    def find_cfg_files(self, pkg, dpkg_dir):
        """
        Helper function to search the cached data for config files of the 
        package
        """
        global _status_data
        _file_md5 = dict()
        
        # Packag named with + form a problem, so replace with wildcard
        _pkg = pkg.replace('+', '.')

        _in_conffile = False 
        _in_pkg_section = False
        re_pkg = re.compile(r'^Package: ' + _pkg + '$')
        re_conffiles = re.compile('^Conffiles:')
        re_file_md5 = re.compile(r" ([\w|\/|\.|-]+) (\w+)")
        re_description = re.compile('Description')
        for line in _status_data:
            if re_pkg.match(line):
                _in_pkg_section = True
            if _in_pkg_section:
                if re_conffiles.match(line):
                    _in_conffile = True
                if _in_conffile:
                    if re_description.match(line):
                        _in_conffile = False
                        _in_pkg_section = False
            if _in_conffile and _in_pkg_section:
                search = re_file_md5.search(line.rstrip())
                if search:
                    _file_md5[search.group(1)] = search.group(2)

        return _file_md5
