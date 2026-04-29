from services import input_service
from services.distribution import distribute_items


def main():
    num_silos = input_service.request_silo_count()
    items = input_service.request_items()
    distribute_items(num_silos, items)


if __name__ == "__main__":
    main()