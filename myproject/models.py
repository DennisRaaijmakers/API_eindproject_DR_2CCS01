from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Operator(Base):
    __tablename__ = "operator"

    opp_id = Column(Integer, primary_key=True, index=True)
    operator_name = Column(String, unique=True, index=True)
    primary_weapon = Column(String, index=True)
    secondary_weapon = Column(String, index=True)


class Player(Base):
    __tablename__ = "player"

    player_id = Column(Integer, primary_key=True, index=True)
    fav_map_id = Column(Integer, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    region = Column(String, index=True)
    mmr = Column(Integer)


# {
#     "fav_map_id": 2,
#     "username": "test",
#     "name": "test",
#     "email": "test@test.com",
#     "password": "abc123!",
#     "region": "Europe",
#     "mmr": 2000
# }

class FavoriteMap(Base):
    __tablename__ = "favorite map"

    map_id = Column(Integer, primary_key=True, index=True)
    map_name = Column(String, index=True)