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
        fake=Faker()
        count=options["count"]

        #make user
        seeder = Seed.seeder()
        seeder.add_entity(User, count, {
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
        
        inserted_pks = seeder.execute()
        

        user_ids = [pk for model, pks in inserted_pks.items() if model == User for pk in pks]
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
            
            seeder = Seed.seeder()
            seeder.add_entity(Post, 2, {
                "user": lambda x: User.objects.get(id=user_id),
                "content": lambda x: fake.text(max_nb_chars=255),
                "categoryType": lambda x: Category.objects.first(),
                "viewCount": 0,
                # "boardAnimalTypes":[],
            })
        
        inserted_pks = seeder.execute()
        post_ids = [pk for model, pks in inserted_pks.items() if model == Post for pk in pks]
        print("post_ids: ", post_ids)

        print("error ready")
        for post_id in post_ids:
            print("post_id: ", post_id)
            if Pet.objects.exists():
                print("I'm error" )
                post = Post.objects.get(id=post_id)
                pet_types = random.sample(list(Pet.objects.all()), random.randint(1, 3))
                post.boardAnimalTypes.set(pet_types) 
                post.save()  
            else:
                print("I'm not")
                post = Post.objects.get(id=post_id)
                pet_types = random.sample(list(Pet.objects.all()), random.randint(1, 3))
                post.boardAnimalTypes.set(pet_types)   
                post.save()
        self.stdout.write(self.style.SUCCESS("게시글을 성공적으로 생성했습니다."))

        seeder = Seed.seeder()
        for post_id in post_ids:
            post = Post.objects.get(id=post_id)
            num_images = random.randint(0, 5)
            images = random.sample(range(num_images), num_images)
            for image in images:
                seeder.add_entity(Image, 1, {
                    "post": lambda x: Post.objects.get(id=post_id),
                    "img_path": fake.image_url(),
                })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"Successfully generated random data."))






