from sqlmodel import Field, SQLModel
from sqlalchemy import CheckConstraint


class Booking(SQLModel, table=True):
    # STUDENT CODE START: constrain status to valid booking states, including cancellation.
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected', 'active', 'completed', 'cancelled')",
            name="ck_booking_status",
        ),
    )

    # STUDENT CODE END

    bookingid: int | None = Field(default=None, primary_key=True)
    listingid: int = Field(foreign_key="listing.listingid", index=True)
    tenantid: int = Field(foreign_key="user.id", index=True)
    tenant_name: str
    age: int
    start_month: str
    end_month: str
    message: str = ""
    status: str = Field(default="pending", index=True)
