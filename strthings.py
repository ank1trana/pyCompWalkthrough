import curses
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


first = 'John'
last = 'Doe'

message = first + ' ' + last + ' is a coder.'
print(message)

#formatted string

msg = f'{first} {last} is a coder.' 
print(msg)

#length of the string
print(len(message))
#change case
print(message.upper())
print(message)
#original string isnot modified
print(message.lower())

#index of char's first occurence
print(message.find('o'))

#replacement of string
print(message.replace('o','3'))
print(message)
#again replace doesnt change original

#below is boolean, find brings the index
print('Doe' in message)
#first char is caps
print(message.title())


#in operator
oh = "this is not a keyword either"
print('>>>>>>>>' + 'keyword' in oh)
#in the above concat was done first
