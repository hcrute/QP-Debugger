import xml.etree.ElementTree as ET

class qm_state:
	states = []
	trans = []
	glyph = None
	def __init__(self, name, level):
		self.name = name
		self.level = level
		
class qm_class:
	states = []
	
	def __init__(self, name, level):
		self.name = name
		self.level = level
		
level = 0
AO_flag = False
look_for = ["class", "state", "tran", "state_glyph"]
ret_obj = []
current_class = None
current_obj = None
current_state = None
state_flag = False
nested_states = False
def printRecur(root):
	global level
	global AO_flag
	global state_flag
	if root.tag == "state" and state_flag == False:
		level += 1
		state_flag = True
	elif root.tag == "class":
		level = 0
		state_flag = False
		
	if root.tag in look_for and AO_flag:
		add_to_object(root)
	if root.tag == "package":
		if root.attrib['name'] == "AOs":
			AO_flag = True
			
	nested = False
	for elem in root.getchildren():
		if "state" == root.tag and "state" == elem.tag and nested == False:
			level += 1
			nested = True
		printRecur(elem)

def add_to_object(obj):
	global class_flag
	global ret_obj
	global level
	global current_class
	global current_obj
	global current_state
	global nested_states
	
	if obj.tag == "class":
		new_class = qm_class(obj.attrib['name'], level)
		new_class.states = []
		ret_obj.append(new_class)
		current_class = new_class
		current_obj = new_class
		nested_states = False
	elif obj.tag == "state":
		new_state = qm_state(obj.attrib['name'], level)
		new_state.states = []
		new_state.trans = []
		if current_state == None:
			current_class.states.append(new_state)
			current_state = new_state
		elif nested_states == False:
			if level > current_state.level:
				current_state.states.append(new_state)
				current_obj = current_state
				nested_states = True
				current_state = new_state
			else:
				current_class.states.append(new_state)
				current_state = new_state
		else: #add nesting greater than 2 with "previous" pointer
			if level > current_obj.level:
				current_obj.states.append(new_state)
				current_state = new_state
			else:
				current_class.states.append(new_state)
				current_obj = new_state
	elif obj.tag == "tran":
		current_state.trans.append(obj)
	elif obj.tag == "state_glyph":
		current_state.glyph = obj
		
	#debug print
	#if current_class != None and current_obj != None and current_state != None:
		#print obj.tag.title(), level, current_class.name, current_obj.name, current_state.name
#make this file a copy of dpp.qm		
tree = ET.parse('Practice.qm')
root = tree.getroot()
printRecur(root)

for C in ret_obj:
	print "CLASS"
	print C.name
	for S in C.states:
		print "	STATE"
		print "	", S.name
		print "		Transitions"
		for t in S.trans:
			print "		", t.attrib['trig']
		
		for s in S.states:
			print "	SUBSTATE"
			print " 	", s.name
			print "		Transitions"
			for t in s.trans:
				print "		", t.attrib['trig']
				
				
'''
ret_obj - list of qm_class objects
qm_class	
	list of states
	name
	level - but this is used for parsing, probably not anything else
	
qm_state
	list of states
	list of transitions
	name
	
ret_obj -> GUI
'''
				
				

		
