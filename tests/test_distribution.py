from services.distribution import distribute_items


class TestDistribution:
    def test_distribution(self):
        distribute_items(1, [])