class Brute:

    def __init__(self, path_to_settings, bruting_format, **kwargs):

        #CHECKING ARGUMENTS

        if type(path_to_settings) != str: raise Exception("path_to_settings type must be string, got {}".format(type(path_to_settings)))

        if type(bruting_format) != list and type(bruting_format) != str: raise Exception("bruting_format type must be list or str, got {}".format(type(bruting_format)))

        if "start" in kwargs.keys():

            if type(kwargs["start"]) != str and type(kwargs["start"]) != list: raise Exception("start type must be list or str, got {}".format(type(kwargs["start"])))

            start_arg = kwargs["start"]

        else: start_arg = None

        if "stop" in kwargs.keys():

            if type(kwargs["stop"]) != str and type(kwargs["stop"]) != list: raise Exception("stop type must be list or str, got {}".format(type(kwargs["stop"])))

            stop_arg = kwargs["stop"]

        else: stop_arg = None

        if "dump" in kwargs.keys():

            dump_dict = kwargs["dump"]

            if "path" not in dump_dict.keys(): raise Exception("path needed when dumping")

            self.dump_path = dump_dict["path"]

            if "clear" in dump_dict.keys():
                if dump_dict["clear"]: open(self.dump_path,"w+").write("")

            self.dump_file = open(self.dump_path,"a+")

        else: self.dump_file = None
            
        #CONFIGURING

        self.has_finished = False
        
        self.LoadSettings(path_to_settings)

        self.LoadFormat(bruting_format)

        if start_arg != None: self.LoadStart(start_arg)

        if stop_arg  != None: self.LoadStop(stop_arg)

        self.password_counter = 0
        
        self.CalculatePasswordNumber()

        #FIXING

        self.stop_indexes[-1] += 1

    #CONFIG METHODS

    def LoadSettings(self,path_to_settings):
        
        self.settings = {}
        lists = {}

        file_lines = open(path_to_settings).read().split("\n")
        for line in file_lines:

            if line == "" or line[0] == "#": continue
            
            pieces = line.split(" ")
            
            if pieces[1] == "<":
                
                lists[pieces[0]] = pieces[2].split(",")

            elif pieces[1] == "<<":

                    try:
                        lists[pieces[0]] = open(pieces[2]).read().split(pieces[3])
                    except:
                        lists[pieces[0]] = open(pieces[2]).read().split("\n")

            elif pieces[1] == "=":

                self.settings[pieces[0]] = []
                for list_name in pieces[2].split("+"):
                    self.settings[pieces[0]] += lists[list_name]

    def LoadFormat(self,bruting_format):

        self.format_string    = ""
        self.password_indexes = []
        self.stop_indexes     = []
        self.specified_lists  = []

        if type(bruting_format) == str:
            format_list = bruting_format.split(" ")
        else:
            format_list = bruting_format


        for f in format_list:

            if len(f) <= 1: self.format_string += f; continue

            self.password_indexes.append(0)
            self.stop_indexes.append(len(self.settings[f])-1)
            self.specified_lists.append(f)
            self.format_string += "{}"

    def LoadStart(self,start_arg):

        if type(start_arg) == list:

            self.password_indexes = start_arg

        else:

            self.password_indexes = self.Password_to_indexes(start_arg)

    def LoadStop(self,stop_arg):

        if type(stop_arg) == list:

            self.stop_indexes = stop_arg

        else:

            self.stop_indexes = self.Password_to_indexes(stop_arg)

    def Password_to_indexes(self,password):

        indexes = []

        temp_format = self.format_string.replace("{}","|")

        format_indexes = [i for i, c in enumerate(temp_format) if c == "|"]

        i = 0
            
        for index in format_indexes:

            char_at_index  = password[index]
                
            listName_for_index = self.specified_lists[i]
            list_for_index = self.settings[listName_for_index]

            i += 1

            indexes.append(list_for_index.index(char_at_index))

        return indexes

    def ListForIndex(self,index):

        listName_for_index = self.specified_lists[index]
        list_for_index = self.settings[listName_for_index]

        return list_for_index

    def CalculatePasswordNumber(self):

        self.password_number = 0

        indexes = list(self.password_indexes)
        stop    = list(self.stop_indexes)

        for i in range(len(indexes)-1,-1,-1):

            molt = 1
            for j in range(i+1,len(indexes)):
                molt *= len(self.ListForIndex(j))

            if stop[i] < indexes[i]: self.CPN_Riporto(i,stop)

            num = stop[i] - indexes[i]
            num *= molt
            self.password_number += num

    def CPN_Riporto(self,index,indexes):

        done = False
        i = index - 1
        
        while not done:

            if indexes[i] > 0: indexes[i]-=1; done = True
            else: indexes[i] = len(ListForIndex(i))-1; i -= 1

    #GENERATOR METHODS

    def Indexes_to_password(self,indexes):

        chars = []
        for i in range(len(indexes)):
            lista = self.ListForIndex(i)
            chars.append(lista[indexes[i]])

        return self.format_string.format(*chars)

    def UpdateIndexes(self):

        done = False
        i    = len(self.password_indexes) - 1

        while not done:

            self.password_indexes[i] += 1

            if self.password_indexes[i] == len(self.ListForIndex(i)): self.password_indexes[i] = 0; i -= 1
            else: done = True

    def GetPassword(self):

        if self.password_indexes == self.stop_indexes:
            self.has_finished = True

        if self.has_finished: return False

        password = self.Indexes_to_password(self.password_indexes)

        self.UpdateIndexes()

        if self.dump_file != None: self.dump_file.write(password + "\n"); self.dump_file.close(); self.dump_file = open(self.dump_path,"a+")

        return password
        
