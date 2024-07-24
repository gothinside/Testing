import pytest
import json
import httpx
from conftest import create_test_auth_headers_for_user, create_new_user

async def test_smth(client, create_new_role, event_loop):
    user = await create_new_user()
    res = await client.delete("users/{user.id}", headers = create_test_auth_headers_for_user(user.email))
    assert res.status_code == 200
routers.py
@router.delete("/{user_id}", response_model= UserBase)
async def delete_user(user_id:int,
                      session: AsyncSession = Depends(get_db),
                      cur_user: User = Depends(get_current_user_from_token)):
    if cur_user.id == user_id:
        user = await crud.delete_user(session, user_id)
        return user
    elif is_admin(session, cur_user.id) and not is_admin(session, user_id):
        user = await crud.delete_user(session, user_id)
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
