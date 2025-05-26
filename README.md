# Setup Environment - Shell/Terminal
python -m venv env

# Aktifasi environment
.\env\Scripts\Activate

# Install dependency
pip install -r requirements.txt

# Otomasi dependency di requirements.txt
pip freeze > requirements.txt

# Run steamlit app
streamlit run dashboard.py
