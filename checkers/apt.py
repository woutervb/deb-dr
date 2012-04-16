"""
This file implements a class to determine all the files that are needed
for a fully configure apt
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from base import Base
import logging
import os
import sys

class Apt(Base):
    """
    Implement apt specific checks
    """
    _apt_list = ['apt']

    def set_debug(self, log_level):
        self.log = logging.getLogger("Apt")
        self.log.setLevel(log_level)

    def do_check(self, pkg, dpkg_dir, dpkg_exe):
        "Overrule the funtion for our (apt) purpose"
        if pkg not in self._apt_list:
            return list()

        self.log.info('Processing for Apt package')
        filelist = list()
        for root, subFolders, files in os.walk('/etc/apt'):
            for file_ in files:
                filelist.append(os.path.join(root, file_))
                self.log.debug('Adding file (%s)' % (file_))

        return filelist
