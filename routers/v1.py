import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from config.config import API_TAG_NAME, ITEM_REPO
from models.item_model import Item
from models.response_model import SuccessResponse, create_success_response
from services.items_service import get_item, get_items

VERSION = "v1"
api_group_name = f"/{API_TAG_NAME}/{VERSION}/"

def get_repo():
    with ITEM_REPO as repo:
        yield repo


router = APIRouter(
    tags=[api_group_name],
    prefix=f"/license/{VERSION}"
)

"""
@router.get(path="/purchase", status_code=status.HTTP_200_OK, response_model=list[Item])
async def purchase(request: Request, name: str | None = None, repo=Depends(get_repo) ):
    filters = {
        "name": name
    }
    return get_items(filters, repo)


@router.post(path="/purchase/{type_uuid}", status_code=status.HTTP_201_CREATED)
async def create_license( request: Request, repo=Depends(get_repo) ):
    license_uuid = create_license(repo)

    return {"license UUID": license_uuid}


@router.get(path="/pending", status_code=status.HTTP_200_OK, response_model=list[Item])
async def pending_items( request: Request, repo=Depends(get_repo) ):
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
"""

@router.get(path="/purchase", status_code=status.HTTP_200_OK, response_model=SuccessResponse[list[Item]])
async def purchase(request: Request, name: str | None = None, repo=Depends(get_repo) ):
    filters = {
        "name": name
    }
    items = get_items(filters, repo)
    return create_success_response(data=items)

@router.get(path="/unassigned", status_code=status.HTTP_200_OK, response_model=SuccessResponse[list[Item]])
async def unassigned_items(request: Request, repo=Depends(get_repo)):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": entity_uuid,
        "user_uuid": {"$eq": None, "$exists": True},
        "iat": {"$lt": now},
        "exp": {"$gt": now},
    }
    items = get_items(filters, repo)
    return create_success_response(data=items)

""""

@router.post(path="/assign/{uuid}", status_code=status.HTTP_201_CREATED)
async def assign_license( request: Request, repo=Depends(get_repo) ):
    return {"status": "WIP"}

"""
@router.get(path="/assigned", status_code=status.HTTP_200_OK, response_model=SuccessResponse[list[Item]])
async def assigned_items( request: Request, repo=Depends(get_repo) ):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": entity_uuid,
        "user_uuid": {"$ne": None, "$exists": True},
        "iat": { "$lt": now },
        "exp": { "$gt": now },
    }
    items = get_items(filters, repo)
    return create_success_response(data=items)

"""
@router.post(path="/unassign/{uuid}", status_code=status.HTTP_201_CREATED)
async def unassign_license( request: Request, repo=Depends(get_repo) ):
    return {"status": "WIP"}

"""
@router.get(path="/expired", status_code=status.HTTP_200_OK, response_model=SuccessResponse[list[Item]])
async def expired_items(request: Request, repo=Depends(get_repo)):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": entity_uuid,
        "iat": {"$lt": now},
        "exp": {"$lt": now}
    }
    items = get_items(filters, repo)
    return create_success_response(data=items)

@router.get(path="/license/{uuid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[Item])
async def read_item(request: Request, uuid: str, repo=Depends(get_repo)):
    logging.info(f"read item {uuid}")
    item = get_item(uuid, repo)
    if item is None:
        return Response(status_code=404)
    return create_success_response(data=item)

@router.get(path="/mine", status_code=status.HTTP_200_OK, response_model=SuccessResponse[list[Item]])
async def get_mine(request: Request, repo=Depends(get_repo)):
    now = int(datetime.now().timestamp())
    user_uuid = getattr(request.state, 'user_uuid', None)
    filters = {
        "iat": { "$lt": now },
        "exp": { "$gt": now },
        "user_uuid": user_uuid
    }
    logging.info(f"filters: {filters}")
    items = get_items(filters, repo)
    return create_success_response(data=items)
