# Task Manager Application

## 📌 Description
This is a full-stack Task Manager application built using **FastAPI (backend)** and **React.js (frontend)**.  
Users can create projects, add tasks, and view analytics of completed and pending tasks.

---

## 🚀 Features
- Create and manage projects
- Add tasks under projects
- View task analytics (Total, Completed, Pending)
- Pie chart visualization
- JWT Authentication
- REST API using FastAPI

---

## 🛠️ Tech Stack

### Backend:
- FastAPI
- SQLite / PostgreSQL
- SQLAlchemy ORM
- JWT Authentication

### Frontend:
- React.js
- Fetch API / Axios
- Chart.js (for analytics)

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
