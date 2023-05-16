from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Course

import ipdb;

if __name__=='__main__':
    engine = create_engine('sqlite:///gradebook.db')
    Session = sessionmaker(engine)
    session = Session()

    ipdb.set_trace()