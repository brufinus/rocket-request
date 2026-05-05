"""Main module for the rocket silo program."""

from services import input_service
from services.distribution import distribute_items
from services.output_service import print_consolidated, print_distribution


def main() -> None:
    """Main function to coordinate the rocket silo program."""
    num_silos = input_service.request_silo_count()
    items = input_service.request_items()
    silos = distribute_items(items)
    print_distribution(silos, num_silos)
    if len(silos) > num_silos:
        print_consolidated(silos, num_silos)


if __name__ == "__main__":
    main()
