from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        username = username or email.split('@')[0]
        user = self.model(email=email, username=username, **extra_fields)

        if password:
            user.set_password(password)
        user.set_unusable_password()
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not password:
            raise ValueError('Superuser must have a password')
        return self.create_user(email, username, password, **extra_fields)







