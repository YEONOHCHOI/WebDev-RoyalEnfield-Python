'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import MotorBikeType, MotorBike, Order
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    type1 = MotorBikeType(name='650CC', image='1.png', \
        description='''650CC''')
    type2 = MotorBikeType(name='350CC', image='2.png', \
        description='''350CC''')
    type3 = MotorBikeType(name='OFFROAD', image='4.png', \
        description='''OFFROAD''')

    try:
        db.session.add(type1)
        db.session.add(type2)
        db.session.add(type3)
        db.session.commit()
    except:
        return 'There was an issue adding the cities in dbseed function'

    m1 = MotorBike(motorbiketype_id=type1.id, image='1.png', price=11.990,\
        date=datetime(2018, 7, 18),\
        name='Super Meteor 650',\
        description= 'he Super Meteor 650 has a physically imposing presence, yet remains an easy ride, whether you are traversing vast landscapes or heading towards the vanishing point on the horizon.',\ 
        dimension= 'he Super Meteor 650 has a physically imposing presence.') 
    m2 = MotorBike(motorbiketype_id=type1.id, image='2.png', price=10.990,\
        date=datetime(2021, 3, 15),\
        name='INTERCEPTER 650',\
        description= 'The 650 Twin is the rebirth of Royal Enfield’s legendary parallel twin cylinder engine. And it’s driving two Royal Enfield classic motorcycles – the Interceptor and the Continental GT. While classically styled and visually beautiful, the new engine is Royal Enfield’s most forward-looking yet, with a cleaner, elegant look, fewer components, less weight and easier maintenance.',\
        dimension= 'he Super Meteor 650 has a physically imposing presence.') 
    m3 = MotorBike(motorbiketype_id=type1.id, image='3.png', price=11.290,\
        date=datetime(2023, 6, 10),\
        name='CONTINENTAL GT 650',\
        description= 'The 650 Twin is the rebirth of Royal Enfield’s legendary parallel twin cylinder engine.  And it’s driving two Royal Enfield classic motorcycles – the Interceptor and the Continental GT. While classically styled and visually beautiful, the new engine is Royal Enfield’s most forward-looking yet, with a cleaner, elegant look, fewer components, less weight and easier maintenance.',\
        dimension= 'he Super Meteor 650 has a physically imposing presence.')
    m4 = MotorBike(motorbiketype_id=type3.id, image='4.png', price=8.390,\
        date=datetime(2016, 8, 1),\
        name='HIMALAYAN',\
        description= 'The Himalayan cradles a rider in its low seat height, the handlebars and footpegs work perfectly to unite the rider with the  motorcycle for a comfortable upright posture. The inherent mounting points in the front and back let you strap up and set off anytime, while the LCD instrument cluster keeps you on track of miles to maintenance',\                
        dimension= 'he Super Meteor 650 has a physically imposing presence.')
    m5 = MotorBike(motorbiketype_id=type2.id, image='5.png', price=8.240,\
        date=datetime(2019, 5, 20),\
        name='SCRAM 411',\
        description= 'Royal Enfield’s high altitude adventurer DNA has evolved from decades of expeditions and thousands of kilometers of rides across the most challenging terrains in the world. The scram 411 is derived from this very DNA. It is a multi purpose tool optimised for agility;  an ally that’s always ready for whatever life has in store. This is no  cosmetic crossover or pumped up street bike this is a brand new subspecies.',\
        dimension= 'he Super Meteor 650 has a physically imposing presence.')
    m6 = MotorBike(motorbiketype_id=type2.id, image='6.png', price=8.690,\
        date=datetime(2023, 1, 2),\
        name='HUNTER 350',\
        description= 'An old-school, post-war design built around an engine that you can count on. That’s Classic, the machine that bears on simple pleasures of motorcycling, while being dependable enough to ride through any terrain. In it, the tradition of an iconic past exists in harmony with moderntechnology. Timeless, looking through tomorrow.',\
        dimension= 'he Super Meteor 650 has a physically imposing presence.')
    try:
        db.session.add(m1)
        db.session.add(m2)
        db.session.add(m3)
        db.session.add(m4)
        db.session.add(m5)
        db.session.add(m6)
        db.session.commit()
    except:
        return 'There was an issue adding a tour in dbseed function'

    return 'DATA LOADED'