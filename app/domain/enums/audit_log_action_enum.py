from enum import Enum


class AuditLogActionEnum(Enum):
    # Auth actions
    SIGN_IN = "sign_in"
    SIGN_UP = "sign_up"

    # Roadtrips actions
    ROADTRIP_CREATED = "roadtrip_created"
    ROADTRIP_PHOTO_UPDATED = "roadtrip_photo_updated"
