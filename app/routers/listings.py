from fastapi import Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.booking import BookingRepository
from app.repositories.listing import ListingRepository
from app.services.booking_service import BookingService
from app.services.listing_service import ListingService
from . import router, templates


@router.get(
    "/app/listings/{listing_id}",
    response_class=HTMLResponse,
    name="listing_detail_view",
)
async def listing_detail_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    listing_id: int,
    requested: bool = False,
):
    service = ListingService(ListingRepository(db))
    listing = service.get_published_listing(listing_id)
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found",
        )
    return templates.TemplateResponse(
        request=request,
        name="booking.html",
        context={"user": user, "listing": listing, "requested": requested},
    )


@router.post(
    "/app/listings/{listing_id}/book",
    name="listing_booking_create",
)
async def listing_booking_create(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    listing_id: int,
    tenant_name: str = Form(),
    age: int = Form(),
    start_month: str = Form(),
    end_month: str = Form(),
    message: str = Form(""),
):
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity is missing",
        )
    try:
        BookingService(
            BookingRepository(db),
            ListingRepository(db),
        ).request_booking(
            listing_id=listing_id,
            tenant_id=user.id,
            tenant_name=tenant_name,
            age=age,
            start_month=start_month,
            end_month=end_month,
            message=message,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    detail_url = request.url_for(
        "listing_detail_view",
        listing_id=listing_id,
    ).include_query_params(requested="true")
    return RedirectResponse(
        url=detail_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
