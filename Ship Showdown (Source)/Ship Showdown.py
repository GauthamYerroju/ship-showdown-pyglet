#!/usr/bin/env python
#
#       ShipShowdown.py
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

import pyglet
from pyglet.window import key
import math, random, sys

#from configs import *
#from Game import Game
#from Scene_Base import Scene_Base
#from ship import *
#from bullet import *
from data import *

game = Game()

class Scene_Game(Scene_Base, key.KeyStateHandler):
	
	global graphics_batch
	global bullets
	global game
	global options
	
	def on_enter(self):
		keys_1 = (options['p1_left'], options['p1_up'], options['p1_right'], options['p1_down'], options['p1_fire'])
		keys_2 = (options['p2_left'], options['p2_up'], options['p2_right'], options['p2_down'], options['p2_fire'])
		sp1 = 'ship.png'
		s1 = Ship(sp1, keys_1,
		get_accel(options['p1_accel']),
		get_decel(options['p1_decel']),
		get_color(options['p1_color']),
		batch=graphics_batch)
		s2 = Ship(sp1, keys_2,
		get_accel(options['p2_accel']),
		get_decel(options['p2_decel']),
		get_color(options['p2_color']),
		batch=graphics_batch,
		auto=True)
		s1.position = (10+s1.width/2, SCREEN_H/2)
		s2.position = (SCREEN_W-10-s2.width/2, SCREEN_H/2)
		s1.opponent, s2.opponent = s2, s1
		self.s1, self.s2 = s1, s2
		self.push_handlers(s1)
		self.push_handlers(s2)
		self.push_handlers(self)
		self.paused = False
		self.result_label = None
		self.result_phase = False
	
	def update(self, dt):
		if self[key.G]:
			game.change_scene(Scene_Menu())
			return
		if self[key.P]:
			self.paused = not self.paused
			return
		if self.paused: return
		self.s1.update(dt)
		self.s2.update(dt)
		if self.result_phase:
			for b in bullets: b.update(dt)
			if self[key.H]:
				game.change_scene(Scene_Menu())
			return
		# Damage when ships collide with each other
		if collide(self.s1, self.s2):
			snd_hit.play()
			snd_hit.play()
			self.s1.ouch(DAMAGE/2)
			self.s2.ouch(DAMAGE/2)
			self.s1.bounce(self.s2)
			self.s2.bounce(self.s1)
		# Bullet update
		for b in bullets:
			b.update(dt)
			if b.delete_flag:
				bullets.remove(b)
				b.delete()
			if collide(b, self.s1):
				self.s1.ouch(DAMAGE)
				snd_hit.play()
				b.delete_flag = True
			if collide(b, self.s2):
				self.s2.ouch(DAMAGE)
				snd_hit.play()
				b.delete_flag = True
		# Monitor health and end game
		if self.s1.hp <= 0:
			self.init_result_phase(PLAYER2_WIN_TEXT)
		elif self.s2.hp <= 0:
			self.init_result_phase(PLAYER1_WIN_TEXT)
	
	def init_result_phase(self, str):
		self.result_label = pyglet.text.Label(str, batch=graphics_batch,
		font_size=24, x=SCREEN_W/2, y=SCREEN_H/2, anchor_x='center', anchor_y='center')
		self.result_phase = True
	
	def on_draw(self):
		graphics_batch.draw()
	
	def on_exit(self):
		self.s1.delete()
		self.s2.delete()
		for b in bullets: b.delete()
		while len(bullets) > 0: bullets.pop()
		if self.result_label != None: self.result_label.delete()

class Scene_Menu(Scene_Base, key.KeyStateHandler):
	
	global graphics_batch
	global game
	
	def on_enter(self):
		self.commands = ['Start', 'Exit']
		self.labels = []
		for string in self.commands:
			label = pyglet.text.Label(string, font_name='Arial', font_size=24,
			anchor_x='center', anchor_y='center',
			color=(255, 255, 255, 255),
			batch = graphics_batch)
			self.labels.append(label)
		for i in (0, 1):
			self.labels[i].x = SCREEN_W/2
			self.labels[i].y = SCREEN_H/2 - 24 + (48*len(self.labels)) - 48*i
		self.index = 0
		self.set_index(0)
		self.key_timeout = 0
		self.repeat_timeout = 15
		self.push_handlers(self)
		ins_txt = 'G: Cancel/Back || H: Confirm/Forward'
		self.instruction_label = pyglet.text.Label(ins_txt, font_name='Arial', font_size=24,
		anchor_x='center', anchor_y='center', color=(255, 255, 255, 255),
		x=SCREEN_W/2, y=48, batch = graphics_batch)
	
	def update(self, dt):
		if self[key.H]:
			if self.index == 0:
				game.change_scene(Scene_PreStart())
			else: sys.exit()
		if self.key_timeout > 0: self.key_timeout -= dt * 60
		if self[key.UP] and self.key_timeout <= 0:
			self.set_index( (self.index + len(self.labels) - 1) % len(self.labels) )
			self.key_timeout = self.repeat_timeout = 15
		elif self[key.DOWN] and self.key_timeout <= 0:
			self.set_index( (self.index + 1) % len(self.labels) )
			self.key_timeout = self.repeat_timeout = 15
	
	def set_index(self, val):
		if val < 0 or val >= len(self.labels): return
		self.deselect(self.index)
		self.index = val
		self.select(self.index)
	
	def select(self, index):
		if index < 0 or index >= len(self.labels): return
		self.labels[self.index].font_size = 28
		self.labels[self.index].bold = True
		self.labels[self.index].color = (128, 128, 255, 255)
	
	def deselect(self, index):
		if index < 0 or index >= len(self.labels): return
		self.labels[self.index].font_size = 24
		self.labels[self.index].bold = False
		self.labels[self.index].color = (255, 255, 255, 255)
	
	def on_draw(self):
		graphics_batch.draw()
	
	def on_exit(self):
		for label in self.labels:
			label.delete()
		self.instruction_label.delete()


class Scene_PreStart(Scene_Base, key.KeyStateHandler):
	
	global graphics_batch
	global game
	global options
	
	def label(self, str, x, y, *args, **kwargs):
		l = pyglet.text.Label(str, font_name='Arial',
			anchor_x='center', anchor_y='center', x=x, y=y,
			color=(255, 255, 255, 255),
			batch = graphics_batch,
			*args, **kwargs)
		return l
	
	def control_text(self, player):
		if player == 1:
			text = \
			'''
			Controls
			
			Left: %s
			Right: %s
			Up: %s
			Down: %s
			Fire: %s
			Pause: %s
			''' % (key.symbol_string(options['p1_left']),
			key.symbol_string(options['p1_right']), key.symbol_string(options['p1_up']),
			key.symbol_string(options['p1_down']), key.symbol_string(options['p1_fire']),
			key.symbol_string(options['pause']))
		else:
			text = \
			'''
			Controls
			
			Left: %s
			Right: %s
			Up: %s
			Down: %s
			Fire: %s
			Pause: %s
			''' % (key.symbol_string(options['p2_left']),
			key.symbol_string(options['p2_right']), key.symbol_string(options['p2_up']),
			key.symbol_string(options['p2_down']), key.symbol_string(options['p2_fire']),
			key.symbol_string(options['pause']))
		return text
	
	def setup_game(self):
		options['p1_color'] = self.colors[self.col_index[0]][0]
		options['p1_accel'] = self.accels[self.acc_index[0]][0]
		options['p1_decel'] = self.decels[self.dec_index[0]][0]
		
		options['p2_color'] = self.colors[self.col_index[1]][0]
		options['p2_accel'] = self.accels[self.acc_index[1]][0]
		options['p2_decel'] = self.decels[self.dec_index[1]][0]
	
	def on_enter(self):
		p1 = self.label('Player 1', SCREEN_W/4-10, SCREEN_H-40, bold=True, font_size=22)
		p2 = self.label('Player 2', SCREEN_W/4*3+10, SCREEN_H-40, bold=True, font_size=22)
		c1 = self.label(self.control_text(1), p1.x-p1.content_width/2, 120, multiline=True, width=SCREEN_W/2-20, font_size=14)
		c2 = self.label(self.control_text(2), p2.x-p2.content_width/2, 120, multiline=True, width=SCREEN_W/2-20, font_size=14)
		self.other_labels = (p1, p2, c1, c2)
		# Color array
		self.colors, cols = [], ('<Red>', '<Orange>', '<Yellow>', '<Green>', '<Cyan>', '<Blue>', '<Violet>', '<Pink>')
		for c in cols:
			lc = get_color(c)
			tmp = (lc[0], lc[1], lc[2], 255)
			self.colors.append((c, tmp))
		# Accel array
		self.accels, accs = [], ('<Low>', '<Medium>', '<High>')
		for a in accs: self.accels.append((a, get_accel(a)))
		# Decel array
		self.decels, decs = [], ('<Low>', '<Medium>', '<High>')
		for d in accs: self.decels.append((d, get_decel(d)))
		
		self.col_index = [5, 3]
		self.acc_index = [2, 2]
		self.dec_index = [0, 0]
		
		self.labels = [[], []]
		# Player 1 Labels
		self.commands = ['Color: %s' % (options['p1_color']),
		'Accel: %s' % (options['p1_accel']),
		'Decel: %s' % (options['p1_decel'])]
		# Player 1 Labels
		for string in self.commands:
			label = pyglet.text.Label(string, font_name='Arial', font_size=18,
			anchor_y='center',
			color=(255, 255, 255, 255),
			batch = graphics_batch)
			self.labels[0].append(label)
		i = 1
		while (i <= len(self.commands)):
			self.labels[0][i-1].x = 20
			self.labels[0][i-1].y = SCREEN_H-72 - (28*i)
			i += 1
		# Player 2 Labels
		self.commands = ['Color: %s' % (options['p2_color']),
		'Accel: %s' % (options['p2_accel']),
		'Decel: %s' % (options['p2_decel'])]
		for string in self.commands:
			label = pyglet.text.Label(string, font_name='Arial', font_size=18,
			anchor_y='center',
			color=(255, 255, 255, 255),
			batch = graphics_batch)
			self.labels[1].append(label)
		i = 1
		while (i <= len(self.commands)):
			self.labels[1][i-1].x = SCREEN_W/2 + 20
			self.labels[1][i-1].y = SCREEN_H-72 - (28*i)
			i += 1
		self.index = [0, 0]
		self.set_index(1, 0)
		self.set_index(2, 0)
		self.key_timeout = 0
		self.repeat_timeout = 15
		self.push_handlers(self)
	
	def update(self, dt):
		if self[key.G]:
			game.change_scene(Scene_Menu())
			return
		if self[key.H]:
			self.setup_game()
			game.change_scene(Scene_Game())
		if self.key_timeout > 0: self.key_timeout -= dt * 60
		# Player 1
		if self[options['p1_up']] and self.key_timeout <= 0:
			self.set_index( 1, (self.index[0] - 1) % len(self.labels[0]) )
			self.key_timeout = self.repeat_timeout
		elif self[options['p1_down']] and self.key_timeout <= 0:
			self.set_index( 1, (self.index[0] + 1) % len(self.labels[0]) )
			self.key_timeout = self.repeat_timeout
		if self[options['p1_right']] and self.key_timeout <= 0:
			self.key_timeout = self.repeat_timeout
			# Color
			if self.index[0] == 0:
				self.col_index[0] += 1
				self.col_index[0] %= len(self.colors)
				self.labels[0][self.index[0]].color = self.colors[self.col_index[0]][1]
				self.labels[0][self.index[0]].bold = True
				self.labels[0][self.index[0]].text = 'Color: %s' % (self.colors[self.col_index[0]][0])
			# Accel
			elif self.index[0] == 1:
				self.acc_index[0] += 1
				self.acc_index[0] %= len(self.accels)
				self.labels[0][self.index[0]].text = 'Accel: %s' % (self.accels[self.acc_index[0]][0])
			# Decel
			elif self.index[0] == 2:
				self.dec_index[0] += 1
				self.dec_index[0] %= len(self.decels)
				self.labels[0][self.index[0]].text = 'Decel: %s' % (self.decels[self.dec_index[0]][0])
		elif self[options['p1_left']] and self.key_timeout <= 0:
			self.key_timeout = self.repeat_timeout
			# Color
			if self.index[0] == 0:
				self.col_index[0] -= 1
				self.col_index[0] %= len(self.colors)
				self.labels[0][self.index[0]].color = self.colors[self.col_index[0]][1]
				self.labels[0][self.index[0]].bold = True
				self.labels[0][self.index[0]].text = 'Color: %s' % (self.colors[self.col_index[0]][0])
			# Accel
			elif self.index[0] == 1:
				self.acc_index[0] -= 1
				self.acc_index[0] %= len(self.accels)
				self.labels[0][self.index[0]].text = 'Accel: %s' % (self.accels[self.acc_index[0]][0])
			# Decel
			elif self.index[0] == 2:
				self.dec_index[0] -= 1
				self.dec_index[0] %= len(self.decels)
				self.labels[0][self.index[0]].text = 'Decel: %s' % (self.decels[self.dec_index[0]][0])
		# Player 2
		if self[options['p2_up']] and self.key_timeout <= 0:
			self.set_index( 2, (self.index[1] - 1) % len(self.labels[1]) )
			self.key_timeout = self.repeat_timeout
		elif self[options['p2_down']] and self.key_timeout <= 0:
			self.set_index( 2, (self.index[1] + 1) % len(self.labels[1]) )
			self.key_timeout = self.repeat_timeout
		if self[options['p2_right']] and self.key_timeout <= 0:
			self.key_timeout = self.repeat_timeout
			# Color
			if self.index[1] == 0:
				self.col_index[1] += 1
				self.col_index[1] %= len(self.colors)
				self.labels[1][self.index[1]].color = self.colors[self.col_index[1]][1]
				self.labels[1][self.index[1]].bold = True
				self.labels[1][self.index[1]].text = 'Color: %s' % (self.colors[self.col_index[1]][0])
			# Accel
			elif self.index[1] == 1:
				self.acc_index[1] += 1
				self.acc_index[1] %= len(self.accels)
				self.labels[1][self.index[1]].text = 'Accel: %s' % (self.accels[self.acc_index[1]][0])
			# Decel
			elif self.index[1] == 2:
				self.dec_index[1] += 1
				self.dec_index[1] %= len(self.decels)
				self.labels[1][self.index[1]].text = 'Decel: %s' % (self.decels[self.dec_index[1]][0])
		elif self[options['p2_left']] and self.key_timeout <= 0:
			self.key_timeout = self.repeat_timeout
			# Color
			if self.index[1] == 0:
				self.col_index[1] -= 1
				self.col_index[1] %= len(self.colors)
				self.labels[1][self.index[1]].color = self.colors[self.col_index[1]][1]
				self.labels[1][self.index[1]].bold = True
				self.labels[1][self.index[1]].text = 'Color: %s' % (self.colors[self.col_index[1]][0])
			# Accel
			elif self.index[1] == 1:
				self.acc_index[1] -= 1
				self.acc_index[1] %= len(self.accels)
				self.labels[1][self.index[1]].text = 'Accel: %s' % (self.accels[self.acc_index[1]][0])
			# Decel
			elif self.index[1] == 2:
				self.dec_index[1] -= 1
				self.dec_index[1] %= len(self.decels)
				self.labels[1][self.index[1]].text = 'Decel: %s' % (self.decels[self.dec_index[1]][0])
	
	def set_index(self, player, val):
		if (val < 0 or val >= len(self.labels[player-1])): return
		self.deselect(player, self.index[player-1])
		self.index[player-1] = val
		self.select(player, self.index[player-1])
	
	def select(self, player, index):
		if index < 0 or index >= len(self.labels[player-1]): return
		self.labels[player-1][self.index[player-1]].font_size = 20
		self.labels[player-1][self.index[player-1]].bold = True
		if index == 0:
			self.labels[player-1][self.index[player-1]].color = self.colors[self.col_index[player-1]][1]
		else:
			self.labels[player-1][self.index[player-1]].color = (128, 128, 255, 255)
	
	def deselect(self, player, index):
		if index < 0 or index >= len(self.labels[player-1]): return
		self.labels[player-1][self.index[player-1]].font_size = 18
		self.labels[player-1][self.index[player-1]].bold = False
		if index == 0:
			self.labels[player-1][self.index[player-1]].color = self.colors[self.col_index[player-1]][1]
		else:
			self.labels[player-1][self.index[player-1]].color = (255, 255, 255, 255)
	
	def on_draw(self):
		graphics_batch.draw()
	
	def on_exit(self):
		for label in self.other_labels:
			label.delete()
		for player_labels in self.labels:
			for label in player_labels:
				label.delete()




game.change_scene(Scene_Menu())

pyglet.clock.schedule_interval(game.update, 1/FPS)

pyglet.app.run()
