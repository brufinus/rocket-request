from django_distribute.data.constants import ITEM_WEIGHT
from django_distribute.data.items import ITEMS
from django_distribute.services.output_service import *


def test_print_consolidated(capsys):
    silo = RocketSilo()
    silo.inventory = [ITEMS["yumako"]]
    silo.load = ITEMS["yumako"][ITEM_WEIGHT]
    print_consolidated([silo, silo], 1)
