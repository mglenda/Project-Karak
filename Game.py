import pygame

pygame.init()

class Game():
    def __init__(self) -> None:
        pass

    def start(self):
        from GUI.MainScreen import MainScreen
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = MainScreen()

        from GUI.GraphicComponents import Image
        import GUI._const_framepoints as FRAMEPOINT
        self.img = Image(600,600,'_Textures\\Buttons\\ButtonArrowRight.png',self.screen)
        self.img.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_2 = Image(500,500,'_Textures\\Buttons\\ButtonArrowRight.png',self.img)
        self.img_2.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_3 = Image(400,400,'_Textures\\Buttons\\ButtonArrowRight.png',self.img)
        self.img_3.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_4 = Image(300,300,'_Textures\\Buttons\\ButtonArrowRight.png',self.screen)
        self.img_4.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_5 = Image(100,100,'_Textures\\Buttons\\ButtonArrowRight.png',self.screen)
        self.img_5.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_7 = Image(50,50,'_Textures\\Buttons\\ButtonArrowRight.png',self.img_5)
        self.img_7.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_6 = Image(200,200,'_Textures\\Buttons\\ButtonArrowRight.png',self.img_4)
        self.img_6.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.img_8 = Image(10,10,'_Textures\\Buttons\\ButtonArrowRight.png',self.img_5)
        self.img_8.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        from GameLogic.PlayerGroup import PlayerGroup
        self.players = PlayerGroup()

    def get_img(self):
        return self.img

    def get_screen(self):
        return self.screen
    
    def get_players(self):
        return self.players

GAME = Game()