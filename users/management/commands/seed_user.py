import random
from django.core.management.base import BaseCommand, CommandParser

from faker import Faker
from django_seed import Seed
from users.models import User
from posts.models import Post
from images.models import Image
from pets.models import Pet
from categories.models import Category

class Command(BaseCommand):
    help="generate random data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            default=0,
            type=int,
            help="how many user? you make"
        )
    

    def handle(self, *args, **options):
        fake=Faker(['ko_KR'])
        count=options["count"]

        # make user
        user_seeder = Seed.seeder()
        print("first seeder: ", user_seeder)
        user_seeder.add_entity(User, count, {
            "username": lambda x : fake.user_name(),
            "email": lambda x : fake.email(),
            "profile": lambda x: fake.url(),
            "address": None,
            "hasPet": lambda x : random.choice([True, False]),
            "first": False,
            "is_staff": False,
            "is_active": True,
            "dated_joined": fake.date_time_this_decade(),
        })
        
        user_inserted_pks = user_seeder.execute()
        print("user inserted_pks: ", user_inserted_pks)

        user_ids = [pk for model, pks in user_inserted_pks.items() if model == User for pk in pks]
        print("user_ids: ", user_ids)

        
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            print("user: ", user)
            if user.hasPet:
                num_pets = random.randint(1,3)
                pets = random.sample(list(Pet.objects.all()), num_pets)
                user.pets.set(pets)

        user.save()
        self.stdout.write(self.style.SUCCESS(f"Successful generated {count} users."))
            