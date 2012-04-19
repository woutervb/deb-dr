"""
This file implements a class to determine all the files that are needed
for a fully configure bind environment
"""
from base import Base, file_iterator
import re
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
        
        return file_iterator('/etc/openvpn')

