import menusystem, sys
sys.path.append('../')
"""A simple example of the Menu System in action

   Author: Daniel Mikusa <dan@trz.cc>
Copyright: July 9, 2006
"""

# Handler functions
def save_name(data):
    print 'Called save_name with "' + data + '"'

def save_phone(data):
	print 'Called save_phone with "' + data + '"'

def save_street(data):
	print 'Called save_street with "' + data + '"'

def save_city(data):
	print 'Called save_city with "' + data + '"'

def save_state(data):
	print 'Called save_state with "' + data + '"'

def save_zip(data):
	print 'Called save_zip with "' + data + '"'

def done(value):
	return False
	
if __name__ == '__main__':
	xml = menusystem.XMLMenuGenie('save2.xml', 'example2')
	head2 = xml.load()
	head2.waitForInput()
