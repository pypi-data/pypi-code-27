import pygame, pygame.mixer
from pygame.locals import*
import sys
#police = font
pygame.init()
pygame.font.init()

class Fontstring:

	def __init__(self, name=None, size=20, italic=0, bold=0, underline=0, window=None):
		self.font = pygame.font.Font(name, size)
		self.font.set_italic(italic)
		self.font.set_bold(bold)
		self.font.set_underline(underline)
		self.win = window

class Printstring:
	police = pygame.font.Font(None, 20)
	"""
	Policestr -> create a drawing string and the police
	police = pygame.font.Font()
	policename = the name of the police
	policesize = the size of the police
	txt = text to assign the police
	string = texte to print
	color = color of the string
	window = pygame.Surface()
	x and y = posiiton of the text
	"""
	def __init__(self, main_font, string="text", color=(0,0,0), x=0, y=0):
		self.txt = string
		self.string = main_font.font.render(string, True, color)
		self.color = color
		self.x = x
		self.y = y
		self.main_font = main_font
	"""update the printed string"""
	def refresh(self):
		self.string = self.main_font.font.render(self.txt, True, self.color)
	"""print the string"""
	def write(self):
		self.main_font.win.blit(self.string, (self.x, self.y))
	"""set the text to print"""
	def set_text(self, string):
		if type(string) is not str:
			string = str(string)
		self.txt = string
		self.refresh()
	"""return the text printed"""
	def get_text(self):
		return self.txt
	"""set the policename and his size"""
	def set_font(self, name=None, size=None):
		if name is not None:
			self.policename = name
		if size is not None:
			self.policesize = size
		self.main_font.font = pygame.font.Font(self.policename, self.policesize)
		self.refresh()
	"""set the style of the police"""
	def set_style(self, it=False, bd=False, ul=False):
		self.main_font.font.set_italic(it)
		self.main_font.font.set_bold(bd)
		self.main_font.font.set_underline(ul)
		self.refresh()
	"""concatenation"""
	def strcat(self, string):
		if type(string) is not str:
			string = str(string)
		self.txt += string
		self.refresh()

	"""concatenation with >>"""
	def __rshift__(self, string):
		if type(string) is not str:
			string = str(string)
		self.txt += string
		self.refresh()
	"""set the text of the string with <<"""
	def __lshift__(self, string):
		if type(string) is not str:
			string = str(string)
		self.txt = string
		self.refresh()
	"""up the policesize with +="""
	def __iadd__(self, fact):
		if fact < 0:
			return self
		self.set_font(size=int(self.policesize+fact))
		self.refresh()
		return self
	"""down the policesize with -="""
	def __isub__(self, fact):
		if fact < 0:
			return self
		self.set_font(size=int(self.policesize-fact))
		self.refresh()
		return self
	"""mult the policesize with *="""
	def __imul__(self, fact):
		if fact < 0:
			return self
		self.set_font(size=int(self.policesize*fact))
		self.refresh()
		return self
	"""divide the policesize with /="""
	def __itruediv__(self, fact):
		if fact < 0:
			return self
		self.set_font(size=int(self.policesize//fact))
		self.refresh()
		return self
	"""divide the policesize with //="""
	def __ifloordiv__(self, fact):
		if fact < 0:
			return self
		self.set_font(size=int(self.policesize//fact))
		self.refresh()
		return self
	"""return the text of the string with str(self)"""
	def __str__(self):
		return self.get_text()

	def __repr__(self):
		return "font: {}\nsize: {}\ntext: {}\ncolor: {}\nitalic: {}\nbold: {}\nunderline: {}".format(
			self.policename, self.policesize, self.txt, self.color,
			self.main_font.font.get_italic(), self.main_font.font.get_bold(), self.main_font.font.get_underline()
			)



