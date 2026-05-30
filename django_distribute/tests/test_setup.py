from unittest import TestCase

from hypothesis import given
from hypothesis import strategies as st

from django_distribute.containers.rocketsilo import RocketSilo
from django_distribute.data.items import ITEMS, make_item
from django_distribute.exceptions import ChestIndexException
from django_distribute.services.helper import get_formatted_float
from django_distribute.services.initialize_setup import (
    build_consolidated_blueprint,
    build_consolidated_invs,
    build_consolidated_load,
    build_distribution,
    calculate_launch_cycles,
    get_consolidated_slots,
    group_items,
)


class TestSetup(TestCase):
    def test_calculate_launch_cycles(self):
        silos = [RocketSilo()]
        num_silos = 1
        self.assertEqual(calculate_launch_cycles(silos, num_silos), 1)

        silos = [RocketSilo() for _ in range(10)]
        num_silos = 1
        self.assertEqual(calculate_launch_cycles(silos, num_silos), 10)

        silos = [RocketSilo() for _ in range(10)]
        num_silos = 2
        self.assertEqual(calculate_launch_cycles(silos, num_silos), 5)

        silos = [RocketSilo() for _ in range(15)]
        num_silos = 4
        self.assertEqual(calculate_launch_cycles(silos, num_silos), 4)

        silos = []
        num_silos = 3
        self.assertFalse(calculate_launch_cycles(silos, num_silos))

        silos = [RocketSilo() for _ in range(5)]
        num_silos = 10
        self.assertEqual(calculate_launch_cycles(silos, num_silos), 1)

    def test_group_item(self):
        grouped_items = group_items([ITEMS["Pipe"]], ITEMS)
        self.assertEqual(len(grouped_items), 1)

    def test_group_multiple_same_items(self):
        items = [ITEMS["Transport belt"] for _ in range(10)]
        grouped_items = group_items(items, ITEMS)
        self.assertEqual(len(grouped_items), 1)
        self.assertEqual(grouped_items["Transport belt"], 10)

    def test_group_multiple_single_items(self):
        items = [ITEMS["Transport belt"], ITEMS["Chemical plant"]]
        grouped_items = group_items(items, ITEMS)
        self.assertEqual(len(grouped_items), 2)
        self.assertEqual(grouped_items["Transport belt"], 1)
        self.assertEqual(grouped_items["Chemical plant"], 1)

    def test_group_multiple_different_items(self):
        belts = [ITEMS["Transport belt"] for _ in range(18)]
        plants = [ITEMS["Chemical plant"] for _ in range(7)]
        pipes = [ITEMS["Pipe"] for _ in range(21)]
        items = belts + plants + pipes
        grouped_items = group_items(items, ITEMS)
        self.assertEqual(len(grouped_items), 3)
        self.assertEqual(grouped_items["Transport belt"], 18)
        self.assertEqual(grouped_items["Chemical plant"], 7)
        self.assertEqual(grouped_items["Pipe"], 21)

    def test_group_items_sort_by_id(self):
        items = group_items(
            [make_item(1, 1, 3), make_item(1, 1, 1), make_item(1, 1, 2)],
            {"a": make_item(1, 1, 3), "b": make_item(1, 1, 1), "c": make_item(1, 1, 2)},
        )
        self.assertEqual(items, {"b": 1, "c": 1, "a": 1})

    def test_get_formatted_float_whole(self):
        self.assertEqual(get_formatted_float(100.0), "100")
        self.assertEqual(get_formatted_float(900.0), "900")

    def test_get_formatted_float_decimal(self):
        self.assertEqual(get_formatted_float(8.251), "8.3")
        self.assertEqual(get_formatted_float(100.8574), "100.9")

    def test_build_distribution_one_cycle(self):
        silos = [RocketSilo(), RocketSilo()]
        silos[0].add_item(ITEMS["Nuclear reactor"])
        silos[1].add_item(ITEMS["Thruster"])
        self.assertEqual(
            build_distribution(silos, 2, ITEMS),
            [[{"Nuclear reactor": 1}, {"Thruster": 1}]],
        )

    def test_build_distribution_more_silos_than_available(self):
        # Multiple cycles
        silos = [RocketSilo(), RocketSilo(), RocketSilo()]
        silos[0].add_item(ITEMS["Nuclear reactor"])
        silos[1].add_item(ITEMS["Thruster"])
        for _ in range(8):
            silos[1].add_item(ITEMS["Crusher"])
        for _ in range(2):
            silos[2].add_item(ITEMS["Thruster"])
        self.assertEqual(
            build_distribution(silos, 2, ITEMS),
            [
                [{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}],
                [{"Thruster": 2}],
            ],
        )

    def test_build_distribution_less_silos_than_available(self):
        # Only one cycle
        silos = [RocketSilo(), RocketSilo(), RocketSilo()]
        silos[0].add_item(ITEMS["Nuclear reactor"])
        silos[1].add_item(ITEMS["Thruster"])
        for _ in range(8):
            silos[1].add_item(ITEMS["Crusher"])
        for _ in range(2):
            silos[2].add_item(ITEMS["Thruster"])
        self.assertEqual(
            build_distribution(silos, 10, ITEMS),
            [[{"Nuclear reactor": 1}, {"Crusher": 8, "Thruster": 1}, {"Thruster": 2}]],
        )

    def test_build_distribution_empty(self):
        self.assertFalse(build_distribution([], 3, ITEMS))

    @given(st.integers(1, 1000), st.integers(1, 1000))
    def test_build_consolidated_load(self, n, s):
        silos = []
        for val in n, s:
            silo = RocketSilo()
            silo.load = val
            silos.append(silo)
        self.assertEqual(build_consolidated_load(silos, 1), [f"{n + s}"])

    def test_build_consolidated_invs(self):
        silos = []
        for val in [ITEMS["Pipe"]], [ITEMS["Pipe"]], [ITEMS["Car"]]:
            silo = RocketSilo()
            silo.inventory = val
            silos.append(silo)
        self.assertEqual(
            build_consolidated_invs(silos, 1, ITEMS), [{"Car": 1, "Pipe": 2}]
        )

    @given(st.integers(1, 10000), st.integers())
    def test_get_consolidated_slots(self, n, s):
        silos = [RocketSilo() for _ in range(n)]
        self.assertEqual(len(get_consolidated_slots(silos, 1)), 1)

    def test_build_consolidated_blueprint(self):
        """Blueprint string is built from a consolidated inventory."""
        invs = [{"Transport belt": 1}]
        expected = "0eNqNUk1rwzAM/StGZ6ekpR1rYJfBDrt2xzGC42itqWOntlNWSv77ZKdpNvZBT7alp6enJ5+h0h22TplQVtbuoThPEQ/F65dnzClpzRD2amuEjjEjGoQCHB469AFdJnd0Qs9BmRo/oJj3bxzQBBUUDsXpcSpN11ToCMD/IuHQWk911sROxJXPcg6ndFKDC7x8V5pqfMR4lBE+9BkFcLgivkUvXYMTxrfWhaxCHZseOqFJIKWMdQ2NyUHaphVOBEt64SEFuugJDRfHIwq/K40N5ThCDUVwHfYxqwI2VDZZyUEL6kWxOd2PpCyNuLpbrJfr9ep+ka+Wy/lkYR5ZavTSqXZwAx6va2JbNEjSsGbViW2s3GNgm0HGjD0JuWPJTSatc0iDmtqzYJlgXmk7IwHTWidvfi44EWexBvqeX7ELfsNn+M2FLP24yYoXYmbPBBrFe0oKWucRy9GHf8zqPwGWVfPY"
        res = build_consolidated_blueprint(invs)
        self.assertEqual(res, expected)

    def test_build_consolidated_blueprint_max_slots(self):
        """Blueprint string is built for a max capacity chest."""
        inv = {}
        for i, item in enumerate(ITEMS):
            if i > 47:
                break
            inv[item] = 1
        expected = "0eNqtmMlu2zAQhl9F4NkMrMVJbKCXAj30mh6LwKAoWp6ai8IliVH43TuS64hx3BQwdRLE5eNoxJ8znN+klkF0FrRf18bsyOr32OLI6mf02vcBN/rY7KDVTPZtmilBVsSKpyCcF5byLT7JYUZAN+KVrPLD44wI7cGDOE4eXvZrHVQtLA6Y/QsyI51xOM/ofiVkzW/mM7IfnrjA3+HrDUic4/oxTvB++HGdkwEz8jbiXevfVRnnQQXJvLG44lNgEq3Ddm2swm+cEW5Ux+zQvyJfhobQOyQ/zN5wRYTz8CxoZ80zNNGnXAkuR3DzzDQXDeVgeYAEZjUyWws8SB8sk9SbF5HggsVIteC3SnjgFCfWoNN8exuBPWyAAxr7S0i518FTZ0Bez767xN4HxXYmkXz/jiylsHvqtmj19cjlBST+OisS9kI+vwB9YS1q7npmJC7nhKol6JYqxregBc0TwMVn4CIBXH4GLhPAkdb6k80A6tegl3mSJPJIbN4oFFqNQkvgjRqrGW6ohE2a30Uoj5+8T2CNIhoD0fW05UcaHeLe9cf+/PxjKQYl6JRIMbTIP1DVrpiEXFwgl5OQRwXVgvGU46OoIpT0FJQKGjmTmDkKp4aWil6IGAJpZ6RIoN6+oyrQ/fHRWEg57YtISGD4lg3p0vW4+xi3keE1gbWMWZIlnDxlpCDoUz/Rtgm0SDkYvVP8VUZSCZvNBJlcpJAgdxS0E9YnmRgJJViNJk7AXJwzp9nN5SgRziTHX53AuotYWhudmliVozbEayfx0oEZ/EToUSqYZGsIaiJwNb9g88RL5JGfu+Fac9So69iLTtllVRGRUzhlzKlTok5VnaHoBpIO3GpxBsQwM+aA26AT8o4qVpNtDa1ZQppV3Z3RJNNNr/mONQnU+zPqVbeKx7584C1z27U2fn0qETRk5W0Qh74Xt6Q6yxAxJGEOuyL9XeMZb/5DCWFxWyyr5XJxX8wXVZWPJYp5T2mE4xa6Y7WBfH0rg2StwK3OcMms3mcPhu+Ezx6OZtxk3/CKkA2BIeMGE2fXGd24zJuMZQ6kuUEDxrLJWHv4WEAZwLSfQw7vCwv/L7Zc8sIpsz254geSs+846GS8w85jsWJ98sMnzjr8AdE5AHk="
        res = build_consolidated_blueprint([inv])
        self.assertEqual(res, expected)

    def test_build_consolidated_blueprint_chest_index_exception(self):
        """ChestIndexException is thrown when adding more items than available slots."""
        inv = {}
        for i, item in enumerate(ITEMS):
            if i > 48:
                break
            inv[item] = 1
        with self.assertRaises(ChestIndexException):
            build_consolidated_blueprint([inv])
