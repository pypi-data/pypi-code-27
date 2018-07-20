class gscFile(object):
    path = "default.txt"
    #lbl = label.lbl("")
    text = ""
    ntext = ""
    __row = []
    row = []

    def __init__(self, new_path):
        
        self.path = new_path
        
        with open(new_path,'r') as file:
            self.text = file.read()

        self.text = self.text.split("\n")
        self.lbl = label.lbl(self.text[0])

        self.__row = []
        self.row = []

        for i in range(len(self.text) - 2):
            self.__row.append(self.text[i + 1])

        self.row = self.__truncation(self.__row)

    def new_row(self, para_list):

        temp = []
        for i in range(len(self.lbl.units)):
        #for i in range(len(para_list)):
            temp.append(para_list[i])

        temp = self.__format(temp, combine = False)
        self.row.append(temp)

    def save(self):

        self.ntext += self.text[0]
        self.ntext += "\n"

        for i in range(len(self.row)):

            self.ntext += self.__format(self.row[i])
            self.ntext += "\n"

        with open(self.path,'w') as file:
            file.write(self.ntext)

        self.__init__(self.path)

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
