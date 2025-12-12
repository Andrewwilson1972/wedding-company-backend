# wedding-backend

Backend assignment for The Wedding Company — Organization Management Service  
Tech: **FastAPI**, **Motor (async MongoDB)**, **JWT**, **bcrypt**

---

## Project structure

```text
wedding-backend/
├── requirements.txt
├── README.md
└── app/
├── main.py
├── core/
│ ├── config.py
│ ├── database.py
│ └── security.py
├── models/
│ ├── organization.py
│ └── user.py
├── routers/
│ ├── auth_router.py
│ └── organization_router.py
├── services/
│ ├── auth_service.py
│ └── organization_service.py
└── utils/
├── jwt_handler.py
└── password_handler.py
```

---

## 🚀 Quick Start (Local Development)

### **1️⃣ Create & activate a virtual environment**

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### **2️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Create a `.env` file**

See .env example below.

### **4️⃣ Ensure MongoDB is running**

Ensure MongoDB is running locally on port 27017.

### **5️⃣ Start the FastAPI server**

```bash
uvicorn app.main:app --reload
```

### **6️⃣ Test the service**

Health check: GET http://127.0.0.1:8000/

Swagger API docs: http://127.0.0.1:8000/docs

API will run at: http://localhost:8000

## `.env` Example

```env
MONGO_URI=mongodb://localhost:27017/wedding_master
JWT_SECRET=replace-this-with-a-strong-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
APP_NAME=wedding-backend
APP_HOST=0.0.0.0
APP_PORT=8000
```
