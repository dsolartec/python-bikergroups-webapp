from datetime import datetime
from typing import Annotated

from pydantic import PlainSerializer


FormattedDateTime = Annotated[
    datetime,
    PlainSerializer(
        lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'),
        return_type=str,
    ),
]
