import numpy as np

this = "Python's way to apostrophe"
oh = "this is not a keyword either"

triplestr = '''
this is where i can erite a whole para
like an email body
each new line has a \0 character being recorded as well.'''

#indexing 

print('zeroth index>>>>>',repr(triplestr[0]))
#last
print('last char: ',triplestr[-1])

#second from teh end
print('seclast char: ', triplestr[-2])

#ranges of chars
print(triplestr[0:15])

#all the way till the end
print(triplestr[0:])

#assume zero as start in below
print(triplestr[0:5])