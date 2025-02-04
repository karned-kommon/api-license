from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status, Depends, Request
from datetime import datetime

from config.config import API_TAG_NAME, ITEM_REPO
from decorators.check_permission import check_permissions
from models.item_model import Item
from services.items_service import create_item, get_items, get_item, update_item, delete_item

def get_repo():
    with ITEM_REPO as repo:
        yield repo

router = APIRouter(
    tags=[API_TAG_NAME]
)


@router.get("/purchase", status_code=status.HTTP_200_OK, response_model=list[Item])
async def purchase(
        request: Request,
        repo=Depends(get_repo),
        name: Optional[str] = Query(None, description="Name of License"),
):
    filters = {k: v for k, v in {
        "name": name,
    }.items() if v is not None}

    return get_items(filters, repo)


@router.post("/purchase/{type_uuid}", status_code=status.HTTP_201_CREATED)
async def create_license(request: Request, repo=Depends(get_repo)):
    license_uuid =  create_license(repo)

    return {"license UUID": license_uuid}


@router.get("/unassigned", status_code=status.HTTP_200_OK, response_model=list[Item])
async def unassigned_items(
        request: Request,
        repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        },
        "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)

@router.get("/assigned", status_code=status.HTTP_200_OK, response_model=list[Item])
async def assigned_items(
        request: Request,
        repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        },
        "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)


@router.get("/expired", status_code=status.HTTP_200_OK, response_model=list[Item])
async def expired_items(
        request: Request,
        repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        },
        "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)

@router.get("/pending", status_code=status.HTTP_200_OK, response_model=list[Item])
async def pending_items(
        request: Request,
        repo=Depends(get_repo)
):
    now = int(datetime.now().timestamp())
    entity_uuid = request.state.entity_uuid
    filters = {
        "entity_uuid": {
            "$eq": entity_uuid
        },
        "exp": {
            "$lt": now
        }
    }
    return get_items(filters, repo)














@router.post("/", status_code=status.HTTP_201_CREATED)
@check_permissions(['create'])
async def create_new_item(request: Request, item: Item, repo=Depends(get_repo)) -> dict:
    item.created_by = request.state.token_info.get('user_id')
    new_uuid = create_item(item, repo)
    return {"uuid": new_uuid}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Item])
@check_permissions(['read', 'read_own'])
async def read_items(
    request: Request,
    uuid: Optional[str] = Query(None, description="User : UUID"),
    username: Optional[str] = Query(None, description="User : username"),
    firstname: Optional[str] = Query(None, description="User : firstname"),
    lastname: Optional[str] = Query(None, description="User : lastname"),
    email: Optional[str] = Query(None, description="User : email"),
    created_by: Optional[str] = Query(None, description="User who created this step"),
    repo=Depends(get_repo)
):
    filters = {k: v for k, v in {
        "uuid": uuid,
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "created_by": created_by,
    }.items() if v is not None}

    return get_items(filters, repo)


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=Item)
@check_permissions(['read', 'read_own'])
async def read_item(request: Request, uuid: str, repo=Depends(get_repo)):
    item = get_item(uuid, repo)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@check_permissions(['delete', 'delete_own'])
async def delete_existing_item(request: Request, uuid: str, repo=Depends(get_repo)):
    delete_item(uuid, repo)

@router.post("/{uuid}/reset-password", status_code=status.HTTP_201_CREATED)
@check_permissions(['update'])
async def reset_password(request: Request, item: Item, repo=Depends(get_repo)) -> dict:
    return {"return": 'TODO'}


