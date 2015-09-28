#!/usr/bin/env python
#
#       configs.py
#       
#       Copyright 2009 Xion <Xion@UNREAL-093C4E1B>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from pyglet.graphics import Batch
from pyglet import resource
from pyglet.window import key

resource.path = ['resources']
resource.reindex()

ACCEL = 10
DECEL = 0.1
MAX_SPEED = 192
BULLET_SPEED = 288
BULLET_TIMEOUT = 10
DAMAGE = 5
SCREEN_W = 640
SCREEN_H = 480
FPS = 60.

PLAYER1_WIN_TEXT = 'Player-1 has won the battle!'
PLAYER2_WIN_TEXT = 'Player-2 has won the battle!'

graphics_batch = Batch()
bullets = []
snd_bullet = resource.media('zap1.wav', streaming=False)
snd_hit = resource.media('switch3.wav', streaming=False)

def load_pic(filename):
	pic = resource.image(filename)
	pic.anchor_x, pic.anchor_y = pic.width/2, pic.height/2
	return pic
options = {
'pause': key.P,
'back': key.Q,

'p1_left': key.A,
'p1_up': key.W,
'p1_right': key.D,
'p1_down': key.S,
'p1_fire': key.SPACE,
'p1_accel': '<High>',
'p1_decel': '<Low>',
'p1_color': '<Blue>',

'p2_left': key.LEFT,
'p2_up': key.UP,
'p2_right': key.RIGHT,
'p2_down': key.DOWN,
'p2_fire': key.ENTER,
'p2_accel': '<High>',
'p2_decel': '<Low>',
'p2_color': '<Violet>'
}

def get_color(color):
	if color == '<Red>': return (255, 72, 72)
	elif color == '<Orange>': return (255, 160, 72)
	elif color == '<Yellow>': return (255, 255, 72)
	elif color == '<Green>': return (72, 255, 72)
	elif color == '<Cyan>': return (72, 255, 255)
	elif color == '<Blue>': return (128, 128, 255)
	elif color == '<Violet>': return (255, 72, 255)
	elif color == '<Pink>': return (255, 160, 255)
	else: return (255, 255, 255)

def get_accel(accel):
	if accel == '<Low>': return 6
	elif accel == '<Medium>': return 8
	elif accel == '<High>': return 10
	else: return ACCEL

def get_decel(decel):
	if decel == '<Low>': return 0.1
	elif decel == '<Medium>': return 2
	elif decel == '<High>': return 4
	else: return DECEL

def collide(sp1, sp2):
	if sp1.image == None or sp2.image == None: return False
	if sp1.x - sp1.image.anchor_x > sp2.x - sp2.image.anchor_x + sp2.width: return False
	if sp1.x - sp1.image.anchor_x + sp1.width < sp2.x - sp2.image.anchor_x: return False
	if sp1.y - sp1.image.anchor_y > sp2.y - sp2.image.anchor_y + sp2.height: return False
	if sp1.y - sp1.image.anchor_y + sp1.height < sp2.y - sp2.image.anchor_y: return False
	return True

def get_sign(num):
	if num < 0: return -1
	else: return 1
