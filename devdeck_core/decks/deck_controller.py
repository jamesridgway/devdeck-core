import logging

from devdeck_core.controls.deck_control import DeckControl


class DeckController(DeckControl):

    def __init__(self, key_no, **kwargs):
        self.__logger = logging.getLogger('devdeck')
        self.controls = {}
        super().__init__(key_no, **kwargs)
        self.deck_controls()

    async def clear_deck_context(self):
        for key_no, control in self.controls.items():
            await control.clear_deck_context()
        await super().clear_deck_context()

    def dispose(self):
        for key_no, control in self.controls.items():
            control.dispose()

    def register_control(self, key_no, control_class, **settings):
        self.controls[key_no] = control_class(key_no, **settings)

    def deck_controls(self):
        pass

    async def render(self, deck_context):
        self.__logger.info("Rendering deck: %s", type(self).__name__)
        self.__deck_context = deck_context
        deck_context.reset_deck()
        for key_no, control in self.controls.items():
            await control.set_deck_context(deck_context)
            try:
                await control.initialize()
            except Exception as ex:
                self.__logger.error("Key %s (%s) initialize() raised an unhandled exception: %s",
                                    key_no, type(self).__name__, str(ex))
        self.__logger.info("Rendering complete: %s", type(self).__name__)

    async def pressed(self, key_no: int):
        if key_no not in self.controls:
            return
        if issubclass(type(self.controls[key_no]), DeckController):
            return
        self.__logger.info("Key %s pressed on %s", key_no, type(self).__name__)
        try:
            await self.controls[key_no].pressed()
        except Exception as ex:
            self.__logger.error("Key %s (%s) pressed() raised an unhandled exception: %s",
                                key_no, type(self).__name__, str(ex))

    async def released(self, key_no: int):
        if key_no not in self.controls:
            return
        if issubclass(type(self.controls[key_no]), DeckController):
            await self.__deck_context.set_active_deck(self.controls[key_no])
            return
        self.__logger.info("Key %s released on %s", key_no, type(self).__name__)
        try:
            await self.controls[key_no].released()
        except Exception as ex:
            self.__logger.error("Key %s (%s) released() raised an unhandled exception: %s",
                                key_no, type(self).__name__, str(ex))
        await self.__deck_context.pop_active_deck()
