from csv import DictReader
from django.core.management import BaseCommand

# Import the model
# from children.models import children
from users.models import Location
ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Location.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading childrens data")

        # Code to load the data into database
        for row in DictReader(open('./datasets/location.csv', encoding='utf-8')):
            child = Location(
                        name=row['name'],
                        lat=row['lat'],
                        lng=row['lng']
            )

            child.save()
