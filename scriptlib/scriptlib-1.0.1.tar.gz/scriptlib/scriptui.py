'''
ScriptUI
UI Manager for the scriptlib package
Developed by Orbtial
'''

#Custom imports


#Standard imports
import os, sys, time

def refresh():
	"""
	Clears the user interface
	"""
	os.system("tput reset; clear")

def colorise(text, color, newline):
	"""
	Colors output specified by input.
	Colors available are 'red', 'blue', 'green', 'cyan' and 'yellow'

	:param text: String that contains text to be printed.
	:param color: String indicating color of text displayed. Can be 'red', 'blue', 'green', 'cyan' or 'yellow'.
	:param newline: Boolean that indicates whether a newline should be appended after output.
	"""
	colors = {
		"red":"\033[1;31m",
		"blue":"\033[1;34m",
		"green":"\033[0;32m",
		"cyan":"\033[1;36m",
		"yellow":"\033[1;33m"
	}
	if color in colors: sys.stdout.write(colors[color])
	print(text) if newline else print(text, end='')
	sys.stdout.write("\033[0;0m")

def errorMessage(error):
	"""
	Displays an error message specified by the input.

	:param error: String containing error message to be displayed.
	"""
	colorise("<<Error: {}!>>".format(error), "red", True)
	time.sleep(0.5)

def cInt(question, minima, maxima):
	"""
	Obtains a valid integer from the user within the bounds specified.
	Meant for use within other functions.

	:param question: String containing prompt to be displayed.
	:param minima: Integer of lower bound of input.
	:param maxima: Integer of upper bound of input.
	"""
	try:
		ans = int(input(question))
	except:
		errorMessage("Invalid input")
		return [False]
	else:
		if minima <= ans and ans <= maxima:
			return [True, ans]
		else:
			errorMessage("Out of range")
			return [False]

def gInt(question, minima, maxima):
	"""
	Obtains a valid integer from the user within the bounds specified.
	Meant for user interfaces.

	:param question: String containing prompt to be displayed.
	:param minima: Integer of lower bound of input.
	:param maxima: Integer of upper bound of input.
	"""
	while True:
		refresh()
		ans = cInt(question, minima,maxima)
		if ans[0]:
			return ans[1]

def gList(question, items, returnsIndex):
	"""
	Returns an item or its index from a list based on user input.

	:param question: String containing prompt to be displayed.
	:param items: List of items of which user should choose from.
	:param returnsIndex: Boolean indicating whether the function should return the item or its index.
	:return: Item chosen by user from list or Integer specifying index of the item chosen.
	"""
	while True:
		refresh()
		print(question)
		[print("[{}] ".format(i+1) + str(items[i])) for i in range(len(items))]
		ans = cInt(": ", 1, len(items))
		if ans[0]:
			return ans[1]-1 if returnsIndex else items[ans[1]-1]

def gConfirm(question):
	"""
	Returns either True or False based on user input. Used as a confirmation prompt.

	:param question: String containing prompt to be displayed.
	:return: Boolean indicating the decision of the user.
	"""
	while True:
		refresh()
		ans = input(question + " [Y/N]: ").lower()
		if ans == "y":
			return True
		elif ans == "n":
			return False
		else:
			errorMessage("Invalid input")

def dGauge(title, withDetail, x, maxima, length, color):
	"""
	Displays a gauge interface element

	:param title: String containing title of gauge to be displayed. Can be left as an empty string.
	:param withDetail: Boolean indicating whether gauge should display additional details under the gauge on a newline.
	:param x: Integer containing current value of gauge.
	:param maxima: Integer containing maximum value of gauge.
	:param length: Integer indicating the width of the gauge in characters.
	:param color: String indicating color of gauge displayed. Leave as an empty string for intelligent color scheme based on percentage.
	"""
	print(title, end="")
	percentage = min(x, maxima)/maxima
	units = round(percentage*length*8, 0)
	filledUnits = int(units//8); partialUnits = int(units%8)
	bar = filledUnits * "█" + ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][partialUnits]
	bar += (length - filledUnits - (1 if partialUnits > 0 else 0)) * " "
	payload = "▏{}▕".format(bar)
	if withDetail: payload += "\n[{}/{}]".format(x, maxima)
	if color == "":
		if percentage > 0.5: colorise(payload, "green", True)
		elif percentage > 0.3: colorise(payload, "yellow", True)
		else: colorise(payload, "red", True)
	else:
		colorise(payload, color, True)
	
