import os


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'a4f728a4c7cb3be47a9e8326d23f6edf'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+mysqlconnector://CloudSA1dea01e3:Ha8JWXG9@codeflowsql.database.windows.net:1433/CodeFlow'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
