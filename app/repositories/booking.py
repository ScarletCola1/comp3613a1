from sqlmodel import Session, select

from app.models.booking import Booking
from app.models.listing import Listing


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_pending_for_landlord(self, landlord_id: int) -> list[tuple[Booking, Listing]]:
        statement = (
            select(Booking, Listing)
            .join(Listing, Booking.listingid == Listing.listingid)
            .where(Listing.landlordid == landlord_id, Booking.status == "pending")
            .order_by(Booking.bookingid.desc())
        )
        return list(self.db.exec(statement).all())

    def get_for_landlord(
        self,
        booking_id: int,
        landlord_id: int,
    ) -> Booking | None:
        statement = (
            select(Booking)
            .join(Listing, Booking.listingid == Listing.listingid)
            .where(
                Booking.bookingid == booking_id,
                Listing.landlordid == landlord_id,
            )
        )
        return self.db.exec(statement).first()

    def update_status(self, booking: Booking, status: str) -> Booking:
        booking.status = status
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def get_approved_for_tenant(self, tenant_id: int) -> list[tuple[Booking, Listing]]:
        statement = (
            select(Booking, Listing)
            .join(Listing, Booking.listingid == Listing.listingid)
            .where(Booking.tenantid == tenant_id, Booking.status == "approved")
            .order_by(Booking.bookingid.desc())
        )
        return list(self.db.exec(statement).all())

    def get_cancellable_for_tenant(
        self,
        booking_id: int,
        tenant_id: int,
    ) -> Booking | None:
        # STUDENT CODE START: find this tenant's pending or approved booking.
        statement = (
            select(Booking)
            .where(
                Booking.bookingid == booking_id,
                Booking.tenantid == tenant_id,
                Booking.status == "approved",
            )
        )
        return self.db.exec(statement).first()
        # STUDENT CODE END

    def get_approved_booking_for_tenant(
        self,
        booking_id: int,
        tenant_id: int,
    ) -> Booking | None:
        statement = select(Booking).where(
            Booking.bookingid == booking_id,
            Booking.tenantid == tenant_id,
            Booking.status == "approved",
        )
        return self.db.exec(statement).first()
