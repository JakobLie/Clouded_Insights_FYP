# Flask Backend

## Project Structure
backend/
├── app.py # Main Flask application
├── venv/ # Local virtual environment (not committed)
├── pycache/ # Python cache files (can be ignored)
└── README.md

## Activate venv (Always do this before running Flask app)
macOS/Linux:
    source venv/Scripts/activate

Windows (PowerShell):
    venv\Scripts\Activate.ps1

Note: 
You will see a (venv) beside your path in the terminal once activated.
Run 'pwd' to confirm e.g. in Git Bash shell:
- I Run: $ pwd
- I See: /c/Users/user1/Desktop/FYP/Clouded_Insights_FYP/backend (venv) 

## Deactivate venv
To deactivate venv: 
    deactivate

## Running Flask
To run the Flask app (check that you are in the "backend" folder): 
    python -m run flask

Note: The server runs at http://127.0.0.1:5000

## Stopping Flask
To stop the Flask app:
    Press Ctrl + C in the terminal

# Dependencies (Make sure you are in the venv)
To install packages:
    pip install -r requirements.txt


To update requirements after adding new packages:
    pip freeze > requirements.txt

# Additional Notes
Don’t commit venv/ or __pycache__/ (they are added to .gitignore)
Use branches and PRs when pushing to main

