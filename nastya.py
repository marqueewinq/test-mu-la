#!/usr/bin/python


'''
        first is <->
        second is >-<
'''

import math
import pygame
import getopt
import sys

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

	
def main(*argv, **kwargs):	
	# some core config
	pygame.init()
#    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
	screen = pygame.display.set_mode(DISPLAY_SZ)
	pygame.mouse.set_visible(True)
	lengths = kwargs.pop('lengths', None)
	angle = kwargs.pop('angle', None)
	# instantiating the game
	game = Game(lengths = lengths, angle = angle, screen = screen)
	result = game.run()
	# when the game ends
	print 'Svar = {}, Sst = {}'.format(result[0], result[1])
	pygame.quit()

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
	main(lengths = (f,s,), angle = a)
