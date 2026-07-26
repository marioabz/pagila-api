from sqlalchemy.ext.automap import automap_base

from .engine import db_engine

Base = automap_base()


# reflect the tables
Base.prepare(autoload_with=db_engine)
