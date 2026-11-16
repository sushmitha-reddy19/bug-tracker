from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(title="Bug Tracker API")

Severity = Literal["Low", "Medium", "High", "Critical"]
Status = Literal["Open", "In Progress", "Closed"]

class LoginRequest(BaseModel):
    username: str
    password: str

class BugCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    severity: Severity
    status: Status = "Open"

class BugUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[Status] = None

bugs: list[dict] = []
next_id = 1


def require_auth(authorization: Optional[str]) -> None:
    if authorization == "Bearer expired-token":
        raise HTTPException(status_code=401, detail="Token expired")
    if authorization != "Bearer mock-token":
        raise HTTPException(status_code=401, detail="Authentication required")

@app.post("/login")
def login(payload: LoginRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": "mock-token", "token_type": "bearer"}

@app.post("/bugs", status_code=201)
def create_bug(payload: BugCreate, authorization: Optional[str] = Header(default=None)):
    require_auth(authorization)
    global next_id
    bug = {"id": next_id, **payload.model_dump()}
    next_id += 1
    bugs.append(bug)
    return bug

@app.get("/bugs")
def list_bugs(
    authorization: Optional[str] = Header(default=None),
    page: int = Query(default=1, ge=1),
    severity: Optional[Severity] = None,
    status: Optional[Status] = None,
):
    require_auth(authorization)
    filtered = [b for b in bugs if (severity is None or b["severity"] == severity) and (status is None or b["status"] == status)]
    start = (page - 1) * 10
    return {"items": filtered[start:start + 10], "page": page, "page_size": 10, "total": len(filtered)}

@app.patch("/bugs/{bug_id}")
def update_bug(bug_id: int, payload: BugUpdate, authorization: Optional[str] = Header(default=None)):
    require_auth(authorization)
    for bug in bugs:
        if bug["id"] == bug_id:
            if payload.description is not None:
                bug["description"] = payload.description
            if payload.status is not None:
                bug["status"] = payload.status
            return bug
    raise HTTPException(status_code=404, detail="Bug not found")

@app.delete("/bugs/{bug_id}")
def delete_bug(bug_id: int, authorization: Optional[str] = Header(default=None)):
    require_auth(authorization)
    for index, bug in enumerate(bugs):
        if bug["id"] == bug_id:
            return bugs.pop(index)
    raise HTTPException(status_code=404, detail="Bug not found")
