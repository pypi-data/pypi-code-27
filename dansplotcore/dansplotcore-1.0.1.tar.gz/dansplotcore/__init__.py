import os
import re
import sys
import time

LOC=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(LOC, 'danssfml', 'wrapper'))

try:
	import media
except:
	from danssfmlpy import media

class Plot:
	def __init__(self, title):
		self.title=title
		self.points=[]

	def point(self, x, y, r, g, b, a):
		self.points.append([x, y, r, g, b, a])

	def show(self):
		self._construct()
		media.init(title=self.title)
		media.custom_resize(True)
		done=False
		dragging=False
		mouse=[0, 0]
		view=None
		screen=None
		def move(view, dx, dy):
			view[0]-=dx*view[2]/media.width()
			view[1]-=dy*view[3]/media.height()
			media.set_view(*view)
		def zoom(view, zx, zy, x, y):
			#change view st (x, y) stays put and (w, h) multiplies by (zx, zy)
			new_view_w=view[2]*zx
			new_view_h=view[3]*zy
			view[0]+=1.0*x/media.width ()*(view[2]-new_view_w)
			view[1]+=1.0*y/media.height()*(view[3]-new_view_h)
			view[2]=new_view_w
			view[3]=new_view_h
			media.set_view(*view)
		while not done:
			#handle events
			while True:
				event=media.poll_event()
				if not event: break
				#quit
				if event=='q': done=True; break
				#resize
				m=re.match(r'rw(\d+)h(\d+)', event)
				if m:
					w, h=(int(i) for i in m.groups())
					if not view:
						view=[0, 0, w, h]
						media.set_view(*view)
					else:
						zoom(view, 1.0*w/screen[0], 1.0*h/screen[1], w/2, h/2)
					screen=[w, h]
					break
				#left mouse button
				if event[0]=='b':
					dragging={'<': True, '>': False}[event[1]]
					if dragging:
						m=re.match(r'b<0x(\d+)y(\d+)', event)
						drag_prev=(int(i) for i in m.groups())
					break
				#mouse move
				m=re.match(r'x(\d+)y(\d+)', event)
				if m:
					mouse=[int(i) for i in m.groups()]
					if dragging:
						xi, yi=drag_prev
						dx, dy=mouse[0]-xi, mouse[1]-yi
						move(view, dx, dy)
						drag_prev=mouse
					break
				#mouse wheel
				if event.startswith('w'):
					delta=int(event[1:])
					z=1.25 if delta>0 else 0.8
					zoom(view, z, z, mouse[0], mouse[1])
				#keyboard
				m=re.match('<(.+)', event)
				if m:
					key=m.group(1)
					moves={
						'Left' : ( 10,   0),
						'Right': (-10,   0),
						'Up'   : (  0,  10),
						'Down' : (  0, -10),
					}
					if key in moves:
						move(view, *moves[key])
						break
					zooms={
						'a': (1.25, 1),
						'd': (0.80, 1),
						'w': (1, 1.25),
						's': (1, 0.80),
					}
					if key in zooms:
						zoom(view, *zooms[key], media.width()/2, media.height()/2)
						break
					if key=='Return': media.capture_start()
			#draw
			media.clear(color=(0, 0, 0))
			self.vertex_buffer.draw()
			##x axis
			i=view[0]+view[2]/8
			while i<view[0]+15*view[2]/16:
				s='{}'.format(i)
				media.text(s, x=i+2, y=view[1]+view[3]-10, h=8)
				media.line(xi=i, xf=i, y=view[1]+view[3], h=-12)
				i+=view[2]/8
			##y axis
			i=view[1]+view[3]/8
			while i<view[1]+15*view[3]/16:
				s='{}'.format(-i)
				media.text(s, x=view[0], y=i+2, h=8)
				media.line(x=view[0], w=12, yi=i, yf=i)
				i+=view[2]/8
			##display
			media.display()
			media.capture_finish('plot.png')
			time.sleep(0.01)

	def _construct(self):
		self.vertex_buffer=media.VertexBuffer(len(self.points))
		for i, point in enumerate(self.points):
			point[1]=-point[1]
			self.vertex_buffer.update(i, *point)
