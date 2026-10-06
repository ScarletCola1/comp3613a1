from sqlmodel import Session, select

from app.models.booking import Booking
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, review: Review) -> Review:
        # STUDENT CODE START: persist and return the new Review.
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review
        # STUDENT CODE END

    def get_for_booking(self, booking_id: int) -> list[Review]:
        statement = (
            select(Review)
            .where(Review.bookingid == booking_id)
            .order_by(Review.reviewid.desc())
        )
        return list(self.db.exec(statement).all())

    def get_ratings_for_listing(self, listing_id: int) -> list[int]:
        # STUDENT CODE START: return review ratings linked to this listing's bookings.
        statement = (
            select(Review.rating)
            .join(Booking, Review.bookingid == Booking.bookingid)
            .where(Booking.listingid == listing_id)
        )
        return list(self.db.exec(statement).all())
        # STUDENT CODE END
