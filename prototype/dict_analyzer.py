from subprocess import check_output

class qspy_dict:
    usrs = []
    funcs = []
    sigs = []
    objs = []
    def __init__(self):
        self.usrs = []
        self.funcs = []
        self.sigs = []
        self.objs = []
        self.get_dict()
        self.trim_zeroes()
        
    def trim_zeroes(self):
        row_index = 0
        col_index = 0  
        
        for obj in self.objs:
            for data in obj:
                if data != None:
                    while data[:1] == '0':
                        data = data[1:]
                    self.objs[row_index][col_index] = data
                    col_index = col_index + 1
            row_index = row_index +1
            col_index = 0
                    
        row_index = 0
        col_index = 0           
        for obj in self.funcs:
            for data in obj:
                while data[:1] == '0':
                    data = data[1:]
                self.funcs[row_index][col_index] = data
                col_index = col_index + 1
            row_index = row_index +1
            col_index = 0
        
        row_index = 0
        col_index = 0
        for obj in self.sigs:
            for data in obj:
                while data[:1] == '0':
                    data = data[1:]
                if data == '':
                    data = '0'
                self.sigs[row_index][col_index] = data
                col_index = col_index + 1
            row_index = row_index +1
            col_index = 0
        
        row_index = 0
        col_index = 0        
        for obj in self.usrs:
            for data in obj:
                while data[:1] == '0':
                    data = data[1:]
                self.usrs[row_index][col_index] = data
                col_index = col_index + 1
            row_index = row_index +1
            col_index = 0
        
    def get_dict(self, path='C:/qp/qtools/bin/', win_path='C:\\qp\\qtools\\bin\\'):
        targets = check_output("dir "+win_path+"*.dic", shell=True)
        lines = targets.split("\n")

        target = ""
        for line in lines:
            if not line[:1].isspace():
                target = line 
                break
                
        line = target.split(' ')

        count = 0
        file = ""
        for data in line:
            
            if not data.isspace() and data != "":
                count = count + 1
                if count == 5:
                    file = data
                    break
                    
        path = path + file
        path = path[0:len(path)-1]

        f_h = open(path)
        OD = False
        FD = False
        UD = False
        SD = False

        Objects = []
        Functions = []
        Signatures = []
        Users = [] #don't use?
        for line in f_h:
            if line[:1] != '-':
                if "Obj-Dic" in line:
                    OD = True
                elif "Fun-Dic" in line:
                    FD = True
                elif "Usr-Dic" in line:
                    UD = True
                elif "Sig-Dic" in line:
                    SD = True
                elif "Msc-Dic" in line:
                    break
                    
                if SD:
                    self.sigs.append(line.rstrip().split(' '))
                elif UD:
                    self.usrs.append(line.rstrip().split(' '))
                elif FD:
                    self.funcs.append(line.rstrip().split(' '))
                elif OD:
                    self.objs.append(line.rstrip().split(' '))
                    

'''
print "DICT"
for obj in dict.objs:
    print obj
for obj in dict.funcs:
    print obj
for obj in dict.sigs:
    print obj
for obj in dict.usrs:
    print obj
'''
 

