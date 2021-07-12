# Message-Board
An interaction portal where a user can add posts, comment on other users' posts, like posts. Staff users can create groups, can add users to the group, remove user from the group

## Installation 

**Download required packages:**
```
pip install -r requirements.txt
```

**This project uses redis in backend**

For Windows: Download [memurai](https://www.memurai.com)

**You can change the settings of the project in [settings.py](https://github.com/yashwanth1412/Message-Board/blob/master/edxdjango/settings.py)**

## Features
- Google authentication
- User can add, delete posts
- User can like, comment on others' posts
- UI is updated in real time when a post/comment is added
- Staff users(Admin) can create groups, add, remove users from the group

## Environment Variables

Add a .env file in the root directory, specify the variables:
```
GOOGLE_CLIENT_ID = your_google_client_id
GOOGLE_SECRET = your_google_secret
```

## Setup and Run the project
```
Create media folder in the root directory and add avatar.png (Default proflie pic for user)
```

**Run the following commands:**
```
python manage.py makemigrations
python manage.py migrate
```

**Run the server using:**
```
python manage.py runserver
```
