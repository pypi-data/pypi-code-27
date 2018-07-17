import StringIO as io
import json

# data = '{"filename":"results/result_00000002.jpg","tag":[{"person":32,"left":373,"right":515,"top":81,"bot":388},{"person":31,"left":439,"right":556,"top":65,"bot":384}]}'
# data = '{"filename":"results/result_00000056.jpg","tag":[{"car":28,"left":370,"right":719,"top":362,"bot":475}]}'

def check_Overlap(index,data):

	# jsonData=json.loads(io.StringIO((data).decode("utf-8")))
	jsonData=json.loads(data)

	# print(jsonData['tag'])
	# print(len(jsonData['tag']))

	left_arr = []
	right_arr = []
	top_arr = []
	bot_arr = []
	for i in xrange(len(jsonData['tag'])):
		try:
		
			if(jsonData['tag'][i]['car']):

				left_arr += [jsonData['tag'][i]['left']]
				right_arr += [jsonData['tag'][i]['right']]
				top_arr += [jsonData['tag'][i]['top']]
				bot_arr += [jsonData['tag'][i]['bot']]
				
				# print(jsonData['tag'][i])
		
		except:
			continue

	for i in xrange(len(left_arr)):
		for j in xrange(i+1,len(left_arr)):

			b111 = (left_arr[i] < left_arr[j]);
			b112 = (left_arr[i] > left_arr[j]);
			b221 = (right_arr[i] < right_arr[j]);
			b222 = (right_arr[i] > right_arr[j]);
			b331 = (top_arr[i] < top_arr[j]);
			b332 = (top_arr[i] > top_arr[j]);
			b441 = (bot_arr[i] < bot_arr[j]);
			b442 = (bot_arr[i] > bot_arr[j]);

			b121 = (left_arr[i] < right_arr[j]);
			b122 = (left_arr[i] > right_arr[j]);
			b211 = (right_arr[i] < left_arr[j]);
			b212 = (right_arr[i] > left_arr[j]);
			b341 = (top_arr[i] < bot_arr[j]);
			b342 = (top_arr[i] > bot_arr[j]);
			b431 = (bot_arr[i] < top_arr[j]);
			b432 = (bot_arr[i] > top_arr[j]);

			# Rectangles don't overlap

			b1 = b211 and b432;
			b2 = b211 and b341;
			b3 = b122 and b432;
			b4 = b122 and b341;

			if( (b1 or b2 or b3 or b4) != True ):
				# print(index,i,j,'Overlap Occured !!!')
				return True

	return False

def club_Array(arr):

	j = 0

	for i in xrange((len(arr)-1)):
		temp1 = arr[j]
		temp2 = arr[j+1]
		if (temp2 - temp1) < 40 :
			arr.remove(temp1)
		else:
			j += 1

def check_Accident(line_arr):
	
	if(len(line_arr)<40):
		return False
	
	bool_res = False
	result = []

	res = []
	
	for line in line_arr:
		res += [check_Overlap(0,line)]

	# print res
	
	for i in xrange(len(line_arr)-19):
		if(i<20):
			continue

		bool_temp = True

		for j in xrange(-20,19):
			if res[i+j] == False:
				bool_temp = False
				break

		if (bool_temp):
			# print i
			result += [i]
			bool_res = True
	
	club_Array(result)
	
	print result

	return bool_res


def find(result_filename):
	file = open(result_filename, 'r')

	line_arr = []

	for line in file:
		# check_Overlap(line)
		line_arr += [line]

	return check_Accident(line_arr)



# for i in xrange(len(line_arr)):
# 	# print i
# 	if check_Overlap(i,line_arr[i]):
# 		print i

# print check_Accident(line_arr)