import os
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"


AZURE_SQL = {
    "server": "your-server.database.windows.net",
    "database": "your-db-name",
    "username": "your-username",
    "password": "your-password",
    "driver": "{ODBC Driver 17 for SQL Server}",
}

# Shreder Path 
CXX_SHREDDER_EXE = os.path.abspath("./shredder.exe")


RISK_TO_LEVEL = {
    "Public": 1,    
    "Internal": 2,  
    "Private": 3    
}
