# Recipe Management System

A modern web application for managing and sharing recipes, built with Flask and Python.

##  Features

- **User Authentication**
  - User registration and login
  - Secure session management
  - Role-based access control

- **Recipe Management**
  - Create and share recipes
  - Categorize recipes
  - View detailed recipe information
  - User-friendly recipe browsing

- **Modern UI/UX**
  - Responsive design
  - Material Design influence
  - Interactive components
  - Mobile-friendly interface

##  Technologies Used

- **Backend**
  - Python
  - Flask
  - SQLAlchemy
  - Flask-Login for authentication

- **Frontend**
  - HTML5
  - CSS3
  - Modern CSS Grid
  - Responsive Design

##  Prerequisites

- Python 3.8+
- pip (Python package manager)
- Web browser
- Internet connection (for fonts and dependencies)

##  Installation

1. Clone the repository:
```bash
git clone https://github.com/JuanDavid601/Proyecto-Recetas.git
cd Proyecto-Recetas
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python src/segundoparcialpw/run.py
```

##  Project Structure

```
Proyecto-Recetas/
 src/
    segundoparcialpw/
        static/
           base_style.css
        templates/
           admin/
              reseta_form.html
              signup_form.html
           base.html
           index.html
           login_form.html
           Reseta_view.html
        __init__.py
        extensions.py
        forms.py
        models.py
        run.py
 init_db.py
 pyproject.toml
```

##  Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Register a new account or log in
3. Start creating and sharing your recipes
4. Browse recipes created by other users

##  Features in Detail

### Recipe Management
- Create detailed recipes with descriptions
- Categorize recipes for easy organization
- View complete recipe information
- Edit and manage your own recipes

### User System
- Secure user registration and authentication
- Personal user profiles
- Role-based permissions
- Session management

### Interface
- Modern, responsive design
- Intuitive navigation
- Mobile-friendly layout
- Interactive components

##  Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m "Add some AmazingFeature"`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

##  Contact

Juan David - [@JuanDavid601](https://github.com/JuanDavid601)

Project Link: [https://github.com/JuanDavid601/Proyecto-Recetas](https://github.com/JuanDavid601/Proyecto-Recetas)
