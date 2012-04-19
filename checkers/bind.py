"""
This file implements a class to determine all the files that are needed
for a fully configure bind environment
"""
from base import Base
import re
import os.path
import logging

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

class Bind(Base):
    """
    Implement bind specific checks
    """
    _pkg_list = ['bind9']
    _all_files = list()

    def set_debug(self, log_level):
        self.log = logging.getLogger("Bind")
        self.log.setLevel(log_level)

    def do_check(self, pkg, dpkg_dir, dpkg_exe):
        "Overrule the funtion for our (bind) purpose"
        _included_file_list = list()
        if pkg not in self._pkg_list:
            return list()

        self.log.info('Processing for Bind package')
        changed_list = ['/etc/bind/named.conf', ]
        for file_ in changed_list:
            self.bind_include_files(file_, _included_file_list)

        return _included_file_list

    def bind_include_files(self, file_, list_):
        "Check which files are included and referenced so we can include them"
        try:
            fh = open(file_, 'r')
        except IOError:
            return list()
        except:
            raise

        for line in fh.xreadlines():
            search = re.search(r'^include.+"(.+)"', line, re.I)
            if not search:
                search = re.search(r'.+file.+"(.+)"', line, re.I)
            if search:
                filename = search.group(1)
                if os.path.exists(filename):
                    list_.append(filename)
                    self.bind_include_files(filename, list_)


