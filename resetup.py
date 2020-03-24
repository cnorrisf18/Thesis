from kivy.config import Config
Config.set('graphics','resizable', 0)
Config.set('graphics','fullscreen',0)
Config.set('graphics','window_state','maximized')
Config.write()
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import GUI, Players, Animal
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
#from textgame import Setup, Action, Rejuv, Resolution
#for some reason the line above just runs textgame.... weird


class GameApp(App):
    def board_screen(self, count, scre, playernames, animals, *largs):
        gui = GUI(name = str(count), pnum = int(count))
        with gui.canvas:
            btn_bts = Button(text = 'Back to Player Selection', on_press = partial(self.set_current_screen, scre, 'settings'),
                            size_hint = (.2,.1), pos_hint = {"top":1,"left":1})
            gui.add_widget(btn_bts)
        players = Players(count, playernames)
        players.add_starting_animals(animals)
        scre.add_widget(gui)
        self.set_current_screen(scre, gui.name)

    def set_current_screen(self, screen, name_of_screen, *largs):
        #print(f'Changing screen to {name_of_screen}')
        screen.current = name_of_screen

    def settings_screen(self, root, *largs):
        btn_1 = Button(text = 'One', on_press = partial(self.board_screen, 1, root))
        btn_2 = Button(text = 'Two', on_press = partial(self.board_screen, 2, root))
        btn_3 = Button(text = 'Three', on_press = partial(self.board_screen, 3, root))
        btn_4 = Button(text = 'Four', on_press = partial(self.board_screen, 4, root))
        layout = BoxLayout(orientation = 'vertical')
        label = Label(text='Select the number of players')
        layout.add_widget(label)
        layout.add_widget(btn_1)
        layout.add_widget(btn_2)
        layout.add_widget(btn_3)
        layout.add_widget(btn_4)
        settings_screen = Screen(name = 'settings')
        settings_screen.add_widget(layout)
        root.add_widget(settings_screen)

    def setup_screen(self, root, *largs):
        name_list = []
        animal_list = []
        i = 1
        while i !=5:
            layout = BoxLayout(orientation = 'vertical')
            welcome_label = Label(text = f'Welcome to Sanctuary, Player {i}!')
            name = TextInput(multiline = False, padding_x = 695, padding_y = 60,
                             hint_text = 'Enter your name', font_size = 20, background_color = (0, 128, 129, 1))
            name_list.append(name.text)
            animallist = ['Cow','Horse','Pig','Sheep','Goat','Dog','Cat','Chicken','Duck','Rabbit']
            dropdown = DropDown()
            for index in range(10):
                btn = Button(text=animallist[index], size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: dropdown.select(btn.text))
                dropdown.add_widget(btn)
            abutton = Button(text = 'Click to pick your starting animal')
            abutton.bind(on_release=dropdown.open)
            dropdown.bind(on_release=lambda instance, x: setattr(abutton, 'text', x))
            aname = TextInput(multiline = False, padding_x = 680, padding_y = 60,
                              hint_text = f"Enter animal name", font_size = 20, background_color = (200, 0, 200, 1))
            animal_list.append(Animal(aname.text, abutton.text, True))
            movebtn = Button(text = 'Set up the next player')
            movebtn.bind(on_release = partial(self.set_current_screen, root, f'setup{i + 1}'))
            endbtn = Button(text = 'Finished setting up, go to the game!')
            endbtn.bind(on_release = partial(self.board_screen, i, root, name_list, animal_list))
            layout.add_widget(welcome_label)
            layout.add_widget(name)
            layout.add_widget(abutton)
            layout.add_widget(aname)
            layout.add_widget(movebtn)
            layout.add_widget(endbtn)
            if i == 4:
                layout.remove_widget(movebtn)
            setup_screen = Screen(name = f'setup{i}')
            setup_screen.add_widget(layout)
            root.add_widget(setup_screen)
            i += 1
    def build(self):
        root = ScreenManager()
        self.setup_screen(root)
        return root


if __name__ == '__main__':
    GameApp().run()