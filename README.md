# BEATT

BEATT is a Flask-based music streaming web application with role-based workflows for listeners, creators, and admins.

It supports song upload and playback, lyrics viewing, search, ratings, creator-specific publishing flows, and admin moderation features such as content and creator flagging.

---

## Project Overview

This project was built as a database-backed music platform that combines:

- user authentication and role-based access
- creator workflows for uploading and managing songs
- listener workflows for browsing, playing, searching, and rating music
- admin workflows for moderation and platform oversight
- Flask + SQLAlchemy based backend logic with template-driven UI rendering

The codebase is organized around modular Flask views, models, decorators, and form-based workflows.

---

## Core Features

### Listener Features
- Browse and play songs
- View song lyrics
- Search songs by title, artist, or genre
- Rate songs
- Access personalized dashboard content

### Creator Features
- Register as a creator
- Upload songs with metadata and audio files
- Manage uploaded songs
- View creator-specific statistics

### Admin Features
- View all songs and creators
- Flag or unflag songs
- Flag or unflag creators
- Monitor platform-level statistics and moderation state

---

## Role Model

The application is built around three main user roles:

- **Listener/User** — consumes music content and interacts with the platform
- **Creator** — uploads and manages music content
- **Admin** — moderates songs and creators, and oversees platform activity

This role-based design is enforced through decorators and protected view flows in the Flask application.

---

## Tech Stack

- **Backend Framework:** Flask
- **Database Layer:** SQLAlchemy
- **Database:** SQLite
- **Authentication:** Flask-Login
- **Forms / Validation:** WTForms / Flask-WTF
- **Frontend Rendering:** Jinja templates
- **Language:** Python

---

## Application Workflows

### Song Management
The app supports end-to-end song handling workflows, including:
- song upload
- audio file storage
- metadata management
- playback and lyrics rendering
- ratings and engagement tracking

### Moderation
The platform includes moderation flows for:
- flagged songs
- flagged creators
- creator blacklist / whitelist behavior
- admin-visible review and management actions

### Dashboard Experience
Users and creators interact through dashboard-style pages that surface:
- suggested songs
- playlists and albums
- statistics
- moderation-related feedback where applicable

---

## Project Structure

```text
views/           # Flask view modules for user, song, and app workflows
models/          # SQLAlchemy models for music, users, ratings, and moderation
forms/           # Form definitions for user and music interactions
decorators/      # Role-based access and shared content/stat helpers
extensions/      # Flask extension initialization (database, login, etc.)
templates/       # Jinja templates for rendered UI pages
static/          # Static assets such as CSS, JS, and media resources
requirements.txt # Python dependencies
```

---

## Setup

### Prerequisites
Before running the project, make sure you have:
- Python 3
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/git4alauddin/iitm-mad1
cd iitm-mad1
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
```

On Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

On Command Prompt:
```cmd
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Run the Application

Initialize the database once:
```bash
flask shell
```
Then run:
```python
db.create_all()
exit()
```

Start the application:
```bash
flask run
```

---

## Why This Project Matters

This project demonstrates:

- Flask-based backend development
- database-backed application design
- modular view/model organization
- role-based access control
- media/content handling workflows
- moderation-oriented backend logic

It is a useful foundation project for understanding how full web applications manage users, content, workflows, and platform-level control paths.

---

## Limitations / Future Improvements

Possible future improvements include:

- stronger API-first architecture for selected workflows
- cloud-based media storage
- better search and recommendation logic
- richer playlist/album management documentation
- deployment and containerization support
- improved test coverage and developer setup automation

---

## Contact
For queries related to the project, contact:
**Md Alauddin Ansari**  
**Email:** 22f1001182@ds.study.iitm.ac.in
