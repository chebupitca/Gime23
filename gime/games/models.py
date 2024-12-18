from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/')
    game_file = models.FileField(upload_to='games/')
    tags = models.ManyToManyField('Tag', blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def update_average_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            self.average_rating = avg_rating
        else:
            self.average_rating = 0
        self.save()

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()  # Значение от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.rating} звезд"

