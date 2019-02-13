import pygame
from initial_param.kparam import Kparam

class Movie(object):
    """A Movie playing class with pygame package
    """

    def __init__(self, filename):
        pygame.mixer.quit()
        self._movie = pygame.movie.Movie('./video/ex'+str(filename)+'.mpg')
        self.w, self.h = [size for size in self._movie.get_size()]
        self.kp = Kparam()
        self.mscreen = pygame.Surface((self.kp.vid_w/2, self.kp.vid_h/2)).convert()
        self._movie.set_display(self.mscreen, pygame.Rect(0, 0, self.kp.vid_w/2, self.kp.vid_h/2))
        self._movie.play()

    def stop(self, delete=False):
        self._movie.stop()
        if delete:
            del self._movie
            pygame.mixer.init()

    def rewind(self):
        "replay the movie"
        self._movie.rewind()
    
    def ini_resize(self, screen_w, screen_h, ratio=0.5):
        "movie initial resize"
        if screen_w*ratio/self.w >=  screen_h*ratio/self.h:
            return screen_h*ratio/self.h
        else:
            return screen_w*ratio/self.w

    def position(self, screen_w, screen_h, scale=1, Type=1):
        """ generate movie's position.
            According to the keyboard feedback may become larger or smaller.
            Type : 1 => upper-left corner, 2 => lower-right corner 
        """
        if Type == 1:
            return [int(screen_w*self.kp.video_LB/1920.), int(screen_h*self.kp.video2_UB/1080.)]
        elif Type == 2:
            return [int(screen_w*self.kp.video_LB/1920.), int(screen_h*self.kp.video1_UB/1080.)]

    def draw(self, surface, scale=1, pre_scale=1, Type=1):
        "Draw current frame to the surface"
        if scale/pre_scale != 1:
            self.mscreen = pygame.transform.scale(self.mscreen, (int(self.kp.vid_w/2.*scale), int(self.kp.vid_h/2.*scale)))
            self._movie.set_display(self.mscreen, pygame.Rect(0, 0, int(self.kp.vid_w/2.*scale), int(self.kp.vid_h/2.*scale)))
        surface.blit(self.mscreen, self.position(surface.get_width(), surface.get_height(), scale, Type))


