from app import app
from extensions import db
from models.models import PG, Roommate

with app.app_context():
    test_pg = PG(
        name='Test PG',
        city='Test City',
        address='123 Test Street',
        price=5000,
        sharing_type='PG',
        amenities='WiFi, AC, Laundry',
        image_url='https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg',
        description='A test PG for debugging.',
        gallery_images='https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg',
        food_menu='{}'
    )
    db.session.add(test_pg)

    test_roommate = Roommate(
        name='Test Roommate',
        gender='Male',
        location='Test City',
        budget=6000,
        about='A test roommate for debugging.',
        image_url='https://images.pexels.com/photos/3777943/pexels-photo-3777943.jpeg',
        hobbies='reading, music'
    )
    db.session.add(test_roommate)

    db.session.commit()
    print('Test PG and Roommate added!') 