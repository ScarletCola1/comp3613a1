from fastapi import Request
from fastapi.responses import HTMLResponse
from app.dependencies.auth import AuthDep
from app.dependencies.session import SessionDep
from app.repositories.listing import ListingRepository
from app.services.listing_service import ListingService
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    listings = ListingService(ListingRepository(db)).list_published_listings()
    return templates.TemplateResponse(
        request=request,
        name="listings.html",
        context={
            "user": user,
            "listings": listings,
        },
    )