Here’s your updated `README.md` file with the GitHub repository URL included:

---

```markdown
# Travel Agency Platform

A Django-based travel agency platform designed for users to explore travel packages, receive personalized recommendations, and interact with an intelligent chatbot for travel-related assistance. This platform integrates Celery for task management, PostgreSQL for the database, and the OpenAI API for chatbot functionality.

---

## Features

### Core Functionality
- **Travel Package Browsing**:
  - View detailed descriptions, pricing, and themes.
- **Personalized Recommendations**:
  - Receive recommendations based on user clicks and feedback, focusing on package similarity.
- **Chatbot Integration**:
  - Ask travel-related queries and get real-time responses using OpenAI.

### Backend and Infrastructure
- **Celery Task Management**:
  - Asynchronous task handling for email notifications and recommendations.
- **PostgreSQL Database**:
  - Robust database for travel packages, user feedback, and activity tracking.
- **REST API Ready**:
  - Extendable with Django REST Framework for additional integrations.

---

## Installation and Setup

### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **PostgreSQL**
- **RabbitMQ** (for Celery task management)

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/nadiatrabelsii/flouci_travel_agency.git
cd flouci_travel_agency
```

---

### Step 2: Set Up the Python Environment
1. Install `virtualenv` if not already installed:
   ```bash
   pip install virtualenv
   ```
2. Create and activate a virtual environment:
   ```bash
   virtualenv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

---

### Step 3: Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

---

### Step 4: Configure the Environment Variables
1. Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
2. Add the following to your `.env` file:
   ```dotenv
   SECRET_KEY=your-secret-key_django
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   DB_NAME=your database name (postgress)
   DB_USER=your user name (postgress)
   DB_PASSWORD=your password
   DB_HOST=127.0.0.1
   DB_PORT=your port (postgress)
   OPENAI_API_KEY=your-openai-api-key
   CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
   ```

---

### Step 5: Set Up the Database
1. Create the PostgreSQL database:
   ```bash
   createdb travel
   ```
2. Apply the migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

### Step 6: Start the Django Development Server
Run the development server:
```bash
python manage.py runserver
```

---

### Step 7: Start Celery and RabbitMQ
1. Start RabbitMQ (if not already running):
   ```bash
   rabbitmq-server
   ```
2. Start the Celery worker:
   ```bash
   celery -A travel_site worker --loglevel=info
   ```

---

### Access the Platform
Open your browser and navigate to:
```text
http://127.0.0.1:8000
```

---

## Usage

### Features Available:
- **Browse Travel Packages**:
  - Navigate through the available packages and view their details.
- **Get Recommendations**:
  - Based on user activity and feedback, personalized recommendations will be shown.
- **Chatbot Assistance**:
  - Ask travel-related questions via the chatbot powered by OpenAI's GPT-4.

---

## Project Structure

```plaintext
FLUOCI_TRAVEL_AGENCY/
├── frontend/                    # Frontend application for user interface
│   ├── migrations/              # Django migrations for frontend (if needed)
│   ├── templates/frontend       # HTML templates for rendering frontend pages
│   ├── static/css               # Static files (CSS, JS, images)
│   ├── admin.py                 # Admin configuration
│   ├── apps.py                  # App configuration for frontend
│   ├── models.py                # Database models for frontend (if any)
│   ├── tasks.py                 # Tasks specific to frontend logic (optional)
│   ├── urls.py                  # URL patterns for frontend views
│   └── views.py                 # Views for handling frontend requests
├── travel_app/                  # Backend core application
│   ├── management/              # Custom management commands
│   ├── migrations/              # Database migrations for core app
│   ├── admin.py                 # Admin configuration for backend models
│   ├── middleware.py            # Custom middleware for session management
│   ├── models.py                # Database models (e.g., TravelPackage, Feedback)
│   ├── serializers.py           # Serializers for DRF or other data transformations
│   ├── tasks.py                 # Celery tasks for asynchronous processing
│   ├── tests.py                 # Unit tests for backend logic
│   ├── urls.py                  # URL patterns for backend views
│   ├── utils.py                 # Utility functions for reusable logic
│   └── views.py                 # Views for handling backend requests
├── travel_scraper/              # Web scraping application
│   ├── spiders/                 # Spiders for scraping specific travel websites
│   ├── scrapy.cfg               # Scrapy configuration file
├── travel_site/                 # Project configuration directory
│   ├── __init__.py              # Python package initialization
│   ├── asgi.py                  # ASGI configuration for asynchronous support
│   ├── celery.py                # Celery configuration
│   ├── settings.py              # Project settings (database, middleware, etc.)
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI configuration for deployment
├── staticfiles/                 # Collected static files for deployment
├── manage.py                    # Django management script
└── README.md                    # Project documentation

```

---

## Technologies Used

- **Backend**: Django, PostgreSQL, Celery
- **Frontend**: HTML, CSS, JavaScript (Django templates)
- **Task Queue**: RabbitMQ
- **Chatbot**: OpenAI API

---

## Contributing

Follow these steps to contribute to the project:

1. **Fork the Repository**:
   ```bash
   git fork https://github.com/nadiatrabelsii/flouci_travel_agency.git
   ```
2. **Create a New Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**:
   ```bash
   git commit -m "Add your message here"
   ```
4. **Push Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Submit a Pull Request**:
   - Go to the repository on GitHub.
   - Click **Pull Requests** > **New Pull Request**.
   - Submit your changes for review.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or support, contact:

- **Email**: Trabelsi.Nadia@esprit.tn
```

---

### Instructions
1. Save this file as `README.md` in the root directory of your project.
2. Commit and push it to your GitHub repository:
   ```bash
   git add README.md
   git commit -m "Add README.md"
   git push origin main
   ```

Let me know if you'd like further edits or improvements! 🚀