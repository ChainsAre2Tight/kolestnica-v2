from flask_sqlalchemy import SQLAlchemy
import database.models as models
import sqlalchemy.exc
import utils.my_exceptions as exc
from database.caching import CacheController

@CacheController.read_through_cache('key')
def get_user_id_by_sessionId(
        key: str,
        db: SQLAlchemy,
    ) -> int:

    try:
        return db.session.query(models.Session).\
            filter(models.Session.uuid == key).one().user_id
    except sqlalchemy.exc.NoResultFound:
        raise exc.UserNotExistsException