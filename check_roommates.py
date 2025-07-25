from app import create_app
from models.models import Roommate

app = create_app()

with app.app_context():
    roommates = Roommate.query.all()
    print(f"Total roommates in database: {len(roommates)}")
    print("\nFirst 5 roommates with their images:")
    for i, roommate in enumerate(roommates[:5]):
        print(f"{i+1}. {roommate.name} - {roommate.gender}")
        print(f"   Location: {roommate.location}")
        print(f"   Budget: ₹{roommate.budget}")
        print(f"   Image: {roommate.image_url}")
        print(f"   About: {roommate.about}")
        print(f"   Hobbies: {roommate.hobbies}")
        print() 