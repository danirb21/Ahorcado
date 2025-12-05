# Hangman Game – Desktop Version (Tkinter) + Backend API 

This repository contains two related components of the Hangman project:

✅ **Desktop Client (Tkinter)** – standalone playable version  
✅ **Backend API (Flask)** – provides authentication, competitive scoring and leaderboard  

Both parts live in the same repository for convenience during development.

---

## Desktop Application (Tkinter)

### Features
- Fully offline playable mode
- Two game modes:
  - **Competitive Mode** – requires login and connects to backend
  - **Custom Mode** – choose allowed mistakes (does not affect global ranking)
- Turtle-based hangman drawing
- Follows a clean MVC separation
- Guest play supported
- Smooth window transitions

### Technologies Used
- Python 3
- Tkinter (UI)
- Turtle (graphics)
- MVC Architecture

##  Backend API (Flask)

The backend enables the online features of the competitive mode:

### Capabilities
- User registration
- Login and authentication
- JWT-based session handling
- Score updating
- Global leaderboard query

### Technologies Used
- Python 3
- Flask (REST API)
- Flask-JWT-Extended (auth)
- SQLAlchemy ORM
- SQLite database

---

##  Authentication (JWT)

- On successful login, the API returns a **JWT token**
- The desktop app stores it in memory during the session
- Protected routes require

## 🏆 Leaderboard Logic

- Only competitive mode submits results
- Scores accumulate per authenticated user
- Leaderboard is fetched from the backend
- Guest mode does **not** send data

##  Author

This project was created as a learning exercise to explore:

✅ Python GUI development  
✅ Backend/API architecture  
✅ JWT authentication  
✅ MVC design patterns  
✅ Client–server interaction  
