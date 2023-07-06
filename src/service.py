import datetime as _dt
from typing import TYPE_CHECKING

import database.db as _db
import database.models.temperature as _modelsTemperature
import database.schemas.temperature as _schemasTemperature

if TYPE_CHECKING:
    pass


def add_tables():
    return _db.Base.metadata.create_all(bind=_db.engine)


def get_db():
    db = _db.LocalSession()
    try:
        yield db
    finally:
        db.close()


def create_event(timestamp: _dt.datetime, temperature: str):
    temperature_entry = {}
    temperature_entry['timestamp'] = timestamp[0:19]
    temperature_entry['temperature'] = temperature

    db = get_db()
    create_temperature_entry(temperature_entry, next(db))


def create_temperature_entry(
        temperature: _schemasTemperature.CreateTemperature, db):
    temperature = _modelsTemperature.Temperature(temperature)

    db.add(temperature)
    db.commit()
    db.refresh(temperature)
