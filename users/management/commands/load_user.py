from csv import DictReader
from django.core.management import BaseCommand

# Import the model
# from children.models import children
from users.models import User, Location
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
        if User.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading childrens data")

        # Code to load the data into database
        for row in DictReader(open('./datasets/user.csv', encoding='utf-8')):
            child = User.objects.create(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        username=row['username'],
                        password=row['password'],
                        role=row['role'],
                        age=row['age'],
            )
            child.locations.set(Location.objects.filter(id=row['location_id']))
            # locations = Location.objects.get_or_create(name=row['location_id'])
            # child.locations.add(locations)

