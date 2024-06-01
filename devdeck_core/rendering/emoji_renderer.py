import os
import requests
from pathlib import Path

from PIL import ImageDraw, Image


class EmojiRenderer:
    def __init__(self, renderer, emoji_name):
        self.renderer = renderer
        self.emoji_name = emoji_name.replace(':', '')
        self.center_vertical = None
        self.center_horizontal = None
        self._x = 0
        self._y = 0
        self._width = None
        self._height = None

    def x(self, x):
        self._x = x
        return self

    def y(self, y):
        self._y = y
        return self

    def center_vertically(self, offset=0):
        self.center_vertical = offset
        return self

    def center_horizontally(self, offset=0):
        self.center_horizontal = offset
        return self

    def height(self, h):
        self._height = h
        return self

    def width(self, w):
        self._width = w
        return self

    def end(self):
        emoji_filename = os.path.join(str(Path.home()), '.devdeck', 'emoji_cache', '{}_512.png'.format(self.emoji_name))

        if not os.path.exists(emoji_filename):
            Path(os.path.join(str(Path.home()), '.devdeck', 'emoji_cache')).mkdir(parents=True, exist_ok=True)
            emoji_url = "https://emojiapi.dev/api/v1/{}/512.png".format(self.emoji_name)
            r = requests.get(emoji_url, allow_redirects=True)
            with open(emoji_filename, 'wb') as f:
                f.write(r.content)

        emoji_img = Image.open(emoji_filename)

        if self._width is not None and self._height is not None:
            emoji_img.thumbnail((self._width, self._height), Image.ANTIALIAS)

        img_pos = (self._x, self._y)
        if self.center_vertical is not None:
            img_pos = (img_pos[0], ((self.renderer.img.height - emoji_img.height) // 2) + self.center_vertical)
        if self.center_horizontal is not None:
            img_pos = (((self.renderer.img.width - emoji_img.width) // 2) + self.center_horizontal, img_pos[1])

        self.renderer.img.paste(emoji_img, img_pos)
        return self.renderer
