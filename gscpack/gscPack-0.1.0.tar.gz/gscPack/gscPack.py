import os

class gscFile(object):
    
    path = "default.txt"
    #lbl = label.lbl("")
    text = ""
    ntext = ""
    #__row = []
    row = []
    template_path = ""
    template_name = ""
    cft = False

    def __init__(self, new_path, template_path = "gsc_templates", template_name = "template_blank.txt", check_for_template = False):
        
        self.path = new_path
        self.template_path = template_path
        self.template_name = template_name
        self.cft = check_for_template

        self._init1_()

    def _init1_(self):
        try:
            with open(self.path,'r') as file:
                self.text = file.read()
            #print(new_path + " Found")

            #In the future, include something that will add a new line character if it isn't the last character in the file.

            self.text = self.text.split("\n")
            self.lbl = lbl(self.text[0])

            #self.__row = []
##            self.row = []

##            for i in range(len(self.text) - 2):
##                self.__row.append(self.text[i + 1])
##
##            self.row = self.__truncation(self.__row)

            self.row = self.line2list(self.text)
        
        except FileNotFoundError:
            self.new_file()

    def line2list(self, text):

        ntext = []
        
        for i in range(len(text) - 2):
            ntext.append(text[i + 1])

        return self.__truncation(ntext)
            
    def read_template(self):
        while(True):
            try:
                with open((self.template_path + "/" + self.template_name),'r') as file:
                    template = file.read()
                    template = template.split("\n")
                    return template

            except FileNotFoundError:

                print("No Template found. Template Created.")

                with open((self.template_path + "/" + self.template_name),'w') as file:
                    file.write("`1`\n 1 \n")
                print("Template " + self.template_name + " Created at " + self.template_path)
                    
                #print("No template found. Blank template created.")
                print("Please modify " + self.template_name + " found at " + self.template_path + " to fit specifications.")
                jfc = input("Press enter to continue.")
                
                
    def new_file(self):

        template = ""
        os.makedirs(self.template_path, exist_ok = True)

        #try:
##            with open((template_path + "/" + template_name),'r') as file:
##                template = file.read()
##                templatel = ("\n").split(template)
##                template = templatel[0]

        with open(self.path,'w') as file:
             file.write(self.read_template()[0])

        print(self.path + " Created from Template found in " + self.template_path)

        #except FileNotFoundError:
                
           

        self.__init__(self.path, template_path = self.template_path, template_name = self.template_name, check_for_template = self.cft)
        

    def new_row(self, para_list):
        temp = self.line2list(self.read_template())
        nlist = []
        j = 0
        for i in range(len(self.lbl.units)):
            if(temp[0][i] == "?"):
                nlist.append(para_list[j])
                j += 1
            else:
                nlist.append(temp[0][i])

        #nlist = self.__format(nlist)
        self.row.append(nlist)
        #print(self.row)

    def save(self):

        self.ntext += self.text[0]
        self.ntext += "\n"

        for i in range(len(self.row)):

            self.ntext += self.__format(self.row[i])
            self.ntext += "\n"

        with open(self.path,'w') as file:
            file.write(self.ntext)

        self._init1_()

    def __truncation(self, rows):

        #The first section divides each row into a list of strings
        #---------------------------------------------------------
        nrows = []
        
        for i in range(len(rows)):
            
            nrows.append(rows[i].split(" "))
            
            rows[i] = []
            
            for j in range(len(nrows[i])):
                
                if(nrows[i][j] != ""):
                    rows[i].append(nrows[i][j])
 
        return rows

    def __format(self, row, combine = True):

        text = " "

        for i in range(len(row)):
            
            row[i] = row[i] + (" " * ((len(self.lbl.pre_units[i]) - len(row[i]) + 2)))
            text += row[i]
        if(combine == True):
            return text
        elif(combine == False):
            return row

    def lbl_row(self, index, string, place = "none"):

        if(place == "none"):
            return self.row[index][self.lbl.unit_order[string]]
        else:
            self.row[index][self.lbl.unit_order[string]] = place

class lbl(object):

    pre_units = []
    unit_order = {}
    units = []

    def __init__(self, string):

        self.pre_units = string.split("`")[1:-1]
        self.units = self.__truncation(self.pre_units)

        for i in range(len(self.units)):
            self.unit_order[self.units[i]] = i

    def __truncation(self, unit_list):

        for i in range(len(unit_list)):

            temp = ""
            count = 0
            unit = unit_list[i]
            
            for j in range(len(unit)):

                if(unit[j] == " "):
                    temp += unit[j]
                    count += 1
                elif(unit[j] != "`"):
                    temp += unit[j]
                    count = 0

            unit_list[i] = temp[0:(-1 * count)]

        return unit_list
        

    def format(self):
        jfc = True
