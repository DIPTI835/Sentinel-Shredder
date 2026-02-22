import datetime
import pyodbc
from config import AZURE_SQL

def get_conn():
    conn_str = (
        f"DRIVER={AZURE_SQL['driver']};"
        f"SERVER={AZURE_SQL['server']};"
        f"DATABASE={AZURE_SQL['database']};"
        f"UID={AZURE_SQL['username']};"
        f"PWD={AZURE_SQL['password']}"
    )
    return pyodbc.connect(conn_str)

def ensure_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AuditLogs' AND xtype='U')
    CREATE TABLE AuditLogs (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Timestamp DATETIME2 NOT NULL,
        FileName NVARCHAR(512) NOT NULL,
        Sector NVARCHAR(64) NOT NULL,
        Risk_Score INT NOT NULL,
        Status_Success BIT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_log(filename, sector, risk_score, success):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO AuditLogs (Timestamp, FileName, Sector, Risk_Score, Status_Success)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.datetime.utcnow(), filename, sector, risk_score, 1 if success else 0))
    conn.commit()
    conn.close()