## More about this http://flask.pocoo.org/docs/patterns/sqlalchemy/# ##
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

if os.getenv('TEST') == 'yes':
    engine = create_engine('sqlite:///test.db', convert_unicode=True, echo=False)
else:
    engine = create_engine('sqlite:///data.db', convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import model
    Base.metadata.create_all(bind=engine)
    
def commit():
    try:
        db_session.commit()
        return True
    except IntegrityError as (statement):
        #Write out error
        print "IntegrityError \"{0}\" for {1}".format(statement.orig, statement.params)
        #Rollback
        db_session.rollback()
        #Raise new Exception
        if(statement.connection_invalidated):
            print "Program error, connection invalidated to Database, quitting"
        return False

##Helper for the model stuff
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator

class ASCII(TypeDecorator):
    '''
    Prefixes Unicode values with "PREFIX:" on the way in and
    strips it off on the way out.
    '''
    impl = String

    def process_result_value(self, value, dialect):
        if value is not None:
            return str(value)
        return value
