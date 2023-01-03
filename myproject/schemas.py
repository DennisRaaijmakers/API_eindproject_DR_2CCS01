from pydantic import BaseModel


# classes van operator
class OperatorBase(BaseModel):
    opp_id: int | None = -1
    operator_name: str | None = "Invalid"
    primary_weapon: str | None = "Invalid"
    secondary_weapon: str | None = "Invalid"


class OperatorCreate(OperatorBase):
    pass


class Operator(OperatorBase):
    class Config:
        # ORM_mode zorgt ervoor dat je het ook object georienteerd kan schrijven ipv als een python dictionary
        orm_mode = True


# classes van players
class PlayerBase(BaseModel):
    player_id: int | None = -1
    fav_map_id: int | None = -1
    username: str | None = "Invalid"
    name: str | None = "Invalid"
    email: str | None = "Invalid"
    region: str | None = "Invalid"
    mmr: int | None = 0


class PlayerCreate(PlayerBase):
    password: str | None = "Invalid"


class Player(PlayerBase):
    class Config:
        # ORM_mode zorgt ervoor dat je het ook object georienteerd kan schrijven ipv als een python dictionary
        orm_mode = True


class MapBase(BaseModel):
    map_id: int | None = -1
    map_name: str | None = "Invalid"


class MapCreate(MapBase):
    pass


class Map(MapBase):
    class Config:
        # ORM_mode zorgt ervoor dat je het ook object georienteerd kan schrijven ipv als een python dictionary
        orm_mode = True
