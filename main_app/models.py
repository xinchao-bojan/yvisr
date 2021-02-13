from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email or not first_name or not last_name:
            raise ValueError('Customer must have all necessary information')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name.capitalize(),
                          last_name=last_name.capitalize(),
                          )
        user.set_password(password)
        user.save(using=self._db)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email=self.normalize_email(email),
                                first_name=first_name,
                                last_name=last_name,
                                password=password
                                )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=63, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=63)
    last_name = models.CharField(verbose_name='Фамилия', max_length=63)
    photo = models.ImageField(verbose_name='Фото', blank=True)
    rating_points = models.IntegerField(verbose_name='Баллы', default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.rating_points = 0
        for elem in self.record_set.all():
            self.rating_points += int(elem.value)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Record(models.Model):
    owner = models.ForeignKey(CustomUser, verbose_name='Владелец', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    proof = models.FileField(verbose_name='Файл, подтверждающий достижение', blank=True)
    confirmed = models.BooleanField(verbose_name='Подтверждение', default=False)
    value = models.SmallIntegerField(verbose_name='Ценность', default=0)
    judge = models.ForeignKey(CustomUser, verbose_name='Оцениватель', blank=True, on_delete=models.CASCADE,
                              related_name='as_judge')

    def __str__(self):
        return f'{self.title} {self.owner.first_name} {self.owner.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.owner.save()

    def delete(self, *args, **kwargs):
        o = self.owner
        super().delete(*args, **kwargs)
        o.save()
