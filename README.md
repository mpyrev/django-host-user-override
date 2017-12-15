# django-host-user-override

Overrides current user based on host prefix. For example any request to
```5.user.example.com``` becomes request as if you were logged in as
user with ID 5. Works only if you're actually logged in as superuser.

Also gives you big red banner on top of every page if your user is
overridden.

### Installing django-host-user-override

1. Install the package from PyPI: ```pip install django-host-user-override```

2. Add ```host_user_override``` to ```INSTALLED_APPS```:
```python
INSTALLED_APPS = [
   ...,
   'host_user_override',
   ...,
]
```

3. Add ```HostUserOverrideMiddleware``` right after ```AuthenticationMiddleware```:
```python
MIDDLEWARE = [
   ...,
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'host_user_override.middleware.HostUserOverrideMiddleware',
   ...,
]
```

4. Update your ```settings.py``` file to support subdomains (don't forget about DNS as well):
```python
ALLOWED_HOSTS = ['.example.com']

SESSION_COOKIE_DOMAIN = '.example.com'
```

5. Set new ```change_form.html``` template in ```UserAdmin```:
```python
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    change_form_template = 'host_user_override/change_form.html'
```

## Usage

Open any non-superuser in Django Admin and press 'Login as multiuser' button.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Props to django-debug-toolbar team for HTML injection code
* Thanks to @dimoha for original idea
