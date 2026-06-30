from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "task_manager_1000.db"

def get_db():
    return sqlite3.connect(DB)

def ensure_task_category_column():
    conn = get_db()
    cursor = conn.cursor()
    columns = [row[1] for row in cursor.execute("PRAGMA table_info(tasks)").fetchall()]
    if "category" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN category TEXT NOT NULL DEFAULT 'Générale'")
        conn.commit()
    conn.close()


def infer_category(title: str) -> str:
    text = (title or "").lower()
    professional_keywords = [
        "réunion", "client", "rapport", "projet", "déployer", "livrer", "réviser", "bug",
        "analyse", "analyse", "code", "code review", "crm", "assurance", "facture", "banque",
        "document", "contrat", "réunion", "developpement", "dev"
    ]
    personal_keywords = [
        "course", "courses", "sport", "famille", "ménage", "nettoyer", "lessive", "repas",
        "appartement", "maison", "lire", "sortir", "cinéma", "soirée", "rdv", "rendez-vous"
    ]

    if any(keyword in text for keyword in professional_keywords):
        return "Professionnelle"
    if any(keyword in text for keyword in personal_keywords):
        return "Personnelle"
    return "Générale"


ensure_task_category_column()

@app.route("/")
def index():
    return "Bienvenue sur l'API de gestion des tâches"

# ✅ GET toutes les tâches
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, status, priority, category FROM tasks where priority='high' order by due_date DESC LIMIT 20")
    tasks = cursor.fetchall()
    
    conn.close()

    return jsonify([
        {"id": t[0], "title": t[1], "status": t[2], "priority": t[3], "category": t[4] or "Générale"}
        for t in tasks
    ])

# ✅ Ajouter une tâche
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    title = data.get('title', '')
    category = infer_category(title)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (user_id, title, description, status, priority, category)
        VALUES (1, ?, ?, 'todo', 'medium', ?)
    """, (title, title, category))

    conn.commit()
    conn.close()

    return {"message": "Task added", "category": category}

# ✅ Supprimer une tâche
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Deleted"}

# ✅ Mettre à jour le statut, la priorité ou la catégorie d'une tâche
@app.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):
    data = request.json
    status = data.get('status')
    priority = data.get('priority')
    category = data.get('category')

    if status is None and priority is None and category is None:
        return {"message": "Aucun changement fourni"}, 400

    conn = get_db()
    cursor = conn.cursor()

    fields = []
    params = []
    if status is not None:
        fields.append("status=?")
        params.append(status)
    if priority is not None:
        fields.append("priority=?")
        params.append(priority)
    if category is not None:
        fields.append("category=?")
        params.append(category)

    params.append(id)
    cursor.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id=?", params)
    conn.commit()
    conn.close()

    return {"message": "Updated"}

if __name__ == "__main__":
    app.run(debug=True)
