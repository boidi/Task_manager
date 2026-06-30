import sqlite3
import random

conn = sqlite3.connect("task_manager_1000.db")
cursor = conn.cursor()

# Templates réalistes de sous-tâches
subtasks_templates = {
    "réunion": [
        "Définir ordre du jour",
        "Préparer présentation",
        "Collecter données",
        "Envoyer invitations",
        "Préparer compte rendu"
    ],
    "courses": [
        "Faire liste de courses",
        "Vérifier stock",
        "Aller au magasin",
        "Payer",
        "Ranger les produits"
    ],
    "dev": [
        "Analyser le besoin",
        "Coder fonctionnalité",
        "Tester code",
        "Corriger bugs",
        "Déployer"
    ],
    "ménage": [
        "Ranger",
        "Nettoyer surfaces",
        "Passer aspirateur",
        "Laver sol",
        "Vérifier propreté"
    ],
    "admin": [
        "Préparer documents",
        "Remplir formulaire",
        "Envoyer dossier",
        "Archiver",
        "Suivre statut"
    ]
}

def detect_type(title):
    t = title.lower()
    if "réunion" in t or "client" in t:
        return "réunion"
    if "course" in t:
        return "courses"
    if "bug" in t or "code" in t or "dev" in t:
        return "dev"
    if "nettoyer" in t or "ménage" in t:
        return "ménage"
    if "facture" in t or "document" in t:
        return "admin"
    return random.choice(list(subtasks_templates.keys()))

# Récupérer toutes les tâches
cursor.execute("SELECT id, title FROM tasks")
tasks = cursor.fetchall()

subtasks_to_insert = []

for task_id, title in tasks:
    task_type = detect_type(title)
    steps = subtasks_templates[task_type]

    # 3 à 5 sous-tâches par tâche
    selected_steps = random.sample(steps, k=random.randint(3, 5))

    for step in selected_steps:
        subtasks_to_insert.append((task_id, step, 0))

# Insérer en masse
cursor.execute("""
CREATE TABLE IF NOT EXISTS subtasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    title TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT 0
);
""")

cursor.executemany("""
INSERT INTO subtasks (task_id, title, is_completed)
VALUES (?, ?, ?)
""", subtasks_to_insert)

conn.commit()
conn.close()

print("✅ Sous-tâches réalistes générées")