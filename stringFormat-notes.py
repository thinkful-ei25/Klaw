# % OPERATOR
message = 'Hello'
name = 'Bob'

# %s (string), %d (decimal), %x (hex), %f (floating)
print('Hello, %s' % name); 


# str.format()

print('Hello, {}'.format(name)); 

print('{message}, {name}'.format(message=message, name=name)); 

# f-Strings
print(f'Hello, {name}! You have {(2+4):#x} chickens')

#template strings
from string import Template
t = Template('Hey, $name!')
t.substitute(name=name)

#WHAT IS GOING ON HERE? Output is obj ref and not newly formatted string
print(t)
