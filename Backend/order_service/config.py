import urllib.parse


class Config:

    # 🔐 JWT SETTINGS (MUST MATCH AUTH SERVICE)
    JWT_SECRET = "jwt-secret-key-123"
    JWT_ALGORITHM = "HS256"


    # ☁️ AWS DB SETTINGS
    DB_USER = "admin"
    DB_PASS = "sar761SARVAG"
    DB_HOST = "database-1.ckr048u4ykae.us-east-1.rds.amazonaws.com"


    @staticmethod
    def get_db_uri(db_name):

        password = urllib.parse.quote_plus(Config.DB_PASS)

        return (
            f"mysql+pymysql://{Config.DB_USER}:{password}"
            f"@{Config.DB_HOST}:3306/{db_name}"
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False
