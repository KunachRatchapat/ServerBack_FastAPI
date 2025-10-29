

---

# 🥦 Smart Veggie Backend

> 🎓 Final-year project backend developed with **Python** and **FastAPI**

---

## 🚀 Overview

This backend system is a core component of a final-year project designed to **detect and classify various fruits and vegetables from images**. Leveraging the power of classification, the backend seamlessly handles image uploads, processes the detection results, and stores crucial data such as food type, nutritional information, and other relevant metadata in a robust database powered by **SQLModel**.

It serves as the central hub for our mobile application, providing APIs for image processing, user authentication, managing favorite food items, and retrieving detailed information about each produce.

---

## ✨ Features

* **🍏 Fruit & Vegetable Classification:** Utilizes a pre-trained **YOLOv8** model to accurately identify 28 different classes of fruits and vegetables.
* **📸 Image Upload & Processing:** API endpoint for users to upload images for real-time detection.
* **🔍 Classification:** Processes uploaded images to classify fruits/vegetables.
* **📊 Data Management:** Stores detected food types, nutritional facts, and related metadata in a structured database.
* **💖 Favorite Management:** Allows users to mark and retrieve their favorite fruits and vegetables.
* **🔐 User Authentication:** Secure user registration and login using **JWT (JSON Web Tokens)**.
* **📝 CRUD Operations:** Basic Create, Read, Update, Delete functionalities for managing food items and user data.
* **⚡️ High Performance:** Built with FastAPI for a fast and efficient API experience.

---

## 🛠️ Tech Stack

This project is built using a modern and powerful set of technologies:

### Backend:

* **Python:** The primary programming language.
* **FastAPI:** High-performance web framework for building APIs.
* **SQLModel:** A modern ORM for interacting with SQL databases, combining SQLAlchemy and Pydantic.
* **PostgreSQL (or SQLite for development):** Relational database for data storage.
* **python-jose:** For JSON Web Token (JWT) handling.
* **Pydantic:** Data validation and settings management.
* **python-dotenv:** For managing environment variables.

### Other Tools:

* **Docker:** For containerization (optional, but highly recommended for deployment).
* **Git:** Version control.
* **Uvicorn:** ASGI server for running FastAPI applications.
* **MobileNetV2 (Feature Extractor):** Potentially used in conjunction with a custom classifier (like Random Forest) for feature extraction before YOLOv8, or as a fallback/alternative.
* **Random Forest Classifier:** (If used in parallel or as a refinement step after YOLOv8's initial detection) for further classification based on extracted features.

---