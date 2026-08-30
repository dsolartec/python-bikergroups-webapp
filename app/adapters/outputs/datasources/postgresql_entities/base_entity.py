import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase


class BaseEntity(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }
