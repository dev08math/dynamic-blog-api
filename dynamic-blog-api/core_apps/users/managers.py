from distutils.command.build_scripts import first_line_re
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils. translation import gettext_lazy as _
from pandas import value_counts

# Create your tests here.
def CustomUserManager(BaseUserManger):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please provide a valid email address"))

    
    def create_user(self, username, first_name, last_name, email, password, **extra_info):

        if not username:
            raise ValueError(_("Please Provide a username"))

        if not first_name:
            raise ValueError(_("Users must have a valid firstname"))

        if not last_name:
            raise ValueError(_("If you can have a firstname, I bet you can also have lastname"))
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Sorry, but this app will not work without providing a valid email address"))
            
        user = self.model(username=username, first_name = first_name, last_name=last_name, email=email, **extra_info)
        user.set_password(password)
        extra_info.setdefault("is_staff", False)
        extra_info.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password, **extra_info):

        extra_info.setdefault("is_staff", True)
        extra_info.setdefault("is_superuser", True)
        extra_info.setdefault("is_active", True)

        if extra_info.get("is_staff") is False:
            raise ValueError(_("Superuser must be a member of staff first"))
        
        if extra_info.get("is_superuser") is False:
            raise ValueError(_("How come a superuser can't be a superuser?"))
        
        if not password:
            raise ValueError(_("Please provide a proper password to continue"))
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("An admin account must have a valid email address"))
        
        user = self.create_user(username=username, first_name = first_name, last_name=last_name, email=email, **extra_info)
        
        user.save(using=self._db)   # I think this is unecessary
        return user
