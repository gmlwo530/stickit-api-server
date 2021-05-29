from app.crud.base import CRUDBase
from app.models.collect import Collect, CollectCreate, CollectUpdate


class CRUDCollect(CRUDBase[Collect, CollectCreate, CollectUpdate]):
    pass


collect = CRUDCollect(Collect)
