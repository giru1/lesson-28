from csv import DictReader
from django.core.management import BaseCommand

# Import the model
# from children.models import children
from ads.models import Ads, Category
from users.models import User

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
        if Ads.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading childrens data")

        # Code to load the data into database
        for row in DictReader(open('./datasets/ad.csv', encoding='utf-8')):
            author_id = User.objects.get(id=row['author_id'])
            category_id = Category.objects.get(id=row['category_id'])
            child = Ads.objects.create(
                        name=row['name'],
                        author_id=author_id,
                        price=row['price'],
                        description=row['description'],
                        is_published=row['is_published'].lower().title(),
                        image=row['image'],
                        category_id=category_id
            )


            # child.locations.add(locations)
