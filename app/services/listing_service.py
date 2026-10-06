from app.models.listing import Listing
from app.repositories.listing import ListingRepository


DEMO_LISTINGS = [
    Listing(
        landlordid=1,
        title="Sunrise Studio near UWI",
        address="12 Gordon Street, St. Augustine",
        price_per_month=1200,
        room_type="Studio",
        available_from="10/2026",
        status="published",
        rating=4.5,
        image_url="https://picsum.photos/seed/student-accommodation-1/800/500",
    ),
    Listing(
        landlordid=1,
        title="Cozy One-Bed, Tunapuna",
        address="48 Eastern Main Road, Tunapuna",
        price_per_month=1000,
        room_type="One bedroom",
        available_from="10/2026",
        status="published",
        rating=4.0,
        image_url="https://picsum.photos/seed/student-accommodation-2/800/500",
    ),
    Listing(
        landlordid=1,
        title="Modern Room, Curepe",
        address="7 Southern Main Road, Curepe",
        price_per_month=950,
        room_type="Private room",
        available_from="10/2026",
        status="published",
        rating=5.0,
        image_url="https://picsum.photos/seed/student-accommodation-3/800/500",
    ),
    Listing(
        landlordid=1,
        title="Student Flat, St. Augustine",
        address="23 Circular Road, St. Augustine",
        price_per_month=1100,
        room_type="Shared flat",
        available_from="10/2026",
        status="published",
        rating=3.5,
        image_url="https://picsum.photos/seed/student-accommodation-4/800/500",
    ),
    Listing(
        landlordid=1,
        title="Quiet Studio, Valsayn",
        address="5 Bamboo Boulevard, Valsayn",
        price_per_month=1250,
        room_type="Studio",
        available_from="10/2026",
        status="published",
        rating=4.8,
        image_url="https://picsum.photos/seed/student-accommodation-5/800/500",
    ),
]


class ListingService:
    def __init__(self, listing_repository: ListingRepository):
        self.listing_repository = listing_repository

    def list_published_listings(self) -> list[Listing]:
        listings = self.listing_repository.get_all()
        return [listing for listing in listings if listing.status == "published"]

    def get_published_listing(self, listing_id: int) -> Listing | None:
        listing = self.listing_repository.get_by_id(listing_id)
        if listing is None or listing.status != "published":
            return None
        return listing

    def get_listing(self, listing_id: int) -> Listing | None:
        return self.listing_repository.get_by_id(listing_id)

    def ensure_demo_listings(self, landlord_id: int) -> None:
        listings = self.listing_repository.get_all()
        if not listings:
            self.listing_repository.create_all(
                [
                    listing.model_copy(update={"landlordid": landlord_id})
                    for listing in DEMO_LISTINGS
                ]
            )
            return

        demo_titles = {listing.title for listing in DEMO_LISTINGS}
        demo_prefix = "https://picsum.photos/seed/student-accommodation-"
        demo_listings = [
            listing
            for listing in listings
            if listing.title in demo_titles and listing.image_url.startswith(demo_prefix)
        ]
        changed = False
        for listing in demo_listings:
            if listing.landlordid != landlord_id:
                listing.landlordid = landlord_id
                changed = True
        if changed:
            self.listing_repository.create_all(demo_listings)

    def get_listings(self) -> list[Listing]:
        return self.listing_repository.get_all()

    def create_listing(
        self,
        *,
        landlord_id: int,
        title: str,
        address: str,
        price_per_month: float,
        room_type: str,
        available_from: str,
    ) -> Listing:
        if not title.strip() or not address.strip() or not room_type.strip():
            raise ValueError("Title, address, and room type are required.")
        if price_per_month <= 0:
            raise ValueError("Monthly price must be greater than zero.")
        if not available_from.strip():
            raise ValueError("Availability month is required.")
        listing = Listing(
            landlordid=landlord_id,
            title=title.strip(),
            address=address.strip(),
            price_per_month=price_per_month,
            room_type=room_type.strip(),
            available_from=available_from.strip(),
            status="published",
            rating=0.0,
            image_url="",
        )
        return self.listing_repository.create(listing)

    def remove_listing(self, *, listing_id: int, landlord_id: int) -> Listing:
        # STUDENT CODE START: verify landlord ownership and mark the listing removed.
        listing = self.listing_repository.get_by_id(listing_id)
        if listing is None or listing.landlordid != landlord_id:
            raise ValueError("Listing not found.")
        return self.listing_repository.update_status(listing, "removed")
        # STUDENT CODE END