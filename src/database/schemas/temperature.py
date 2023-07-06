import datetime as _dt
import pydantic as _pydantic


class _BaseTemperature(_pydantic.BaseModel):
    temperature: str


class Temperature(_BaseTemperature):
    timestamp: _dt.datetime

    class Config:
        from_attributes = True


class CreateTemperature(_BaseTemperature):
    pass
