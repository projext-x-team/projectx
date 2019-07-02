class Config:
    ENV="dev"
    AppName="Project X"

class DevConfig(Config):
    DB_URI = "sqlite:////Users/alexren/projects/projectX/db"

class ProdConfig(Config):
    DB_URI = "mysql//"