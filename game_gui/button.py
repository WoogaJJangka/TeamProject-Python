import pygame
import pygame_gui

def Ybutton(manager):

    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((125, 100), (150, 50)),
                                       text='YES',
                                       manager=manager)



def Nbutton(manager):

    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 100), (150, 50)),
                                       text='NO',
                                       manager=manager)