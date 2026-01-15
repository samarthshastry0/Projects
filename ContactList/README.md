# CRUD Contact List

A full-stack contact management app built with Flask, React, and SQLite.

## Tech Stack

- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** React, Vite, JavaScript

## Project Structure

```
ContactList/
├── backend/
│   ├── config.py       # Flask & database config
│   ├── main.py         # API routes
│   └── models.py       # Contact model
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── ContactForm.jsx
    │   └── ContactList.jsx
    └── index.html
```

## API Endpoints

- `GET /contacts` - Get all contacts
- `POST /create_contact` - Create new contact
- `PATCH /update_contact/<id>` - Update contact
- `DELETE /delete_contact/<id>` - Delete contact

## Setup & Installation

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install flask flask-sqlalchemy flask-cors
python main.py
```
Backend runs on `http://127.0.0.1:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

## Features

- Create, read, update, and delete contacts
- Real-time list updates
- Form validation
- Error handling
- RESTful API
