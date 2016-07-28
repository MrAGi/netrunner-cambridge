# Netrunner Cambridge

## Database Changes

### Migrating database

1. make changes to model
2. create migrations - `python3.4 manage.py makemigrations`
3. apply migrations - `python3.4 manage.py migrate`
4. commit and push changes to github
5. run `heroku run --app netrunner-cambridge python manage.py migrate`

### Pulling changes from remote database

1. `dropdb netrunner`
2. `heroku pg:pull DATABASE_URL netrunner --app netrunner-cambridge`

### Pushing changes to remote database

1. `heroku pg:push netrunner DATABASE_URL --app netrunner-cambridge`
2. if that doesn't work then do this first: `heroku pg:reset DATABASE_URL`

## Accounts and Registration

The account system requires the following packages to be available:

- [Django Registration Redux](https://django-registration-redux.readthedocs.org/en/latest/index.html)
- [Djrill](https://github.com/brack3t/Djrill)

## Upgrading Packages

- `pip install Django --upgrade`

