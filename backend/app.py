from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, threading, datetime, random
from werkzeug.security import generate_password_hash, check_password_hash

static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app = Flask(__name__, static_folder=static_folder_path, static_url_path="")
CORS(app)

DB_DIR = os.path.join(os.path.dirname(__file__), "db")
LOCK = threading.Lock()

def _db_path(name):
    return os.path.join(DB_DIR, f"{name}.json")

def _read(name):
    path = _db_path(name)
    if not os.path.exists(path):
        os.makedirs(DB_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(name, data):
    with LOCK:
        os.makedirs(DB_DIR, exist_ok=True)
        with open(_db_path(name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def _now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def _calculate_level_from_performance(results):
    """Calculate suggested level based on recent performance"""
    if not results:
        return 2
    
    recent_results = sorted(results, key=lambda r: r.get("created_at", ""), reverse=True)[:3]
    avg_correct = sum(r.get("correct", 0) for r in recent_results) / len(recent_results)
    
    if avg_correct >= 4:
        return 3
    elif avg_correct >= 2.5:
        return 2
    else:
        return 1

@app.route("/")
def root():
    return send_from_directory(static_folder_path, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(static_folder_path, path)

# --- Students ---
@app.post("/api/students")
def create_or_get_student():
    payload = request.get_json(force=True)
    name = payload.get("name", "").strip()
    course = payload.get("course", "").strip()
    if not name or not course:
        return jsonify({"error": "name and course are required"}), 400
    
    students = _read("students")
    sid = f"{name.lower().replace(' ','_')}__{course.lower().replace(' ','_')}"
    
    existing_student = next((s for s in students if s.get("id") == sid), None)
    if not existing_student:
        new_student = {
            "id": sid, 
            "name": name, 
            "course": course, 
            "created_at": _now_iso(),
            "total_points": 0,
            "level": 2,
            "tests_completed": 0,
            "videos_watched": 0
        }
        students.append(new_student)
        _write("students", students)
        return jsonify(new_student)
    
    return jsonify(existing_student)

# --- Auth (simple) ---
@app.post("/api/auth/register")
def auth_register():
    """
    Registra un usuario nuevo y crea su 'student' asociado.
    body: {username, password, name, course}
    """
    p = request.get_json(force=True)
    username = (p.get("username") or "").strip().lower()
    password = (p.get("password") or "").strip()
    name = (p.get("name") or "").strip()
    course = (p.get("course") or "").strip()

    if not username or not password or not name or not course:
        return jsonify({"error": "username, password, name y course son requeridos"}), 400

    students = _read("students")
    # username único (case-insensitive)
    if any((s.get("username") or "").lower() == username for s in students):
        return jsonify({"error": "username ya existe"}), 409

    sid = f"user_{username}"
    student = {
        "id": sid,
        "username": username,
        "password_hash": generate_password_hash(password),
        "name": name,
        "course": course,
        "created_at": _now_iso(),
        "total_points": 0,
        "level": 2,
        "tests_completed": 0,
        "videos_watched": 0,
    }
    students.append(student)
    _write("students", students)

    # Nunca devolver password_hash
    out = {k: v for k, v in student.items() if k != "password_hash"}
    return jsonify(out), 201


@app.post("/api/auth/login")
def auth_login():
    """
    Inicia sesión.
    body: {username, password}
    """
    p = request.get_json(force=True)
    username = (p.get("username") or "").strip().lower()
    password = (p.get("password") or "").strip()

    if not username or not password:
        return jsonify({"error": "username y password son requeridos"}), 400

    students = _read("students")
    student = next((s for s in students if (s.get("username") or "").lower() == username), None)

    # Permite compatibilidad: si todavía no migraste, no hay username.
    if not student:
        return jsonify({"error": "credenciales inválidas"}), 401

    if not check_password_hash(student.get("password_hash", ""), password):
        return jsonify({"error": "credenciales inválidas"}), 401

    out = {k: v for k, v in student.items() if k != "password_hash"}
    return jsonify(out)


@app.post("/api/auth/logout")
def auth_logout():
    # Stateless: el cliente borra su sesión. Aquí solo confirmamos.
    return jsonify({"ok": True})

@app.get("/api/student-stats/<student_id>")
def get_student_stats(student_id):
    """Get comprehensive student statistics"""
    students = _read("students")
    student = next((s for s in students if s.get("id") == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    # Get recent performance
    results = _read("results")
    student_results = [r for r in results if r.get("student_id") == student_id]
    
    # Get rewards
    rewards = _read("rewards")
    student_rewards = [r for r in rewards if r.get("student_id") == student_id]
    total_points = sum(r.get("points", 0) for r in student_rewards)
    
    # Calculate suggested level
    suggested_level = _calculate_level_from_performance(student_results)
    
    # Recent activity (last 5 items)
    recent_activity = []
    for result in student_results[-5:]:
        recent_activity.append({
            "type": "test",
            "description": f"Test completado: {result.get('correct', 0)}/5 correctas",
            "date": result.get("created_at"),
            "points": 10 + min(max(result.get('correct', 0), 0), 5) * 8
        })
    
    for reward in student_rewards:
        if reward.get("type") == "video":
            recent_activity.append({
                "type": "video",
                "description": reward.get("reason", ""),
                "date": reward.get("created_at"),
                "points": reward.get("points", 0)
            })
    
    # Sort by date, most recent first
    recent_activity = sorted(recent_activity, key=lambda x: x.get("date", ""), reverse=True)[:5]
    
    return jsonify({
        "student": student,
        "stats": {
            "total_points": total_points,
            "tests_completed": len(student_results),
            "videos_watched": len([r for r in student_rewards if r.get("type") == "video"]),
            "suggested_level": suggested_level,
            "avg_score": sum(r.get("correct", 0) for r in student_results) / len(student_results) if student_results else 0
        },
        "recent_activity": recent_activity
    })

# --- Videos & Materias ---
@app.get("/api/materias")
def get_materias():
    videos = _read("videos")
    materias = sorted(list({v.get("subject") for v in videos if v.get("subject")}))
    return jsonify(materias)

@app.get("/api/videos")
def get_videos():
    subject = request.args.get("materia")
    videos = _read("videos")
    if subject:
        videos = [v for v in videos if v.get("subject") == subject]

    student_id = request.args.get("student_id")

    if student_id:
        rewards = _read("rewards")
        completed_videos = {
            r.get("video_id")
            for r in rewards
            if r.get("student_id") == student_id and r.get("type") == "video"
        }
        # completed calculado por ID cuando hay student_id
        for v in videos:
            v["completed"] = v.get("id") in completed_videos
    else:
        # sin student_id: ningún video marcado como completado
        for v in videos:
            v["completed"] = False

    return jsonify(videos)

@app.post("/api/video-completo")
def video_completo():
    p = request.get_json(force=True)
    sid = p.get("student_id")
    video_id = p.get("video_id")
    if not sid or not video_id:
        return jsonify({"error": "student_id y video_id son requeridos"}), 400

    students = _read("students")
    videos   = _read("videos")
    rewards  = _read("rewards")

    student = next((s for s in students if s.get("id") == sid), None)
    video   = next((v for v in videos   if v.get("id") == video_id), None)
    if not student or not video:
        return jsonify({"error": "Student or video not found"}), 404

    # ✅ Duplicado por ID (estable)
    already_completed = any(
        r.get("student_id") == sid and
        r.get("type") == "video" and
        r.get("video_id") == video_id
        for r in rewards
    )
    # (Opcional) compatibilidad con recompensas antiguas sin video_id:
    if not already_completed:
        already_completed = any(
            r.get("student_id") == sid and
            r.get("type") == "video" and
            video.get("title") in (r.get("reason") or "")
            for r in rewards if "video_id" not in r
        )

    if already_completed:
        return jsonify({"ok": True, "awarded": 0, "message": "Video ya completado"})

    # Puntos por duración (mínimo 10, 20 si >= 10:00)
    duration = video.get("duration", "00:00")
    try:
        m, s = map(int, duration.split(":"))
        base_points = 20 if (m*60 + s) >= 600 else 10
    except Exception:
        base_points = 10

    # Guardar reward con video_id
    rewards.append({
        "student_id": sid,
        "type": "video",
        "video_id": video_id,  # 👈 clave nueva
        "points": base_points,
        "reason": f"Video completado: {video.get('title')}",
        "created_at": _now_iso(),
    })
    _write("rewards", rewards)

    # Actualizar stats del estudiante
    student["videos_watched"] = student.get("videos_watched", 0) + 1
    student["total_points"]   = student.get("total_points", 0) + base_points
    _write("students", students)

    return jsonify({"ok": True, "awarded": base_points})

# --- Tests Adaptativos ---
@app.get("/api/pregunta")
def get_question():
    level = int(request.args.get("nivel", 2))
    questions = _read("questions")
    subset = [q for q in questions if q.get("level") == level]
    
    if not subset:
        # Fallback to closest level
        all_levels = sorted(list({q.get("level") for q in questions if q.get("level")}))
        closest_level = min(all_levels, key=lambda x: abs(x - level)) if all_levels else 2
        subset = [q for q in questions if q.get("level") == closest_level]
    
    if not subset:
        return jsonify({"error": "no questions found"}), 404
    
    # Random selection instead of always first
    q = random.choice(subset)
    return jsonify(q)

@app.post("/api/test-result")
def test_result():
    payload = request.get_json(force=True)
    sid = payload.get("student_id")
    correct = int(payload.get("correct", 0))
    final_level = int(payload.get("final_level", 2))
    duration_seconds = int(payload.get("duration_seconds", 0))
    
    if not sid:
        return jsonify({"error": "student_id required"}), 400
    
    results = _read("results")
    entry = {
        "student_id": sid, 
        "correct": correct, 
        "final_level": final_level,
        "duration_seconds": duration_seconds,
        "created_at": _now_iso()
    }
    results.append(entry)
    _write("results", results)

    # More sophisticated point calculation
    base_points = 10
    accuracy_bonus = correct * 8  # 8 points per correct answer
    speed_bonus = max(0, 10 - (duration_seconds // 60))  # Bonus for completing quickly
    level_bonus = final_level * 5  # Bonus based on final level achieved
    
    total_points = base_points + accuracy_bonus + speed_bonus + level_bonus
    
    rewards = _read("rewards")
    rewards.append({
        "student_id": sid, 
        "type": "test", 
        "points": total_points,
        "reason": f"Test completado ({correct}/5) nivel final {final_level} en {duration_seconds//60}m {duration_seconds%60}s",
        "created_at": _now_iso()
    })
    _write("rewards", rewards)

    return jsonify({"ok": True, "awarded": total_points, "breakdown": {
        "base": base_points,
        "accuracy": accuracy_bonus,
        "speed": speed_bonus,
        "level": level_bonus
    }})

# --- Rewards & Results ---
@app.get("/api/rewards")
def get_rewards():
    sid = request.args.get("student_id")
    rewards = _read("rewards")
    if sid:
        rewards = [r for r in rewards if r.get("student_id") == sid]
    
    rewards = sorted(rewards, key=lambda r: r.get("created_at", ""), reverse=True)
    total = sum(r.get("points", 0) for r in rewards)
    
    # Group by type for summary
    by_type = {}
    for r in rewards:
        type_key = r.get("type", "other")
        if type_key not in by_type:
            by_type[type_key] = {"count": 0, "points": 0}
        by_type[type_key]["count"] += 1
        by_type[type_key]["points"] += r.get("points", 0)
    
    return jsonify({
        "total": total, 
        "items": rewards,
        "summary": by_type
    })

@app.get("/api/results")
def get_results():
    sid = request.args.get("student_id")
    results = _read("results")
    if sid:
        results = [r for r in results if r.get("student_id") == sid]
    
    results = sorted(results, key=lambda r: r.get("created_at", ""), reverse=True)
    
    # Add some analytics
    if results:
        avg_score = sum(r.get("correct", 0) for r in results) / len(results)
        best_score = max(r.get("correct", 0) for r in results)
        avg_level = sum(r.get("final_level", 2) for r in results) / len(results)
    else:
        avg_score = avg_level = best_score = 0
    
    return jsonify({
        "results": results,
        "analytics": {
            "total_tests": len(results),
            "avg_score": round(avg_score, 1),
            "best_score": best_score,
            "avg_level": round(avg_level, 1)
        }
    })

if __name__ == "__main__":
    # Ensure DB directory exists and preload files
    os.makedirs(DB_DIR, exist_ok=True)
    for fname in ["students", "videos", "questions", "results", "rewards"]:
        if not os.path.exists(_db_path(fname)):
            _write(fname, [])
    
    app.run(host="0.0.0.0", port=8000, debug=True)