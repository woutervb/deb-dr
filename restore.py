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
            script = open(file_ + '.sh', 'wb')
        except IOError:
            print "Could not write the file: " + file_
            raise

        for item in self._file_to_backup:
            tar.add(item)
            self.log.debug('Adding item (%s)' % (item))

        tar.close()

        self.log.info("Writing restore script")
        script.write("""#!/bin/sh

export TMPDIR=`mktemp -d /tmp/restore.XXXXXX`
ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ { print NR + 1; exit 0; }' $0`
tail -n+$ARCHIVE $0 > $TMPDIR/restore.tar

sudo (cd / ; tar xf $TMPDIR/restore.tar etc/apt)
sudo apt-get update
sudo apt-get install -y """ )
        for pkg in self._package_list:
            script.write(" %s" % (pkg))
        script.write('\n')
        script.write('exit 0\n')
        script.write('\n\n')
        script.write('__ARCHIVE_BELOW__\n')

        fh = open(file_ + '.tar', 'rb')
        buf = fh.read(65536)
        while len(buf) > 0:
            script.write(buf)
            buf = fh.read(65536)
        fh.close()
        script.close()


if __name__ == '__main__':
    # No unit test yet
    pass
