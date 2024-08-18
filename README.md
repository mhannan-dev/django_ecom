# Django ecommerce application with inventory using tailwind, flowbite, django, sqlite3

## Overview

This is a Django ecommerce application with inventory using tailwind, flowbite, django, sqlite3

## Requirements

- Python 3.9 or higher
- Django 4.2 or higher
- [Other dependencies, e.g., Django REST framework, Pillow, etc.]

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mhannan-dev/django_ecom.git
   cd your-repository

python -m venv venv
source venv/bin/activate  # On Unix or macOS
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
