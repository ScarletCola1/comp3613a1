from sqlmodel import Session, select

from app.models.listing import Listing


class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Listing]:
        statement = select(Listing)
        return list(self.db.exec(statement).all())

    def get_by_id(self, listing_id: int) -> Listing | None:
        return self.db.get(Listing, listing_id)

    def create_all(self, listings: list[Listing]) -> list[Listing]:
        self.db.add_all(listings)
        self.db.commit()
        for listing in listings:
            self.db.refresh(listing)
        return listings

    def create(self, listing: Listing) -> Listing:
        # STUDENT CODE START: persist this listing and return the saved row.
       self.db.add(listing)
       self.db.commit()
       self.db.refresh(listing)
       return listing
        # STUDENT CODE END

    def get_for_landlord(self, landlord_id: int) -> list[Listing]:
        statement = (
            select(Listing)
            .where(Listing.landlordid == landlord_id)
            .order_by(Listing.listingid.desc())
        )
        return list(self.db.exec(statement).all())

    def update_status(self, listing: Listing, status: str) -> Listing:
        # STUDENT CODE START: persist this listing status change and return the saved row.
        listing.status = status
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing
        # STUDENT CODE END

    def update_average_rating(
        self,
        listing: Listing,
        average_rating: float,
    ) -> Listing:
        # STUDENT CODE START: persist the recalculated listing average.
        listing.averagerating = average_rating
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing
        # STUDENT CODE END