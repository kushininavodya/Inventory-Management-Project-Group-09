

---

# Kothalawala Mart - Inventory & POS System

A professional **Point of Sale (POS)** and **Inventory Management System** built using **Python**.
The system has a modern interface that automatically adjusts to different screen sizes without needing scrollbars.

---

## Key Features

* **Responsive Dashboard** – Works smoothly on small laptops and large monitors.
* **Secure Login System** – Staff can login and signup safely.
* **Smart POS Billing** – Quick item search, automatic price calculation, and instant stock updates.
* **Inventory Management** – Add new products or update existing stock easily.
* **Reports & History** – View total stock value, total revenue, and transaction history.
* **Low Stock Alerts** – Highlights items with quantity below 5 units.
* **Modern UI Design** – Clean white cards with emerald green and slate blue theme.

---

## Project Structure

The project is divided into 3 main parts: **Interface, Logic, and Database**.

```
Inventory_management_system/
│
├── start.py                # Main file to run the system
│
├── screens/                # User Interface (GUI)
│   ├── login_window.py
│   ├── signup_window.py
│   ├── menu_window.py
│   ├── stock_window.py
│   ├── billing_window.py
│   └── history_window.py
│
├── brain/                  # System Logic
│   ├── login_rules.py
│   ├── stock_rules.py
│   └── bill_rules.py
│
└── database/               # Data Storage (JSON)
    ├── users.json
    ├── stock.json
    └── sales_history.json
```

---

## Installation Guide

### 1. Install Python

Make sure Python 3.8 or higher is installed.

Check version:

```
python --version
```

---

### 2. Create Virtual Environment

**Windows**

```
python -m venv venv
venv\Scripts\activate
```



---

### 3. Install Requirements

Tkinter usually comes with Python.

For Linux users:

```
sudo apt-get install python3-tk
```

---

## Run the System

Run the main file:

```
python start.py
```

---

## Tech Stack

* **Language:** Python 3
* **GUI:** Tkinter / TTK
* **Database:** JSON


