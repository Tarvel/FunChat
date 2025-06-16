# FunChat

FunChat is a Django-based web application that allows users to register, log in, create chat rooms, participate in discussions, and manage profiles. It supports real-time-like messaging and room-based organization of conversations.

## Features

- User Registration and Authentication
- Profile Creation and Updates
- Create, Update, and Delete Chat Rooms
- Post and Delete Messages
- Topic-Based Room Filtering
- Paginated Room Listings
- View Recent Activities and Topics

## Pages and Views

### Authentication

- **`loginPage(request)`**  
  Logs in a user if credentials are valid.

- **`logoutPage(request)`**  
  Logs out the current user.

- **`registerUser(request)`**  
  Registers a new user and redirects to profile completion.

### Profile

- **`completeProfile(request)`**  
  Allows new users to complete their profile after registration.

- **`updateUser(request)`**  
  Allows users to edit their account and profile information.

- **`userProfile(request, username)`**  
  Displays a user’s profile, rooms, and recent messages.

### Home and Room

- **`home(request)`**  
  Displays available rooms, topics, and recent messages. Includes search and pagination.

- **`room(request, pk)`**  
  Shows room details, allows posting messages, and displays participants.

### Room Management

- **`createRoom(request)`**  
  Authenticated users can create a new room under a topic.

- **`updateRoom(request, pk)`**  
  Allows the room host to update room details.

- **`deleteRoom(request, pk)`**  
  Deletes a specific room (host only).

### Message Management

- **`deleteMessage(request, pk)`**  
  Deletes a specific message (message owner only).

### Browse

- **`topicsPage(request)`**  
  Lists all topics with a search feature.

- **`activityPage(request)`**  
  Shows recent messages across rooms.

## Templates Used

- `base/register_login_form.html`
- `base/update_profile.html`
- `base/home.html`
- `base/room.html`
- `base/profile.html`
- `base/create_room.html`
- `base/delete.html`
- `base/topics.html`
- `base/activity.html`
- `base/error.html`

## Dependencies

- Django
- Paginator (for pagination)

## Project Structure
```
├── README.md
├── base        # App logic (models, views, templates)
├── db.sqlite3  # Postgres forproduction
├── funchat
├── manage.py
├── media
├── requirements.txt
├── static
├── templates
└── venv

