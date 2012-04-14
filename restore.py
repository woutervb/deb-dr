"""
This file will implement the restore Class so that we can create a 
restore script
"""

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os.path
import tarfile
import logging

class Restore(object):
    "The class that implements the restore part"
    _file_to_backup = set()
    _package_list = set()

    def __init__(self, log_level):
        self.log = logging.getLogger("Dpkg")
        self.log.setLevel(log_level)

    def add_files(self, file_list):
        "This function will check the list of files for reachability"
        for file_ in file_list:
            if os.path.exists(file_):
                try:
                    fh = open(file_, 'r')
                except IOError:
                    continue
                fh.close()
                self._file_to_backup.add(file_)

    def add_packages(self, package_list):
        "This function will add the packages for later use"
        for item in package_list:
            self._package_list.add(item)
    
    def create_file(self, file_):
        try:
            tar = tarfile.open(file_ + '.tar', 'w')
            script = open(file_ + '.sh', 'w')
        except IOError:
            print "Could not write the file: " + file_
            raise

        for item in self._file_to_backup:
            tar.add(item)
            self.log.debug('Adding item (%s)' % (item))

        tar.close()

        self.log.info("Writing restore script")
        script.write("""
#!/bin/sh

sudo (cd / ; tar xf %s etc/apt)
sudo apt-get update
sudo apt-get install -y """ % (file_ + '.tar',))
        for pkg in self._package_list:
            script.write(" %s" % (pkg))


if __name__ == '__main__':
    # No unit test yet
    pass
