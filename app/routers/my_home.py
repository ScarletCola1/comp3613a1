from fastapi import Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.booking import BookingRepository
from app.repositories.listing import ListingRepository
from app.repositories.review import ReviewRepository
from app.services.booking_service import BookingService
from app.services.listing_service import ListingService
from app.services.review_service import ReviewService
from . import router, templates


@router.get("/my-home", name="my_home_view")
async def my_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity is missing.",
        )
    bookings = BookingService(
        BookingRepository(db),
        ListingRepository(db),
    ).list_approved_for_tenant(user.id)
    return templates.TemplateResponse(
        request=request,
        name="my-home.html",
        context={"user": user, "bookings": bookings},
    )

@router.post(
    "/my-home/bookings/{booking_id}/cancel",
    name="my_home_booking_cancel",
)
async def my_home_booking_cancel(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    booking_id: int,
):
    # STUDENT CODE START: handle the request with BookingService.
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity is missing.",
        )
    try:
        BookingService(
            BookingRepository(db),
            ListingRepository(db),
        ).cancel_tenant_booking(
            booking_id=booking_id,
            tenant_id=user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    # STUDENT CODE END
    return RedirectResponse(
        url=request.url_for("my_home_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/my-home/bookings/{booking_id}", name="my_home_booking_view")
async def my_home_booking_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    booking_id: int,
):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity is missing.",
        )
    booking = BookingService(
        BookingRepository(db),
        ListingRepository(db),
    ).get_approved_booking_for_tenant(
        booking_id=booking_id,
        tenant_id=user.id,
    )
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approved booking not found.",
        )
    listing = ListingService(ListingRepository(db)).get_listing(booking.listingid)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found.",
        )
    return templates.TemplateResponse(
        request=request,
        name="my-home-booking.html",
        context={
            "user": user,
            "booking": booking,
            "listing": listing,
            "reviews": ReviewRepository(db).get_for_booking(booking_id),
        },
    )


@router.post(
    "/my-home/bookings/{booking_id}/reviews",
    name="my_home_review_create",
)
async def my_home_review_create(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    booking_id: int,
    rating: int = Form(),
    body: str = Form(),
):
    # STUDENT CODE START: submit a review through ReviewService.
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity is missing.",
        )
    try:
        ReviewService(
            ReviewRepository(db),
            BookingRepository(db),
            # STUDENT CODE START: provide the ListingRepository dependency.
            ListingRepository(db),
            # STUDENT CODE END
        ).submit_approved_booking_review(
            booking_id=booking_id,
            tenant_id=user.id,
            rating=rating,
            body=body,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    # STUDENT CODE END
    return RedirectResponse(
        url=request.url_for("my_home_booking_view", booking_id=booking_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )
