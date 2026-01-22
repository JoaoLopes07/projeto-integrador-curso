# fix_migration.py
import sqlite3
import sys

def fix_migrations():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("Migrações atuais:")
    cursor.execute("SELECT id, app, name, applied FROM django_migrations ORDER BY applied")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, App: {row[1]}, Nome: {row[2]}, Data: {row[3]}")
    
    print("\nRemovendo migração problemática do admin...")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'admin' AND name = '0001_initial'")
    
    print(f"Registros removidos: {cursor.rowcount}")
    
    conn.commit()
    conn.close()
    print("\nMigração do admin removida. Agora você pode executar as migrações na ordem correta.")

if __name__ == "__main__":
    fix_migrations()