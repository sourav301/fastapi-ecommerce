import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# ✅ Create a test database (use SQLite for simplicity)
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost/ecommerce_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Fixture to set up and tear down the test database
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db  # Provide test session
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Cleanup

# ✅ Override the `get_db` dependency to use the test database
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
