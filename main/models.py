from django.db import models
from django.db.models.deletion import CASCADE
from main.tasks import notify_user_func
from django.dispatch import receiver
from django.db.models.signals import post_save


class Created_at(models.Model):
    """
    нужен для того чтобы, во всех модельках не прописывать один и тот же код
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Problem(Created_at):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        'account.CustomUser',
        on_delete=models.CASCADE,
        related_name='problems'
    )

    def __str__(self):
        return self.title


class Picture(Created_at):
    image = models.ImageField(upload_to='pictures')
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='pictures'
    )
    

class Reply(Created_at):
    text = models.TextField()
    image = models.ImageField(
        upload_to='reply_pictures'
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        'account.CustomUser',
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return self.text[:10] + '...'


class Comment(Created_at):
    text = models.TextField()
    author = models.ForeignKey(
        'account.CustomUser',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text

@receiver(post_save, sender=Problem)
def modify_user(sender, instance, created, **kwargs):
    if created:
        email = instance.author.email
        notify_user_func.delay(email)
