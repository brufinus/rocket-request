from data.constants import ITEM_WEIGHT
from data.items import ITEMS
from services.output_service import *


def test_print_consolidated(capsys):
    silo = RocketSilo()
    silo.inventory = [ITEMS["yumako"]]
    silo.load = ITEMS["yumako"][ITEM_WEIGHT]
    print_consolidated([silo, silo], 1)
