from sqlalchemy.orm import Session

import models
import schemas
import auth

# map variablen
chalet = {
    "map_id": 1,
    "map_name": "chalet"
}
oregon = {
    "map_id": 2,
    "map_name": "oregon"
}
clubhouse = {
    "map_id": 3,
    "map_name": "clubhouse"
}


# read data

def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Player).filter(models.Player.email == email).first()

def get_player_by_id(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.player_id == player_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Player).filter(models.Player.username == username).first()


def get_map_by_name(db: Session, map_name: str):
    return db.query(models.FavoriteMap).filter(models.FavoriteMap.map_name == map_name).first()


def get_map_by_id(db: Session, map_id: int):
    return db.query(models.FavoriteMap).filter(models.FavoriteMap.map_id == map_id).first().map_name


def get_all_maps(db: Session):
    print(db.query(models.FavoriteMap).all())
    return db.query(models.FavoriteMap).all()

def get_operator_by_name(db: Session, operator_name: str):
    return db.query(models.Operator).filter(models.Operator.operator_name == operator_name).first()

# create data


def create_player(db: Session, player: schemas.PlayerCreate):
    secure_password = auth.get_password_hash(player.password)
    db_user = models.Player(player_id=len(get_all_players(db))+1,
                            fav_map_id=player.fav_map_id,
                            username=player.username,
                            name=player.name,
                            email=player.email,
                            region=player.region,
                            mmr=player.mmr,
                            password=secure_password)
    db.add(db_user)
    db.commit()
    # print("--------------------------------------------------------------------")
    # print(type(db_user))
    db.refresh(db_user)
    return db_user


# update data
def update_player(db: Session, player_id: int, player: schemas.PlayerCreate):
    secure_password = auth.get_password_hash(player.password)
    db_user = db.query(models.Player).filter(models.Player.player_id == player_id).first()
    db_user.fav_map_id = player.fav_map_id
    db_user.username = player.username
    db_user.name = player.name
    db_user.email = player.email
    db_user.region = player.region
    db_user.mmr = player.mmr
    db_user.password = secure_password
    db.commit()
    # print(type(db_user))
    db.refresh(db_user)
    return db_user


# delete data

def delete_player(db: Session, player_id: int):
    print(player_id)
    db_user = db.query(models.Player).filter(models.Player.player_id == player_id).first()
    db.delete(db_user)
    db.commit()
    return None

def get_favorite_map_of_player(db: Session, player_id: int):
    # Vraagt de favorite ID van de map van de player op
    favorite_map_id = db.query(models.Player).filter(models.Player.player_id == player_id).first().fav_map_id
    # Met dat ID vragen de map met dat ID op
    return db.query(models.FavoriteMap).filter(models.FavoriteMap.map_id == favorite_map_id).first()

def create_map(db: Session, map_p: schemas.Map):
    print("TYPE IS ", map_p.map_name)
    db_map = models.FavoriteMap(map_name=map_p.map_name)
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map

def create_op(db: Session, op: schemas.Operator):
    db_op = models.Operator(operator_name=op.operator_name,
                            primary_weapon=op.primary_weapon,
                            secondary_weapon=op.secondary_weapon)
    db.add(db_op)
    db.commit()
    db.refresh(db_op)
    return db_op