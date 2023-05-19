import random
from django.core.management.base import BaseCommand, CommandParser

from faker import Faker
from django_seed import Seed
# from users.models import User
from posts.models import Post
from images.models import Image
from pets.models import Pet
from categories.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help="generate random data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            default=0,
            type=int,
            help="how many post? you make"
        )

    def handle(self, *args, **options):
        fake=Faker(['ko_KR'])
        count=options["count"]

        # make post
        users = User.objects.all()
        print("users: ", users)
        for user in users:
            print
            post=Post.objects.create(
                user=user,
                content=fake.text(max_nb_chars=255),
                categoryType= Category.objects.order_by("?").first()
            )

            pet_objects = random.sample(list(Pet.objects.all()), random.randint(1, 3))
            print("pet_objects: ", pet_objects)
            post.boardAnimalTypes.set(pet_objects) 
            print("add success")
          
        self.stdout.write(self.style.SUCCESS("게시글을 성공적으로 생성했습니다."))

#수정사항: category 랜덤으로 받을 것.