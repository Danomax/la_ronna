#First Attempt to Make La Ronna Game in Kivy 
#For Android touch App

#Daniel Cortés 21-04-2017
#Aplicacion
from kivy.app import App
from kivy.core.window import Window
#contenedor
from kivy.uix.widget import Widget
#importar para contenedores de imagenes
from kivy.uix.image import Image
#Contenedor de textos, boton
from kivy.uix.label import Label
from kivy.uix.button import Button
#Constructor del codigo Kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
#Box Layout para texto de presentacion
from kivy.uix.boxlayout import BoxLayout
#reloj para la aplicacion
from kivy.clock import Clock

import random

Builder.load_string('''
<ChatanksWidget>:
  Image:
    source: 'chatanks.bmp'
    size: self.parent.size
    pos: self.parent.pos
    allow_stretch: True
    keep_ratio: False
  BoxLayout:
    orientation: 'vertical'
    center: self.parent.center
    pos: self.pos[0],300
    spacing: 130
    Label:
      color: root.text_colour
      font_size: 40
      text: 'DanoMax presents:'
    Label:
      color: root.text_colour
      font_size: 40
      text: 'La Ronna in the Lost World'
    Label:
      color: root.text_colour
      font_size: 40
      text: 'version 2017 for Android'
    Button: 
      color: root.text_colour
      font_size: 40
      text: 'A Jugar!'
      size: self.texture_size
        
''')

class ChatanksWidget(Label):
  text_colour = ObjectProperty([0, 0, 0, 1])
  #if press button change to stage 1:

class Sprite(Image):
  def __init__(self,**kwargs):
    super(Sprite,self).__init__(**kwargs)
    self.size = self.texture_size
    
class Background(Widget):
  def __init__(self,source):
    self.velocity = 0
    super(Background,self).__init__()
    self.image = Sprite(source=source)
    self.add_widget(self.image)
    self.size = self.image.size
    self.image_dupe = Sprite(source=source, x=self.width)
    self.add_widget(self.image_dupe)
    
  def update(self):
    self.image.x -=self.velocity
    self.image_dupe.x -=self.velocity
    if self.image.right <= 0:
      self.image.x = 0
      self.image_dupe.x = self.width
      
class Malo(Sprite):
  def __init__(self, **kwargs):
    super(Malo,self).__init__(**kwargs)
    self.velocity_y = 0
    self.velocity_x = 0
    self.gravity = -0.1
    self.walk_state =0
    self.hitting = False
    self.groundpos=0
  def update(self):
    self.y += self.velocity_y
    self.x += self.velocity_x
    if self.walk_state > 0:
      self.walk_state+=1  
    if self.walk_state > 60:
      self.walk_state=1
  def on_touch_down(self,*ignore):
    self.hitting = True
  def set_ground(self,groundpos):
    self.groundpos = groundpos
      
class Monkey(Malo):
  def __init__(self, pos):
    self.source = 'atlas://img/malos/monkey1'
    super(Monkey,self).__init__(source=self.source,pos=pos)
    self.jump_state = 0
    self.set_ground(pos[1])
  def update(self):
    super(Monkey,self).update()
    if self.walk_state > 0:
      self.velocity_x = -2.0
    if self.walk_state ==1:
      self.source = 'atlas://img/malos/monkey1'
    elif self.walk_state == 30:
      self.source = 'atlas://img/malos/monkey2'
    self.jumping = random.randint(0,500)
    if self.jumping == self.walk_state:
      self.velocity_y = 4.5
      source = 'atlas://img/malos/monkey3'
      self.jump_state = 1
    if self.jump_state == 1:
      self.velocity_y += self.gravity
      self.velocity_y = max(self.velocity_y,-10)
      if self.y < self.ground:
        self.velocity_y = 0
        self.y = self.ground
        self.jump_state = 0
        self.walk_state = 1
        self.source = 'atlas://img/malos/monkey1'     

class Fly(Malo):
  def __init__(self, pos):
    self.source = 'atlas://img/malos/fly1'
    super(Fly,self).__init__(source=self.source,pos=pos)
  def update(self):
    super(Fly,self).update()
    if self.walk_state > 0:
      self.velocity_x = -2.0
    self.velocity_y += self.gravity
    self.velocity_y = max(self.velocity_y,-10)
    if self.velocity_y < -10:
      self.velocity_y = random.randint(0,10)
    if self.y > self.groundpos:
      self.velocity_y = random.randint(3,8)
    if self.walk_state ==1:
      self.source = 'atlas://img/malos/fly1'
    elif self.walk_state == 30:
      self.source = 'atlas://img/malos/fly2'

class Rat(Malo):
  def __init__(self, pos):
    self.source = 'atlas://img/malos/rat1'
    super(Rat,self).__init__(source=self.source,pos=pos)
    self.ground = pos[1]
  def update(self):
    super(Rat,self).update()
    if self.walk_state > 0:
      self.velocity_x = -2.0
    if self.walk_state ==1:
      self.source = 'atlas://img/malos/rat1'
    elif self.walk_state == 30:
      self.source = 'atlas://img/malos/rat2'

      
class Ronna(Sprite):
  def __init__(self, pos):
    super(Ronna,self).__init__(source='atlas://img/ronna/stand',pos=pos)
    self.velocity_y = 0
    self.gravity = -0.1
    self.walk_state = 0
    self.jump_state = 0
    self.kick_state = 0
    self.punch_state = 0
    self.ground = pos[1]
  def update(self):
    if self.walk_state > 0:
      self.walk_state+=1
    if self.walk_state > 60:
      self.walk_state=1
    if self.walk_state ==1:
      self.source = 'atlas://img/ronna/right_walk1'
    elif self.walk_state == 30:
      self.source = 'atlas://img/ronna/right_walk2'
    if self.jump_state == 1:
      self.velocity_y += self.gravity
      self.velocity_y = max(self.velocity_y,-10)
      self.y += self.velocity_y
      if self.y < self.ground:
        self.velocity_y = 0
        self.y = self.ground
        self.jump_state = 0
        self.walk_state = 1
        self.source = 'atlas://img/ronna/right_walk1'
    
  def on_touch_down(self,*ignore):
    if self.walk_state==0:
      self.walk_state = 1
    elif self.walk_state>0:
      self.walk_state=0
      self.jump_state=1
      self.velocity_y = 5.0
      self.source = 'atlas://img/ronna/jump'
    
  
class Stage1Widget(Widget):
  def __init__(self):
    super(Stage1Widget, self).__init__()
    self.background1 = Background(source='img/sun.png')
    self.background1.velocity = 0
    self.background2 = Background(source='img/mount.png')
    self.background2.velocity = 0
    self.background3 = Background(source='img/ground.png')
    self.background3.velocity = 0
    self.add_widget(self.background1)
    self.add_widget(self.background2)
    self.add_widget(self.background3)
    self.size = self.background1.size
    self.ronna = Ronna(pos=(20,self.background3.y+self.background3.height))
    self.add_widget(self.ronna)
    self.malos = []
    nmalos = 50
    for i in range(1,nmalos):
      malotype = random.randint(200,300)
      if malotype > 0 and malotype < 100:
        self.malos.append(Rat(pos=((self.width+malotype)*i,self.background3.y+self.background3.height)))
        self.add_widget(self.malos[-1])
        self.malos[-1].walk_state = 1
      elif malotype > 100 and malotype < 200:
        self.malos.append(Monkey(pos=((self.width+malotype)*i,self.background3.y+self.background3.height)))
        self.add_widget(self.malos[-1])
        self.malos[-1].walk_state = 1
      elif malotype > 200 and malotype < 300:
        self.malos.append(Fly(pos=((self.width+malotype)*i,self.height/2)))
        self.add_widget(self.malos[-1])
        self.malos[-1].walk_state = 1
        self.malos[-1].set_ground(self.background3.y+self.background3.height)
    Clock.schedule_interval(self.update, 1.0/60.0)

  def update(self,*ignore):
    self.background1.update()
    self.background2.update()
    self.background3.update()
    self.ronna.update()
    for m in self.malos:
      m.update()
      if m.x < -self.width:
        self.malos.remove(m)
        self.remove_widget(m)

    if self.ronna.walk_state > 0:
      self.background2.velocity = 0.3
      self.background3.velocity = 1

class RonnaApp(App):
  def build(self):
    game = Stage1Widget()
    Window.size = game.size
    return game

if __name__ == "__main__":
  RonnaApp().run()