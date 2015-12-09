#!/usr/bin/python


'''
		first is <->
		second is >-<
'''

import math
import pygame
import getopt
import sys
import random
import string
import xlrd
import xlwt 
from xlutils.copy import copy

# style

DISPLAY_SZ = (1200,800,)
DISPLAY_BGCOLOR = (20,20,20,)
ARROW_COLOR = (255,255,255,)
ARROW_MARGIN = 60
ARROW_YPOS = 240
ARROW_POINTERS_SZX = 40
CAPTION_COLOR = (200, 200, 200,)
CAPTION_POS = (DISPLAY_SZ[0] / 2 - 200, 120,)
UI_PACE = 10

TESTING_SERIES_SZ = 5
TESTING_SESSIONKEY_SZ = 9

class Game(object):
	def __init__(self, *argv, **kwargs):
		ls = kwargs.pop('lengths', None)
		if (ls is not None and ls != (None, None,)):
			self.lengths = map(int, ls)
		else:
			self.lengths = None
		self.angle = float(kwargs.pop('angle', None))
		self.screen = kwargs.pop('screen', None)
		
	def get_basic_pos(self):
			basic_f = (DISPLAY_SZ[0]/2 + ARROW_MARGIN, ARROW_YPOS)
			basic_s = (0               + ARROW_MARGIN, ARROW_YPOS)
			return (basic_f, basic_s,)
		
	def draw_arrows(self):
		self.screen.fill(DISPLAY_BGCOLOR)
		
		font = pygame.font.Font(None, 36)
		text = font.render("Press SPACE to submit", 1, CAPTION_COLOR)
		self.screen.blit(text, CAPTION_POS)

		basic_f, basic_s = self.get_basic_pos()
		dx = ARROW_POINTERS_SZX
		
		dy = dx * math.tan(math.radians(self.angle))
		
		## first
		x,y = basic_f
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x+dx,y-dy), (x,y), (x+dx, y+dy),], 2)
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x,y), (x + self.lengths[0],y)], 2)
		x = x + self.lengths[0]
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x-dx,y-dy), (x,y), (x-dx, y+dy),], 2)

		## second
		x,y = basic_s
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x-dx,y-dy), (x,y), (x-dx, y+dy),], 2)
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x,y), (x + self.lengths[1],y)], 2)
		x = x + self.lengths[1]
		pygame.draw.lines(self.screen, ARROW_COLOR, False, [(x+dx,y-dy), (x,y), (x+dx, y+dy),], 2)
	
	def finalize(self):
		return self.lengths
	
	def run(self):
		if (self.lengths is None):
			print 'lengths are None, abort'
			return 0
		if (self.screen is None):
			print 'screen is None, setting default'
			self.screen = pygame.display.set_mode((640,480,))
		if (self.angle is None):
			print 'angle is None, setting default'
			self.angle = 45

		mainloop = True
		while mainloop:
			self.draw_arrows()
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
							self.lengths[0] -= UI_PACE
							self.draw_arrows()
					elif event.key == pygame.K_RIGHT:
							self.lengths[0] += UI_PACE
							self.draw_arrows()
					elif event.key == pygame.K_SPACE:
							return self.finalize()
				if event.type == pygame.MOUSEBUTTONDOWN:
					return self.finalize()
			pygame.display.flip()

	
def runtest(*argv, **kwargs):	
	# some core config
#    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
	screen = pygame.display.set_mode(DISPLAY_SZ)
	pygame.mouse.set_visible(True)
	lengths = kwargs.pop('lengths', None)
	angle = kwargs.pop('angle', None)
	# instantiating the game
	game = Game(lengths = lengths, angle = angle, screen = screen)
	result = game.run()
	# when the game ends
	return result

def generate_fsa(n):
	f = random.randint(10,35) * 10
	s = random.randint(10,35) * 10
	a = random.randint(30,60)
	return (f,s,a,)

def runseries(n, user_id):
	pygame.init()
	results = []
	for test_n in range(n):
		f,s,a = generate_fsa(n)
		results.append(runtest(lengths = (f,s,), angle = a))
	pygame.quit()
	return results

def main():
	u = str(raw_input('username > '))

	sid = ''.join(random.choice(string.lowercase) for i in range(TESTING_SESSIONKEY_SZ))
	results = runseries(TESTING_SERIES_SZ, u)
	
	print 'results of {} sid {}'.format(u, sid)
	for result in results:
		print 'Svar = {}, Sst = {}'.format(result[0], result[1])

	try:
		rb = xlrd.open_workbook('results.xls', formatting_info=True)
	except Exception, e:
		rb = xlwt.Workbook()
		sh = rb.add_sheet('results')
		sh.write(0, 0, 'user id')
		sh.write(0, 1, 'session id')
		sh.write(0, 2, 'Sst')
		sh.write(0, 3, 'Svar')
		rb.save('results.xls')

	rb = xlrd.open_workbook('results.xls', formatting_info=True)
	r_sheet = rb.sheet_by_index(0) 
	r = r_sheet.nrows		
	wb = copy(rb)
	sheet = wb.get_sheet(0) 
	for result in results:
		sheet.write(r, 0, u)
		sheet.write(r, 1, sid)
		sheet.write(r, 2, str(result[1]))
		sheet.write(r, 3, str(result[0]))
		r += 1
	wb.save('results.xls')


if __name__ == "__main__":
	main()

'''
if __name__ == "__main__":
	f = None
	s = None
	a = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"f:s:a:",["first=","second=","angle="])
	except getopt.GetoptError:
		print '... -f <first length> -s <second length> -a <angle>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-f':
			f = arg
		if opt == '-s':
			s = arg
		if opt == '-a':
			a = arg
	runtest(lengths = (f,s,), angle = a)
'''

