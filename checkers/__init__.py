import checkers.base
import checkers.bind

"""Initialize the module by creating a list of instansiated object of
search functions
"""

checkerslist = list()
checkerslist.append(checkers.base.Base()) 
checkerslist.append(checkers.bind.Bind()) 
