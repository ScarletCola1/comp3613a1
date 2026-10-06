from fastapi import Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from itsdangerous import exc

from app.dependencies.auth import LandlordDep
from app.dependencies.session import SessionDep
from app.repositories.booking import BookingRepository
from app.repositories.listing import ListingRepository
from app.services.booking_service import BookingService
from app.services.listing_service import ListingService
from . import router, templates


@router.get("/landlord", name="landlord_home_view")
async def landlord_home_view(
    request: Request,
    user: LandlordDep,
    db: SessionDep,
):
    booking_service = BookingService(
        BookingRepository(db),
        ListingRepository(db),
    )
    listings = ListingRepository(db).get_for_landlord(user.id)
    pending_requests = booking_service.list_pending_for_landlord(user.id)
    return templates.TemplateResponse(
        request=request,
        name="landlord.html",
        context={
            "user": user,
            "pending_requests": pending_requests,
            "listings": listings,
        },
    )


@router.post("/landlord/bookings/{booking_id}/{decision}", name="landlord_booking_decision")
async def landlord_booking_decision(
    request: Request,
    user: LandlordDep,
    db: SessionDep,
    booking_id: int,
    decision: str,
):
    try:
        BookingService(
            BookingRepository(db),
            ListingRepository(db),
        ).update_landlord_decision(
            booking_id=booking_id,
            landlord_id=user.id,
            decision=decision,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return RedirectResponse(
        url=request.url_for("landlord_home_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/landlord/listings/new", name="landlord_listing_new")
async def landlord_listing_new(
    request: Request,
    user: LandlordDep,
):
    return templates.TemplateResponse(
        request=request,
        name="landlord-listing-form.html",
        context={"user": user},
    )


@router.post("/landlord/listings/new", name="landlord_listing_create")
async def landlord_listing_create(
    request: Request,
    user: LandlordDep,
    db: SessionDep,
    title: str = Form(),
    address: str = Form(),
    price_per_month: float = Form(),
    room_type: str = Form(),
    available_from: str = Form(),
):
    # STUDENT CODE START: complete this thin handler through ListingService.
    ListingService(ListingRepository(db)).create_listing(
        landlord_id=user.id,
        title=title,
        address=address,
        price_per_month=price_per_month,
        room_type=room_type,
        available_from=available_from,
    )
    # STUDENT CODE END
    return RedirectResponse(
        url=request.url_for("landlord_home_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/landlord/listings/{listing_id}/delete", name="landlord_listing_delete")
async def landlord_listing_delete(
    request: Request,
    user: LandlordDep,
    db: SessionDep,
    listing_id: int,
):
    # STUDENT CODE START: keep this route thin and call ListingService.
    try:
        ListingService(ListingRepository(db)).remove_listing(
            listing_id=listing_id,
            landlord_id=user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    # STUDENT CODE END
    return RedirectResponse(
        url=request.url_for("landlord_home_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
