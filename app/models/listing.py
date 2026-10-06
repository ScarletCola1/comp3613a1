from sqlmodel import Field, SQLModel


class Listing(SQLModel, table=True):
    listingid: int | None = Field(default=None, primary_key=True)
    # STUDENT CODE START: add the Listing-to-User ownership foreign key.
    landlordid: int = Field(foreign_key="user.id", index=True)
    # STUDENT CODE END
    title: str
    address: str
    price_per_month: float
    room_type: str
    available_from: str
    status: str = Field(default="available", index=True)
    rating: float = Field(default=0.0)
    monthsrented: int = Field(default=0)
    averagerating: float = Field(default=0.0)
    image_url: str
