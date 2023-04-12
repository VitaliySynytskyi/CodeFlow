import os


class Config:
    # APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv(
    #     'APPINSIGHTS_INSTRUMENTATIONKEY')
    # SECRET_KEY = os.getenv(
    #     'SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     'SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://howery:Nevermind_15@codeflow.mysql.database.azure.com:3306/codeflow?ssl_ca=DigiCertGlobalRootCA.crt.pem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'a4f728a4c7cb3be47a9e8326d23f3edf'
    APPINSIGHTS_INSTRUMENTATIONKEY = 'e3f5ef91-2bac-4e31-b7bd-cea717f7aaad'
