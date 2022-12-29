import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Setting:
    TITLE = 'REAL ESTATE FEED'
    VERSION = '0.0.1'
    DESCRIPTION = """
##Number one Vietnam Real Estate Information Gate
I'd always dreamed of owning my own home, 
and now my dream has come true.
    """
    NAME = 'HungNM17'
    EMAIL = 'manhhung.dt6@gmail.com'

    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'mydb')
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
    DATABASE_URL=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SECURITY_KEY = os.getenv('SECURITY_KEY')
    ALGORITHM = 'HS256'

setting = Setting()
