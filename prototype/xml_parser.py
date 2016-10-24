import xml.etree.ElementTree as ET
from Tkinter import *
import sys
import Queue
import threading
import random
import time
from receive import msg_analyzer

class gui_class:
    
    def __init__(self, name):
        self.name = name
        self.states = []
        self.transitions = []
        self.models = []
        
    def add_state(self, name, object):
        self.states.append((name, object))
        
    def add_transition(self, name, object):
        self.transitions.append((name, object))

class qm_state:
    states = []
    trans = []
    choices = []
    glyph = None
    def __init__(self, name, level):
        self.name = name.lower()
        self.level = level
        self.choices = []
        
class qm_class:
    states = []
    diagram = None
    def __init__(self, name, level):
        self.name = name.lower()
        self.level = level
        self.diagram = None


        

def unpackXML(root):
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
        unpackXML(elem)

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
        if(current_state.glyph == None):
            current_state.glyph = obj
        else:
            current_obj.glyph = obj
    elif obj.tag == "choice_glyph":
        current_state.choices.append(obj);
    elif obj.tag == "state_diagram":
        current_class.diagram = obj;
        
    #debug print
    #if current_class != None and current_obj != None and current_state != None:
        #print obj.tag.title(), level, current_class.name, current_obj.name, current_state.name
#make this file a copy of dpp.qm        


def draw_state(C, S, w, base_x, base_y, num, first_flag=False, state_model=None):
    if state_model is None:
        state_model = gui_class(S.name+str(num))
    else:
        m = gui_class(S.name+str(num))
        state_model.models.append(m)
        state_model = m
    if S.glyph != None: 
        coordinates =  S.glyph.attrib['node'].split(',')
        x = 5*int(coordinates[0])
        y = 5*int(coordinates[1])
        dx = 5*int(coordinates[2])
        dy = 5*int(coordinates[3])
        #draw the state rectangle
        rect = w.create_rectangle((base_x+x), base_y+y, (base_x+x+dx), (base_y+y+dy))
        text = w.create_text(((base_x+x)+(base_x+x+dx))/2, (base_y+y+15), text=S.name )
        state_model.add_state(S.name, rect)
        if first_flag: #draw the rectangle around the entire class
            data = C.diagram.attrib['size'].split(',')
            w.create_rectangle((base_x+x-15), (base_y+y-15), (base_x+x+5*int(data[0])), (base_y+y+15+5*int(data[1])))
            w.create_text(((base_x+x-15)+(base_x+x+5*int(data[0])))/2, (base_y+y+5*int(data[1])), text=C.name+" "+str(num))
             
    for T in S.trans:
        for child in T.getchildren():
            if child.tag == "tran_glyph" and child.getchildren() != None:
                if child.attrib['conn'] != None:
                    data = child.attrib['conn'].split(',')
                    if len(data) == 5:
                        x = 5*int(data[0])
                        y = 5*int(data[1])
                        dx = 5*int(data[4])
                        line = w.create_line((base_x+x), base_y+y, (base_x + x + dx), base_y+y)
                        state_model.add_transition(T.attrib['trig'].lower(), line)
                        text = w.create_text((x+dx+2*base_x)/2, base_y+y+7, text=T.attrib['trig'].lower())
                    elif len(data) == 7:
                        x1 = 5*int(data[0])
                        y1 = 5*int(data[1])
                        dx = 5*int(data[4])
                        dy = 5*int(data[5])
                        back = 5*int(data[6])
                        line = w.create_line((base_x+x1), base_y+y1, (base_x + x1 + dx), base_y+y1)
                        state_model.add_transition(T.attrib['trig'].lower(), line)
                        line = w.create_line((base_x+x1+dx), base_y+y1, (base_x + x1 + dx), (base_y+y1+dy))
                        state_model.add_transition(T.attrib['trig'].lower(), line)
                        line = w.create_line((base_x+x1+dx), (base_y+y1+dy), (base_x + x1 + dx + back), (base_y+y1+dy))
                        state_model.add_transition(T.attrib['trig'].lower(), line)
                        text = w.create_text((x1+2*base_x+dx)/2, base_y+y1+7, text=T.attrib['trig'].lower())
    for choice in S.choices:
        data = choice.attrib['conn'].split(',')
        if len(data) == 5:
            x = 5*int(data[0])
            y = 5*int(data[1])
            dx = 5*int(data[4])
            line = w.create_line((base_x+x), base_y+y, (base_x + x + dx), base_y+y)
            #figure out how to deal with this for the gui                   
        elif len(data) == 7:
            x1 = 5*int(data[0])
            y1 = 5*int(data[1])
            dx = 5*int(data[4])
            dy = 5*int(data[5])
            back = 5*int(data[6])
            line = w.create_line((base_x+x1), base_y+y1, (base_x + x1 + dx), base_y+y1)
            line = w.create_line((base_x+x1+dx), base_y+y1, (base_x + x1 + dx), (base_y+y1+dy))
            line = w.create_line((base_x+x1+dx), (base_y+y1+dy), (base_x + x1 + dx + back), (base_y+y1+dy))
    for s in S.states:
        draw_state(C, s, w, base_x, base_y, num, False, state_model)
    
    return state_model
    

def draw_class(C, w, base_x, base_y, num, list):
    first_flag = True
    model = gui_class(C.name+str(num))
    for S in C.states:
        if first_flag:
            model.models.append(draw_state(C, S, w, base_x, base_y, num, first_flag))
            first_flag = False
        else:
            model.models.append(draw_state(C, S, w, base_x, base_y, num))
            
    list.append(model)
    return list      
        
class Application(Frame):
    models = []
    def createWidgets(self, master):
        master.geometry('%dx%d+%d+%d' %(1000, 750, 0, 0))
        master.display_frame = Frame(master, width =1000, height = 700 )
        master.display_frame.pack(fill = "both", expand = True)
        w = Canvas(master.display_frame, width=1000, height=750)
        base_x = 10
        base_y = 0
        j = 1
        total_count = 0
        state_models = []
        for C in ret_obj:
            for i in range(0, int(AO_COUNT[j])):
                draw_class(C, w, base_x, base_y, i, state_models)
                total_count = total_count + 1
                if total_count % 2 == 0:
                    base_x = base_x +210
                    base_y = 0
                if total_count % 2 == 1:
                    base_y = 350
                    
            j = j + 1
            
        w.pack()
        self.models = state_models
        
        self.w = w
        self.find_gui_state("philo1", "hungry")
        self.reset_gui_class("philo1", self.models)
        '''
        for model in self.models:
            print model.name
            for mo in model.models:
                print " ", mo.name
                for m in mo.models:
                    print "     ", m.name
        '''
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)
        
    def set_queue(self, queue):
        self.queue = queue
        
    def find_gui_state(self, C, name):
        for model in self.models:
            if C in model.name:
                for m in model.models:
                    for s in m.states:
                        if name in s[0]:
                            self.w.itemconfig(s[1], fill="red")
                            return
                    if m.models != None:
                        self.find_states(m, name)
                            
    def find_states(self, m, name):
        for mo in m.models:
            for s in mo.states:
                if name in s[0]:
                    self.w.itemconfig(s[1], fill="red")
                    return
                if mo.models != None:
                    self.find_states(mo, name)
            
            
    def find_gui_trans(self, C, name):
        for model in self.models:
            if C in model.name:
                for m in model.models:
                    for t in m.transitions:
                        if name in t[0]:
                            self.w.itemconfig(t[1], fill="red")
                            return
                    if m.models != None:
                        self.find_trans(m, name)
                            
    def find_trans(self, m, name):
        for mo in m.models:
            for t in mo.transitions:
                if name in t[0]:
                    self.w.itemconfig(t[1], fill="red")
                    return
                if mo.models != None:
                    self.find_trans(mo, name)
                    
    
    def reset_gui_class(self, class_name, models):
        for model in self.models:
            if class_name in model.name:
                for m in model.models:
                    for s in m.states:
                        self.w.itemconfig(s[1], fill="grey")
                    for t in m.transitions:
                        self.w.itemconfig(t[1], fill="black")
                return
            #if model.models != None:
                #self.reset_gui_class(class_name, model)
            
    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                print msg
                
                msg = msg.split(' ')
                msg_c = msg[0]
                i = 0
                num = 0
                msg_class = ''
                for m in msg_c:
                    i = i + 1
                    if m == '[':
                        num = msg_c[i:i+1]
                for C in self.models:
                    if C.name[0:len(C.name)-1] in msg_c:
                        msg_class = C.name[0:len(C.name)-1]
                msg_trig = msg[1]
                msg_old = msg[2].split('_')[1]
                msg_new = msg[3].split('_')[1]
                self.reset_gui_class(msg_class+num, self.models)
                self.find_gui_state(msg_class+num, msg_new.lower())
            except Queue.Empty:
                pass
                
                
class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master, app):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = app
        self.gui.set_queue(self.queue)
        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
    	self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            msg_receiver = msg_analyzer(self.queue)
            #break

    def endApplication(self):
        self.running = 0
        
level = 0
AO_flag = False
look_for = ["class", "state", "tran", "state_glyph", "choice_glyph", "state_diagram"]
ret_obj = []
current_class = None
current_obj = None
current_state = None
state_flag = False
nested_states = False
AO_COUNT = []
if len(sys.argv) > 0:
    for arg in sys.argv:
        AO_COUNT.append(arg)

tree = ET.parse('Practice.qm')
root = tree.getroot()
unpackXML(root)
root = Tk()
app = Application(master=root)

rand = random.Random()

client = ThreadedClient(root, app)
app.mainloop()
try:
    root.destroy()
except:
    pass
'''
ret_obj - list of qm_class objects
qm_class    
    list of states
    name
    level - but this is used for parsing, probably not anything else
    
qm_state
    list of states
    list of transitions 
    state glyph
    name
    
ret_obj -> GUI
'''
                
                

        
