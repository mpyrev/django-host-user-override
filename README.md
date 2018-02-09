# django-host-user-override

Overrides current user based on host prefix. For example any request to
```5.user.example.com``` (format can be changed in settings) becomes
request as if you were logged in as user with ID 5. This allows you
to be logged in as different users in different tabs
**at the same time** without losing your primary authenticated user.

Works only if you're logged in as superuser.

Also gives you big red banner on top of every page if your user is
overridden.

## Requirements

* Your DNS server should resolve subdomains ```*.user.<your domain>```
  to the same IP address as main domain.
* Your project should not use absolute link generation or any other
  technic that can change current subdomain. It is a more inconvenience
  than requirement though.

## Installing django-host-user-override

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

### Optional settings

6. Update ```settings.py``` if you want host pattern other than ```<id>.user.<domain>```. Example for ```u<id>.<domain>```:
```python
HOSTUSEROVERRIDE_HOST_REGEXP = r'u(\d+)\..+'

HOSTUSEROVERRIDE_HOST_SUB_REGEXP = r'u\d+\.'

HOSTUSEROVERRIDE_REDIRECT_URL_FORMAT = 'http://u{user_id}.{host}/'

HOSTUSEROVERRIDE_PERMANENT_REDIRECT = False
```

## Usage

Open any non-superuser in Django Admin and press 'Login as multiuser' button.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Props to django-debug-toolbar team for HTML injection code
* Thanks to @dimoha for original idea
