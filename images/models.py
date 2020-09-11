from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/%Y/%m/%d/',
    )
    description = models.TextField(blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self):
        return 'Изображение {} пользователя {}'.format(
            self.title, self.user.username
        )

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id])
