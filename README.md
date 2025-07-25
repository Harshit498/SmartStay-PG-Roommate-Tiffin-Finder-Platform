# 🏠 SmartStay – PG, Flat & Roommate Finder Platform

**SmartStay** is a full-stack rental platform built with Flask where users can search for PGs, flats, or roommates. It also includes **roommate matching**, **tiffin services**, and **chat features** to create a one-stop solution for students and working professionals looking for accommodation.

---

## 🚀 Features

### 🔍 PG & Flat Listings
- Browse verified PG and flat listings
- Filter by location, budget, and amenities
- Responsive UI for desktop and mobile

### 👫 Roommate Matching
- Match with compatible roommates based on preferences
- In-app **chat system** for direct communication

### 🍱 Tiffin Service Integration
- Discover local tiffin providers with menus and pricing
- Booking forms to connect with service providers

### 📝 Booking Forms
- Submit booking requests for PGs, flats, or tiffin services
- Data stored in SQLite for tracking and management

### 📊 Dashboard
- Centralized view of saved listings and roommate connections
- Planned **expense tracking** module (future enhancement)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python), SQLAlchemy
- **Frontend:** HTML, CSS (Bootstrap), Jinja2
- **Database:** SQLite
- **Features:** Authentication, Filterable Listings, Roommate Matching Logic

---

## 📂 Project Structure

smartstay/
│
├── app.py # Main Flask app (routes, auth, etc.)
├── models.py # Database models (Users, PG, Roommate, Tiffin)
├── templates/ # All HTML templates (home, listings, dashboard)
├── static/ # CSS, JS, and images
├── blueprints/ # Modular route files (pg, roommate, tiffin, chat)
└── instance/smartstay.db # SQLite database


---

## 🧠 How It Works (Simplified)

1. **User Signup/Login** → Users create accounts and log in.
2. **Browse Listings** → PGs and flats are displayed with filters (budget, location).
3. **Roommate Matching** → Users answer preference questions → matched with potential roommates.
4. **Booking & Tiffin** → Booking forms allow requests to PG owners or tiffin providers.
5. **Dashboard** → Shows saved listings, matches, and service requests.

---

## 🧪 Status

| Feature                  | Status       |
|-------------------------|--------------|
| PG & Flat Listings       | ✅ Done       |
| Roommate Matching        | ✅ Done       |
| Tiffin Services          | ✅ Done       |
| Booking Forms            | ✅ Done       |
| Chat Feature             | ⚠️ Basic (expandable) |
| Expense Tracking         | 🚧 Planned    |
| Deployment               | ❌ Not yet deployed |

---

## 📸 Screenshots *(Optional Section)*
_Add homepage, listing, and roommate match screenshots here for extra impact._

---

## 🧑‍💻 Author

- **Harshit Khandelwal**  
- Final Year B.Tech CSE Student  
- [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgements

- UI inspired by Indian PG rental platforms like StanzaLiving & BookMyPG
- Data modeled for real-world PG/roommate use cases

---
