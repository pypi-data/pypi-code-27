import os
textfile = os.path.abspath('C:/Users/kyuha/Desktop/CP_Output/raw_images_1')
split = textfile.split(os.path.sep)
if split[0]=='C:' :
	split[0]='mnt'
	split[1]='mydata'
	join = os.path.join(*split)
	textfile = join
if textfile[-1] is not '/':
	textfile = textfile + '/'

print textfile