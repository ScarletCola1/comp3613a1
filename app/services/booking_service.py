from datetime import datetime

from app.models.booking import Booking
from app.repositories.booking import BookingRepository
from app.repositories.listing import ListingRepository


class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        listing_repository: ListingRepository,
    ):
        self.booking_repository = booking_repository
        self.listing_repository = listing_repository

    def list_pending_for_landlord(self, landlord_id: int):
        return self.booking_repository.get_pending_for_landlord(landlord_id)

    def list_approved_for_tenant(self, tenant_id: int):
        return self.booking_repository.get_approved_for_tenant(tenant_id)

    def get_approved_booking_for_tenant(
        self,
        *,
        booking_id: int,
        tenant_id: int,
    ) -> Booking | None:
        return self.booking_repository.get_approved_booking_for_tenant(
            booking_id,
            tenant_id,
        )

    def cancel_tenant_booking(
        self,
        *,
        booking_id: int,
        tenant_id: int,
    ) -> Booking:
        # STUDENT CODE START: coordinate cancellation of this tenant's active booking.
        booking = self.booking_repository.get_cancellable_for_tenant(
            booking_id,
            tenant_id,
        )
        if booking is None:
            raise ValueError("Booking not found or cannot be cancelled.")
        return self.booking_repository.update_status(booking, "cancelled")
        # STUDENT CODE END

    def update_landlord_decision(
        self,
        *,
        booking_id: int,
        landlord_id: int,
        decision: str,
    ) -> Booking:
        if decision not in {"approved", "rejected"}:
            raise ValueError("Decision must be approved or rejected.")
        booking = self.booking_repository.get_for_landlord(booking_id, landlord_id)
        if booking is None:
            raise ValueError("Booking request not found.")
        if booking.status != "pending":
            raise ValueError("This booking request has already been decided.")
        return self.booking_repository.update_status(booking, decision)

    def request_booking(
        self,
        *,
        listing_id: int,
        tenant_id: int,
        tenant_name: str,
        age: int,
        start_month: str,
        end_month: str,
        message: str,
    ) -> Booking:
        listing = next(
            (
                item
                for item in self.listing_repository.get_all()
                if item.listingid == listing_id and item.status == "published"
            ),
            None,
        )
        if listing is None:
            raise ValueError("This listing is no longer available.")
        if not 18 <= age <= 120:
            raise ValueError("Age must be between 18 and 120.")
        try:
            start = datetime.strptime(start_month, "%Y-%m")
            end = datetime.strptime(end_month, "%Y-%m")
        except ValueError as exc:
            raise ValueError("Choose valid start and end months.") from exc
        if end < start:
            raise ValueError("The end month must be the same as or later than the start month.")
        if not tenant_name.strip():
            raise ValueError("Name is required.")

        booking = Booking(
            listingid=listing_id,
            tenantid=tenant_id,
            tenant_name=tenant_name.strip(),
            age=age,
            start_month=start_month,
            end_month=end_month,
            message=message.strip(),
            status="pending",
        )
        return self.booking_repository.create(booking)
