# Анализатор текста в императивном стиле программирования
def count_of_char(text, char):
	count = 0
	for c in text:
		if c == char:
			count+=1
	return count
while True:
	print ('ВАЖНО!\nФайл, который необходимо проанализировать на наличие букв кириллицы и их процентное соотношение должен находиться в одной папке с приложением!')
	file_input = str(input('Укажите название файла с расширением: '))
	with open(file_input, "rt") as f:
		text = f.read()

	for char in 'абвгдеёийклмнопрстуфхцчшщыьъэюя':
		percent = 100*count_of_char(text, char)/len(text)
		print('{0} - {1}%'.format(char, round(percent,2)))
		