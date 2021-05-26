import os

def run_pytest():
    print("Start test...")
    os.system("dotenv --file .env.test run -- pytest")

def run_server():
    print("Start server...")
    os.system("uvicorn app.main:app --reload")