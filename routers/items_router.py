import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status

from config.config import API_TAG_NAME, ITEM_REPO
from models.item_model import Item
from services.items_service import get_item, get_items


def get_repo():
    with ITEM_REPO as repo:
        yield repo


router = APIRouter(
    tags=[API_TAG_NAME]
)


@router.get("/purchase", status_code=status.HTTP_200_OK, response_model=list[Item])
async def purchase(
        request: Request, name: str | None = None, repo=Depends(get_repo), ):
    filters = {
        "name": name
    }

    return get_items(filters, repo)


@router.post("/purchase/{type_uuid}", status_code=status.HTTP_201_CREATED)
async def create_license( request: Request, repo=Depends(get_repo) ):
    license_uuid = create_license(repo)

    return {"license UUID": license_uuid}


@router.get("/pending", status_code=status.HTTP_200_OK, response_model=list[Item])
async def pending_items(
        request: Request, repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        }, "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)


@router.get("/unassigned", status_code=status.HTTP_200_OK, response_model=list[Item])
async def unassigned_items(
        request: Request, repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        }, "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)


@router.post("/assign/{uuid}", status_code=status.HTTP_201_CREATED)
async def assign_license( request: Request, repo=Depends(get_repo) ):
    return {"status": "WIP"}


@router.get("/assigned", status_code=status.HTTP_200_OK, response_model=list[Item])
async def assigned_items(
        request: Request, repo=Depends(get_repo)
):
    filters = {
        "user_uuid": {"$ne": None, "$exists": True, "$ne": ""}
    }
    return get_items(filters, repo)


@router.post("/unassign/{uuid}", status_code=status.HTTP_201_CREATED)
async def unassign_license( request: Request, repo=Depends(get_repo) ):
    return {"status": "WIP"}


@router.get("/expired", status_code=status.HTTP_200_OK, response_model=list[Item])
async def expired_items(
        request: Request, repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        }, "exp": {
            "$lt": now
        }
    }
    logging.info(f"expired items {filters}")
    return get_items(filters, repo)


@router.get("/license/{uuid}", status_code=status.HTTP_200_OK, response_model=Item)
async def read_item( request: Request, uuid: str, repo=Depends(get_repo) ):
    logging.info(f"read item {uuid}")
    item = get_item(uuid, repo)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/mine", status_code=status.HTTP_200_OK, response_model=list[Item])
async def get_mine( request: Request, repo=Depends(get_repo) ):
    logging.info(f"get mine")
    logging.info(request.state)
    token_info = request.state.token_info
    logging.info(token_info)
    user_uuid = ""
    logging.info(f"get mine: {user_uuid}")
    logging.info(user_uuid)
    filters = {
        "user_uuid": user_uuid
    }
    return get_items(filters, repo)
