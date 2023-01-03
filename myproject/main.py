# project over Rainbow six siege.
import random

from fastapi import Depends, FastAPI, HTTPException, Path, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import os
import crud
import models
import schemas
import auth
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POST REQUEST

# http://127.0.0.1:8000/player/
@app.post("/player/", response_model=schemas.Player)
def create_user(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    does_email_exist = crud.get_user_by_email(db, email=player.email)
    does_username_exist = crud.get_user_by_username(db, username=player.username)
    if does_email_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif does_username_exist:
        raise HTTPException(status_code=400, detail="Username already registered")

    return crud.create_player(db=db, player=player)


# http://127.0.0.1:8000/map/
@app.post("/map/", response_model=schemas.Map)
async def create_map(map_map: schemas.Map, db: Session = Depends(get_db)):
    if crud.get_map_by_name(db, map_map.map_name):
        raise HTTPException(status_code=400, detail="Map already exists")
    else:
        crud.create_map(db, map_map)

    return map_map

@app.post("/op/", response_model=schemas.Map)
async def create_op(op: schemas.Operator, db: Session = Depends(get_db)):
    if crud.get_operator_by_name(db, op.operator_name):
        raise HTTPException(status_code=400, detail="Operator already exists")
    else:
        crud.create_op(db, op)

    return op

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    # Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}

# PUT REQUEST

# http://127.0.0.1:8000/update/player/1
@app.put("/update/player/{player_id}", response_model=schemas.Player)
async def update_player(player: schemas.PlayerCreate, db: Session = Depends(get_db),
                        player_id: int = Path(ge=0, le=60, default=1), token: str = Depends(auth.oauth2_scheme)):
    return crud.update_player(db=db, player=player, player_id=player_id)


# DELETE REQUEST

# http://127.0.0.1:8000/delete/player/1
@app.delete("/delete/player/{player_id}", response_model=schemas.Player)
async def delete_player(db: Session = Depends(get_db), player_id: int = Path(ge=0, le=60, default=1), token: str = Depends(auth.oauth2_scheme)):
    return crud.delete_player(db=db, player_id=player_id)


# GET REQUEST

# http://127.0.0.1:8000/get/player/1
@app.get("/get/player/{player_id}")
async def get_player_by_id(db: Session = Depends(get_db), player_id: int = Path(ge=0, le=60, default=1)):
    if not crud.get_player_by_id(db=db, player_id=player_id):
        raise HTTPException(status_code=400, detail=f"No player with id {player_id}")
    return crud.get_player_by_id(db, player_id)

@app.get("/players/", response_model=list)
def read_users(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.get_all_players(db)

# Get request voor een map op te vragen met ID
# http://127.0.0.1:8000/get/map/1
@app.get("/get/map/{map_id}", response_model=str)
async def get_map_by_id(db: Session = Depends(get_db), map_id: int = Path(ge=0, le=60, default=1)):
    return crud.get_map_by_id(db, map_id)


# http://127.0.0.1:8000/get/player/favoritemap/1
@app.get("/get/player/favoritemap/{player_id}", response_model=schemas.Map)
async def get_favorite_map_of_player(db: Session = Depends(get_db), player_id: int = Path(ge=0, le=60, default=1)):
    return crud.get_favorite_map_of_player(db, player_id)


# http://127.0.0.1:8000/map/random?amount=2
@app.get("/map/random", response_model=list)
async def get_random_maps(db: Session = Depends(get_db), amount: int = Query(default=1, gt=0)):
    # een temp copy van de maps, zodat we geen duplicates krijgen
    maps_copy = crud.get_all_maps(db).copy()
    resultaat = []
    # Als we out of bounds gaan (het gevraagde aantal is groter dan of gelijk aan de lengte van de lijst,
    # dan laten we gewoon alle maps zien
    if amount >= len(crud.get_all_maps(db)):
        return crud.get_all_maps(db)
    else:
        for i in range(amount):
            # we pakken een random getal tussen 0 en de grootte van de lijst.
            random_getal = random.randint(0, len(maps_copy) - 1)
            rand_map = maps_copy[random_getal]
            # Voegen de geselecteerde random maps aan de lijst
            resultaat.append(rand_map)
            # We verwijderen de geselecteerde random maps zodat we geen duplicates krijgen :)
            maps_copy.remove(rand_map)
    return resultaat
