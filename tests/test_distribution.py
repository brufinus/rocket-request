from services.distribution import expand_items


class TestDistribution:
    def test_item_expansion(self):
        items = [("transport_belt", 2), ("chemical_plant", 3)]
        expanded_items = expand_items(items)
        assert len(expanded_items) == 5