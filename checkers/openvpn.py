"""
This file implements a class to determine all the files that are needed
for a fully configure bind environment
"""
from base import Base
import re
import os.path
import logging

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

class OpenVPN(Base):
    """
    Implement openvpn specific checks
    """
    _pkg_list = ['openvpn']
    _all_files = list()

    def set_debug(self, log_level):
        self.log = logging.getLogger("OpenVPN")
        self.log.setLevel(log_level)

    def do_check(self, pkg, dpkg_dir, dpkg_exe):
        "Overrule the funtion for our (Openvpn) purpose"
        if pkg not in self._pkg_list:
            return list()

        self.log.info('Processing for OpenVPN package')
        filelist = list()
        # Assume that if /etc/default/openvpn is changed it will be
        # tracked by the base package
        for root, subFolders, files in os.walk('/etc/openvpn'):
            for file_ in files:
                filelist.append(os.path.join(root, file_))
                self.log.debug('Adding file (%s)' % (file_))

        return filelist

