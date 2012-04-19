"""
This file implements a class to determine all the files that are needed
for a fully configure apt
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from base import Base, file_iterator
import logging

class NetBase(Base):
    """
    Implement netbase specific checks
    """
    _pkg_list = ['netbase']

    def set_debug(self, log_level):
        self.log = logging.getLogger("Netbase")
        self.log.setLevel(log_level)

    def do_check(self, pkg, dpkg_dir, dpkg_exe):
        "Overrule the funtion for our (netbase) purpose"
        if pkg not in self._pkg_list:
            return list()

        self.log.info('Processing for Netbase package')

        return ['/etc/networking/interface', '/etc/hostname', '/etc/hosts']
