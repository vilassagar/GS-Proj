from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
        Common class can be imported to get the below fields in the models.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)  # Timezone-aware UTC timestamp
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        onupdate=lambda: datetime.now(timezone.utc)  # Timezone-aware UTC timestamp on update
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
