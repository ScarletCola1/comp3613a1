from sqlalchemy import Column, ForeignKey, Integer, String
from sqlmodel import Field, SQLModel


class Review(SQLModel, table=True):
    reviewid: int | None = Field(
        default=None,
        sa_column=Column("id", Integer, primary_key=True),
    )
    bookingid: int = Field(
        sa_column=Column(
            "booking_id",
            Integer,
            ForeignKey("booking.bookingid"),
            nullable=False,
            index=True,
        ),
    )
    reviewerid: int = Field(
        sa_column=Column(
            "reviewer_id",
            Integer,
            ForeignKey("user.id"),
            nullable=False,
            index=True,
        ),
    )
    rating: int = Field(
        ge=1,
        le=5,
        sa_column=Column("rating", Integer, nullable=False),
    )
    body: str = Field(
        max_length=2000,
        sa_column=Column("comment", String(2000), nullable=False),
    )

    # STUDENT CODE END
