import base
import bind
import apt

"""Initialize the module by creating a list of instansiated object of
search functions
"""

checkerslist = list()
checkerslist.append(base.Base()) 
checkerslist.append(bind.Bind()) 
checkerslist.append(apt.Apt()) 
