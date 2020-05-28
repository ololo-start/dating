import datetime
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    Male = 'male'
    Female = 'female'
    Bisexual = 'bisexual'
    Heterosexual = 'heterosexual'
    Homosexual = 'homosexual'
    Young = '18-25'
    Young_adult = '25-35'
    Adult = '35-45'
    Old_adult = '45-60'
    Senior = '60+'
    CHOICES_GENDER = (
        (Male, Male.title()),
        (Female, Female.title()),
    )
    CHOICES_ORIENTATION = (
        (Bisexual, Bisexual.title()),
        (Heterosexual, Heterosexual.title()),
        (Homosexual, Homosexual.title())
    )
    AGE_CHOICES = (
        ('Young', Young),
        ('Young_adult', Young_adult),
        ('Adult', Adult),
        ('Old_adult', Old_adult),
        ('Senior', Senior)
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=6,
        choices=CHOICES_GENDER,
        default=Male
    )
    orientation = models.CharField(
        max_length=12,
        choices=CHOICES_ORIENTATION,
        default=Heterosexual
    )
    about = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    avatar = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    age = models.CharField(max_length=15, blank=True, null=True)
    partner_gender = models.CharField(
        max_length=6,
        choices=CHOICES_GENDER,
        default=Male
    )
    partner_orientation = models.CharField(
        max_length=12,
        choices=CHOICES_ORIENTATION,
        default=Heterosexual
    )
    partner_age = models.CharField(
        max_length=12,
        choices=AGE_CHOICES,
        default=Young
    )

    def __str__(self):
        return self.user.first_name

    def get_image(self):
        if self.avatar:
            return self.avatar.url
        else:
            return 'media/default.jpg'

    @property
    def get_age(self):
        if self.birthday:
            today = datetime.date.today()
            age = (today.year - self.birthday.year) - int(
                (today.month, today.day) < (self.birthday.month, self.birthday.day)
            )
            if age in range(18, 25):
                return 'Young'
            if age in range(25, 35):
                return 'Young_adult'
            if age in range(25, 45):
                return 'Adult'
            if age in range(45, 60):
                return 'Old_adult'
            if age in range(60, 120):
                return 'Senior'

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super().save(*args, **kwargs)


class UserLike(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_vote')
    like = models.BooleanField(default=False)

    def __str__(self):
        return str(self.voter) + '+' + str(self.to_user) + '=' + str(self.like)

    class Meta:
        unique_together = ('to_user', 'voter')