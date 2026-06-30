import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("task_manager_1000.db")
cursor = conn.cursor()

titles_pro = [
    "Préparer réunion", "Envoyer rapport", "Appeler client", 
    "Analyser données", "Mettre à jour CRM", "Corriger bug",
    "Déployer application", "Faire code review", "Optimiser requête",
    "Rédiger documentation"
]

titles_perso = [
    "Faire les courses", "Nettoyer appartement", "Faire sport",
    "Lire un livre", "Préparer repas", "Ranger maison",
    "Faire lessive", "Appeler famille", "Sortir poubelles",
    "Organiser week-end"
]

titles_admin = [
    "Payer facture", "Contacter assurance", "Prendre RDV médecin",
    "Vérifier compte bancaire", "Envoyer document",
    "Renouveler abonnement", "Classer papiers"
]

descriptions = [
    "À faire rapidement", "Urgent", "À planifier",
    "Peut être reporté", "Important", "Tâche quotidienne"
]

statuses = ["todo", "in_progress", "done"]
priorities = ["low", "medium", "high"]
# def initialize_database():
#     conn = sqlite3.connect("task_manager.db")
#     cursor = conn.cursor()

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             description TEXT NOT NULL
#         )
#     ''')

#     conn.commit()
#     conn.close()

def random_title():
    return random.choice(titles_pro + titles_perso + titles_admin)

def random_desc():
    return random.choice(descriptions)

def random_date():
    return (datetime.now() + timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d")

tasks = []

for i in range(1000):
    tasks.append((
        None,  # id
        random.randint(1, 100),  # user_id
        random_title(),
        random_desc(),
        random.choice(statuses),
        random.choice(priorities),
        random_date()
    ))
    

# with sqlite3.connect("task_manager_1000.db", timeout=30) as conn:
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
id INTEGER PRIMARY KEY AUTOINCREMENT not null,
user_id INTEGER NOT NULL,
title TEXT NOT NULL,
description TEXT NOT NULL,
status TEXT NOT NULL,
priority TEXT NOT NULL,
due_date date NOT NULL
            )
            """)
cursor.executemany("""
INSERT INTO tasks (id, user_id, title, description, status, priority, due_date)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", tasks)
conn.commit()
conn.close()

print("✅ 1000 tâches réalistes générées")