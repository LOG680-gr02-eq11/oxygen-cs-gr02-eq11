import database.db as _db
import sqlalchemy as _sql


class Temperature(_db.Base):
    __tablename__ = "temperatures"
    timestamp = _sql.Column(_sql.DateTime, primary_key=True, index=True)
    temperature = _sql.Column(_sql.String, index=True)

    def __init__(self, temperature: dict):
        self.timestamp = temperature["timestamp"]
        self.temperature = temperature["temperature"]
