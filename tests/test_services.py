from services.input_service import get_item


class TestSetup:
    def test_get_item(self):
        assert len(get_item("Transport Belt")) > 0
