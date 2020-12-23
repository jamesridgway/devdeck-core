from assertpy import assert_that

from devdeck.core.settings.control_validation_error import ControlValidationError


class TestControlValidationError:
    def test_errors_parsed(self):
        errors = {'decks': [{0: [{'controls': [{3: [{'keyx': ['unknown field']}]}]}]}]}
        exception = ControlValidationError(SomeControl(), 4, errors)
        assert_that(str(exception)) \
            .is_equal_to(
            'The following validation errors occurred for SomeControl on key 4:\n * decks.0.controls.3.keyx: unknown field.')


class SomeControl:
    pass
