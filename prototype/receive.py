import socket
import binascii
import time
from dict_analyzer import qspy_dict

class msg_analyzer:
    
    def __init__(self, queue):
        self.dict = qspy_dict()
        self.queue = queue
        UDP_IP = "127.0.0.1"
        UDP_PORT = 7701
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)

        values = [1,128]

        MESSAGE = bytearray(values)

        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        MESSAGE[0] = 2
        MESSAGE[1] = 0
        #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        #MESSAGE[0] = 3
        #MESSAGE[1] = 130
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        '''
        print "DICT"
        for obj in self.dict.objs:
            print obj
        for obj in self.dict.funcs:
            print obj
        for obj in self.dict.sigs:
            print obj
        for obj in self.dict.usrs:
            print obj
        '''
        while 1:
            data, addr = sock.recvfrom(4096)
            if bytearray(data)[1] == 6:
                data = bytearray(data)
                string = ""
                flag = False
                line = ""
                parsed = [[],[],[],[]]
                index = 0
                out_of_bounds_flag = False
                j = 0
                for d in data:
                    
                    line = line + str(d) + ' '
                    if d != 0 and j > 5:
                        if index < len(parsed):
                            parsed[index].append(d)
                        else:
                            print 'HERE' , ' ', line, ' ', data
                            out_of_bounds_flag = True
                        #string = string + str(d) + ' '
                        flag = True
                    else:
                        if flag:
                            index = index+1
                            #print string
                        flag = False
                        #string = ""
                    j = j + 1
                #print string 
                #print parsed[0]
                #print parsed[1]
                row_index = 0
                data = []
                for parse in parsed:
                    total = 0
                    index = 0
                    if len(parse) == 3:
                        parse.append(0)
                    for i in parse:
                        total = total + (pow(16, 2*index)*parsed[row_index][index])
                        index = index +1
                    row_index = row_index + 1
                    data.append(hex(total))
                    
                if not out_of_bounds_flag:
                    string = ""
                    string = string + self.compare_msg(data[1], 0) + " "
                    string = string + self.compare_msg(data[0], 2) + " "
                    string = string + self.compare_msg(data[2], 1) + " "
                    string = string + self.compare_msg(data[3], 1)
                    self.queue.put(string)
    def compare_msg(self, msg, index):
        msg = msg[2:]
        if index == 0:
            for data in self.dict.objs:
                if data[0].lower() == msg:
                    return data[len(data)-1]
                    
        elif index == 1:
            for data in self.dict.funcs:
                if data[0].lower() == msg:
                    return data[len(data)-1]
                    
        elif index == 2:
            for data in self.dict.sigs:
                if data[0].lower() == msg:
                    return data[len(data)-1]
                
