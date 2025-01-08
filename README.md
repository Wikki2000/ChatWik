# Chat App

A real-time chat application built with Python, Flask, and Socket.IO that allows users to send and receive messages instantly. This app also uses Redis for message broadcasting, SQLAlchemy for database management, and is styled with HTML and CSS.

## Features

- **Real-time Messaging**: Send and receive messages in real-time using Socket.IO.
- **User Authentication**: Sign up and log in securely to start chatting.
- **Multiple Chat Rooms**: Join different chat rooms to chat with specific groups of people.
- **Private Messaging**: Send private messages to users individually.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Push Notifications**: Get notified of new messages.
- **User Presence**: View online/offline status of users.
- **Message History**: Stored messages for users to view previous conversations.

## Tech Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Database**: SQLAlchemy, SQLite (or another database of your choice)
- **Real-time Communication**: Socket.IO
- **Authentication**: Flask-Login or custom authentication using sessions
- **Caching and Message Broadcasting**: Redis
- **Frontend**: HTML, CSS, jQuery for frontend interactions

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python 3](https://www.python.org/downloads/) installed on your machine.
- [Redis](https://redis.io/download) installed or use a cloud Redis provider.
- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask](https://flask.palletsprojects.com/en/2.0.x/) are required (can be installed via pip).

## Installation

### Clone the repository

```bash
git clone https://github.com/Wikki2000/ChatWik/
cd ChatWik
```

## Create a Virtual Environment
It's recommended to use a virtual environment to isolate your project dependencies.

1. Install virtualenv if you haven't already:
```bash
pip install virtualenv
```

2. Create a new virtual environment:
```bash
python3 -m venv venv
```
3. Install Dependencies
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Running the App
Make sure Redis is running locally or is connected via a cloud service. You can start Redis with the following command:

```bash
redis-server
```
To start the app, run the following command:

```bash
python3 -m app.app
```
