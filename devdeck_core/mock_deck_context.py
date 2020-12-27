from unittest.mock import MagicMock

from PIL import ImageChops, Image
from assertpy import assert_that

from devdeck_core.deck_context import DeckContext
from devdeck_core.renderer import Renderer


def mock_context(control):
    return MockDeckContextManager(control)


def assert_rendered(ctx, image_filename_or_renderer):
    if isinstance(image_filename_or_renderer, str):
        assert_that(ImageChops.difference(ctx.get_image(), Image.open(image_filename_or_renderer)
                                          .convert('RGB')).getbbox()).is_none()
        return
    if isinstance(image_filename_or_renderer, Renderer):
        assert_that(ImageChops.difference(ctx.get_image(), image_filename_or_renderer.render()).getbbox()).is_none()
        return
    raise AttributeError('Unexpected type for image_filename_or_renderer')


class MockDeck:
    def key_count(self):
        return 15

    def set_key_image(self, key_no, image):
        pass

    def key_image_format(self):
        return {
            'size': (72, 72),
            'format': 'BMP',
            'flip': (True, True),
            'rotation': 0,
        }


class MockDeckContextManager:
    def __init__(self, control):
        self.control = control

    def __enter__(self):
        devdeck = MagicMock()
        deck = MockDeck()
        ctx = DeckContext(devdeck, deck)
        self.control.set_deck_context(ctx)
        return ctx

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.control.clear_deck_context()
