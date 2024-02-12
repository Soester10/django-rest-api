from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

class AppUserManager(BaseUserManager):
	def create_user(self, email, username, password):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.username = username
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, username, password):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, username, password)
		user.isactive = True
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user


class Custom_User(AbstractUser, PermissionsMixin):
	id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50)
	username = models.CharField(max_length=50, unique=True)
	USERNAME_FIELD = 'username'
	# REQUIRED_FIELDS = ['email']
	objects = AppUserManager()
	def __str__(self):
		return self.username
	

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DataModel(models.Model):
	user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
	SKU = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=50)
	tags = models.ManyToManyField(Tag)
	stock_status = models.CharField(max_length=50)
	available_stock = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name
