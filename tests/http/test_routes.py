# tests/http/test_routes.py
# Flask test client - no real DB or network needed
from app import db, Students

def test_index_returns_200(client):
    """GET / returns HTTP 200."""
    assert client.get("/").status_code == 200

def test_new_form_returns_200(client):
    """GET /new returns the student form."""
    assert client.get("/new").status_code == 200

def test_add_student_redirects(client):
    """POST /new with all fields redirects (302)."""
    r = client.post("/new", data={
        "name": "Alice Smith", "city": "Miami",
        "addr": "123 Main St", "pin": "33101",
        "phone": "305-555-1234"
    })
    assert r.status_code == 302

def test_student_appears_on_list(client):
    """Added student appears on home page."""
    client.post("/new", data={
        "name": "Bob Jones", "city": "Hialeah",
        "addr": "1 Oak Ave", "pin": "33012",
        "phone": "305-555-0001"
    })
    r = client.get("/", follow_redirects=True)
    assert b"Bob Jones" in r.data

def test_missing_name_rerenders_form(client):
    """POST /new without name re-renders form (200).
    App validates: name, city, addr, phone required."""
    before = Students.query.count()
    r = client.post("/new", data={
        "name": "", "city": "Miami",
        "addr": "1 St", "pin": "33101",
        "phone": "305-555-0000"
    })
    assert r.status_code == 200
    assert Students.query.count() == before