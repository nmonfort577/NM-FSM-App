# tests/integration/test_student_db.py
# Runs against staging MySQL. DATABASE_URL set by Jenkins.
import os
import uuid
import pytest
from app import app, db, Students
@pytest.fixture(scope="module")
def integration_app():
    """Connect to staging MySQL for this module."""
    url = os.environ.get("DATABASE_URL", "")
    if not url.startswith("mysql"):
        pytest.fail(
            "DATABASE_URL is not MySQL (got: %r). "
            "Check pytest.ini D: prefixes and the Jenkins export." % url)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": url,
    })
    with app.app_context():
        db.create_all()
        yield app
def cleanup(names):
    """Remove test rows regardless of test outcome."""
    Students.query.filter(Students.name.in_(names)).delete(
        synchronize_session=False)
    db.session.commit()
def test_create_and_retrieve(integration_app):
    """Round-trip: insert student, query back."""
    name = "Integ-%s" % uuid.uuid4().hex[:8]
    try:
        s = Students(name=name, city="Miami",
                     addr="1 Main St", pin="33101",
                     phone="305-555-0000")
        db.session.add(s)
        db.session.commit()
        r = Students.query.filter_by(name=name).first()
        assert r is not None
        assert r.name == name
    finally:
        cleanup([name])
def test_multiple_students(integration_app):
    """Batch insert, all rows queryable."""
    names = ["Integ-%s" % uuid.uuid4().hex[:8] for _ in range(3)]
    try:
        for n in names:
            db.session.add(Students(
                name=n, city="Miami", addr="1 St",
                pin="33101", phone="305-555-0000"))
        db.session.commit()
        for n in names:
            assert Students.query.filter_by(name=n).first() is not None
    finally:
        cleanup(names)