"""
This file implements a class to determine all the files that are needed
for a fully configure apt
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

from base import Base, file_iterator
import logging

class Udev(Base):
    """
    Implement apt specific checks
    """
    _pkg_list = ['udev']

    def set_debug(self, log_level):
        self.log = logging.getLogger("Udev")
        self.log.setLevel(log_level)

    def do_check(self, pkg, dpkg_dir, dpkg_exe):
        "Overrule the funtion for our (udev) purpose"
        if pkg not in self._pkg_list:
            return list()

        self.log.info('Processing for udev package')

        return file_iterator('/etc/udev')
