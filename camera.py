import pygame
from pygame import Rect

WIN_WIDTH = 800
WIN_HEIGHT = 640

HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

CAMERA_SLACK = 30   # this appears to be unused, but looks like a useful concept.

global cameraX, cameraY

class Camera(object):
    """ Camera( int, int ) -> Camera

    The camera has a set width and height to determine the section of the level that is shown.
    """
    def __init__(self):#, width, height):
        self.state = Rect(0, 0, WIN_WIDTH, WIN_HEIGHT)

    def apply(self, target):
        """ c.apply( Sprite ) -> Rect

        In practice, this is always applied to a GameImage and returns the location the target should occupy onscreen,
        given the camera's current offset.
        """
        return target.rect.move(self.state.topleft)

    def origin(self):
        """ c.origin( ) -> int, int

        Returns the current coordinates of the upper-left of the camera. (these should be 0, 0 if the camera is flush with the upper-left corner of the level.)
        """
        return self.state.left, self.state.top

    def update(self, target):
        """ c.update( Sprite ) -> None

        The camera updates its position to center on the given target without going past any of the level's edges.
        The level is not referenced here, so to understand the exact mechanics of this method you would probably have
        to figure out where it is called in level.
        """
        camera = self.state
        
        l, t, _, _ = target.rect
        _, _, w, h = camera
        l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h 
        self.state = Rect(l, t, w, h)
