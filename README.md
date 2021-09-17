# Jungle Devs - Django Reddit Challenge

## Description

**Challenge goal**: The idea of the challenge is to implement a very simplified version of [Reddit](https://www.reddit.com),
meaning you will have _Users_, _Topics_, _Posts_ and _Comments_. with this you're expected to test your knowledge on
the basic concepts involved in a Django backend application, and to also learn even more.
Always!

**Target level**: This is an entry level course, no prior knowledge of programming is needed.

**Final accomplishment**: By the end of this challenge, you’ll be able to understand the basics of Django and how to create your own RESTful API with basic CRUD functionalities.

## Acceptance criteria

- Separate your project into 4 Django apps, one for each entity:
  - User
  - Topic
  - Post
  - Comment
- Have all the required fields for each entity as described on this README
- Use the URL structure described on this README with Nested URL Routers

### Entities

As mentioned in the description, this challenge will have four entities (each one should be a separate app).
Here are brief descriptions of what they are and what are the expected properties of each (keep in mind that you can
improve them as you wish!):

- _User_: can be used plain from what is offered by Django;
- _Topic_: the equivalent of a sub-reddit. The suggest fields are:
  - Name
  - Title
  - Author
  - Description
  - URLName - the name we want to use to reach it through the browser (check [SlugField](https://docs.djangoproject.com/en/2.1/ref/models/fields/#slugfield))
  - Created_at
  - Updated_at
- _Post_: the equivalent of a _Reddit thread_, a _post_ belongs to a _specific topic_ and is _created by an user_. The
  suggested fields are:
  _ Title
  _ Content
  _ Created_at
  _ Updated_at \* Topic
- _Comment_: the equivalent of a comment, a comment belongs to a _specific post_ (which belongs to a _specific topic_)
  and is _created by an user_. The suggested fields are:
  _ Title
  _ Content
  _ Created_at
  _ Updated_at \* Post

### URLs

We want to have a behavior similar to _Reddit (not necessarily equal)_, so ideally we'd like a structure like this:

- _/topics/_ - lists all available topics
- _/topics/{urlname}/_ - details (as well as some posts) from a specific topic (identified by _urlname_)
- _/topics/{urlname}/posts/_ - lists all posts from a specific topic
- _/topics/{urlname}/posts/{post_id}/_ - lists details and some comments from a post
- _/topics/{urlname}/posts/{post_id}/comments/_ - lists all comments from a post
- _/topics/{urlname}/posts/{post_id}/comments/{comment_id}/_ - lists details from a comment

## Prerequisites

- [Python 3.7](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Virtualenv](https://github.com/pypa/virtualenv/)
- [Git](https://git-scm.com/)

## Development

- Create the virtual environment and activate it

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

- Install the requirements `pip install -r requirements.txt`
- Start the dockers `docker-compose up` with the database and the localstack
- Run the server with `python manage.py runserver 8000`

You need a `.env`file with your environment variables, here's an example file:

```bash
LOAD_ENVS_FROM_FILE='True'
ENVIRONMENT='development'
SECRET_KEY='#*=backend-challenge=*#'
DEFAULT_FROM_EMAIL='Challenge <challenge@jungledevs.com>'
DATABASE_URL='postgres://postgres:postgres@localhost:5432/backend-challenge-001'
SENTRY_DSN='sentry_key'
AWS_STORAGE_BUCKET_NAME='django-be'
```

## Additional Information

Here are some useful stuff to keep in mind while completing this challenge:

- Try to keep your code [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), so the creation of [abstract helper](https://realpython.com/modeling-polymorphism-django-python/#abstract-base-model) [models](https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes) is more than welcome
  to avoid repetition of fields in your models;
- Remember that only the author of a topic, post or comment should be able to modify or delete it! If you have any doubts, check the [Authentication and Permissions part](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/) on the Django REST tutorial
- For better structuring and visualization, you may use [Nested Serializers](https://www.django-rest-framework.org/api-guide/relations/#nested-relationships) to customize your responses beyond the primary keys
- [Nested Routers documentation](https://github.com/alanjds/drf-nested-routers)
- [lookup field section on the Routers documentation](https://www.django-rest-framework.org/api-guide/routers/#simplerouter)
