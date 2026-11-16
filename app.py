from flask import Flask, jsonify, request

app = Flask(__name__)
BUGS = []
SEVERITIES = {"low", "medium", "high", "critical"}
STATUSES = {"open", "in_progress", "closed"}


def error(message, code=400):
    return jsonify({"error": message}), code


@app.get("/bugs")
def list_bugs():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 5))
        if page < 1 or size < 1:
            raise ValueError
    except (TypeError, ValueError):
        return error("page and size must be positive integers")
    status = request.args.get("status")
    items = [b for b in BUGS if not status or b["status"] == status]
    start = (page - 1) * size
    return jsonify({"items": items[start:start + size], "page": page, "pages": (len(items) + size - 1) // size})


@app.post("/bugs")
def create_bug():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    severity = data.get("severity")
    if not title:
        return error("title is required")
    if severity not in SEVERITIES:
        return error("invalid severity")
    bug = {"id": len(BUGS) + 1, "title": title, "severity": severity, "status": "open"}
    BUGS.append(bug)
    return jsonify(bug), 201


@app.patch("/bugs/<int:bug_id>")
def update_bug(bug_id):
    bug = next((b for b in BUGS if b["id"] == bug_id), None)
    if not bug:
        return error("bug not found", 404)
    status = (request.get_json(silent=True) or {}).get("status")
    if status not in STATUSES:
        return error("invalid status")
    bug["status"] = status
    return jsonify(bug)


@app.delete("/bugs/<int:bug_id>")
def delete_bug(bug_id):
    for i, bug in enumerate(BUGS):
        if bug["id"] == bug_id:
            return jsonify(BUGS.pop(i))
    return error("bug not found", 404)


if __name__ == "__main__":
    app.run(debug=True)
