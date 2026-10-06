from app.models.review import Review
from app.repositories.booking import BookingRepository
from app.repositories.listing import ListingRepository
from app.repositories.review import ReviewRepository


class ReviewService:
    def __init__(
        self,
        review_repository: ReviewRepository,
        booking_repository: BookingRepository,
        listing_repository: ListingRepository,
    ):
        self.review_repository = review_repository
        self.booking_repository = booking_repository
        self.listing_repository = listing_repository

    def submit_approved_booking_review(
        self,
        *,
        booking_id: int,
        tenant_id: int,
        rating: int,
        body: str,
    ) -> Review:
        # STUDENT CODE START: validate an approved owned booking and create its review.
        booking = self.booking_repository.get_approved_booking_for_tenant(
            booking_id, tenant_id
        )
        if booking is None:
            raise ValueError("Approved booking not found for this tenant.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        comment = body.strip()
        if not comment:
            raise ValueError("Comment cannot be empty.")

        review = Review(
            bookingid=booking_id,
            reviewerid=tenant_id,
            rating=rating,
            body=comment,
        )
        saved_review = self.review_repository.create(review)
        self.recalculate_listing_average(booking.listingid)
        return saved_review
        # STUDENT CODE END

    def recalculate_listing_average(self, listing_id: int) -> None:
        # STUDENT CODE START: combine the original listing rating with submitted reviews.
        listing = self.listing_repository.get_by_id(listing_id)
        if listing is None:
            raise ValueError("Listing not found for review rating update.")

        scores = self.review_repository.get_ratings_for_listing(listing_id)
        total = sum(scores)
        count = len(scores)
        if listing.rating > 0:
            total += listing.rating
            count += 1
        average = round(total / count, 1) if count else 0.0

        self.listing_repository.update_average_rating(listing, average)
        # STUDENT CODE END
