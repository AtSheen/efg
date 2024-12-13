# Tax Code Prediction Web Application



Built using FastPI and SvelteKit

## Setting Up Environment in Local
Requirements:
- Python 3.12

### <ins> Setting up Fastapi </ins>

1. Create Python Virtual Enviroment

> create venv from python installation
```
~\AppData\Local\Programs\Python\Python312\python -m venv venv

venv\Scripts\activate
```
> activate it

2. Download Dependencies
    - Make sure your venv is activated, if not activate it
    - it may ask you to install autopep8, type yes

```
pip install -r requirements.txt
```

4. Run the Fastapi with uvicorn 
```cmd
uvicorn main:app --no-reload
(or)
python main.py
```