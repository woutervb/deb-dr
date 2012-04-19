import base
import bind
import apt
import openvpn
import udev
import netbase

"""Initialize the module by creating a list of instansiated object of
search functions
"""

checkerslist = list()
checkerslist.append(base.Base()) 
checkerslist.append(bind.Bind()) 
checkerslist.append(apt.Apt()) 
checkerslist.append(openvpn.OpenVPN()) 
checkerslist.append(udev.Udev()) 
checkerslist.append(netbase.NetBase()) 
