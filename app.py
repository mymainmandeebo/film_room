def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        db = read_db()
        live_user = next((u for u in db["users"] if u["id"] == payload.get("sub")), None)
        if live_user:
            return {
                "sub": live_user["id"],
                "id": live_user["id"],
                "username": live_user["username"],
                "role": live_user["role"],
                "player_name": live_user.get("player_name"),
                "project_ids": live_user.get("project_ids", [])
            }
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

