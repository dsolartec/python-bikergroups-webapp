from datetime import datetime


class UserModel:
    # Common properties

    id: str | None
    username: str
    password: str | None

    # Profile properties

    display_name: str

    # System properties

    created_at: datetime | None
    updated_at: datetime | None

    def __init__(
            self,
            # Common properties
            id: str | None,
            username: str,
            password: str | None,

            # Profile properties
            display_name: str,

            # System properties
            created_at: datetime | None,
            updated_at: datetime | None,
    ):
        self.id = id
        self.username = username
        self.password = password

        self.display_name = display_name

        self.created_at = created_at
        self.updated_at = updated_at
