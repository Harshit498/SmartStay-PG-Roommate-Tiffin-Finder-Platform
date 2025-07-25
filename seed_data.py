from faker import Faker
from models.models import db, PG, Roommate, TiffinService, Event, TiffinVendor
from app import app
import random
import os
import json

fake = Faker()

PG_IMAGES = [
    'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg',
    'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg',
    'https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg',
    'https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg',
    'https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg',
]
ROOMMATE_IMAGES = [
    'https://images.pexels.com/photos/3777943/pexels-photo-3777943.jpeg',  # Indian man in casual wear
    'https://images.pexels.com/photos/3777946/pexels-photo-3777946.jpeg',  # Indian woman in traditional dress
    'https://images.pexels.com/photos/3777949/pexels-photo-3777949.jpeg',  # Indian man in formal wear
    'https://images.pexels.com/photos/3777952/pexels-photo-3777952.jpeg',  # Indian woman in modern attire
    'https://images.pexels.com/photos/3777955/pexels-photo-3777955.jpeg',  # Indian man in casual shirt
    'https://images.pexels.com/photos/3777958/pexels-photo-3777958.jpeg',  # Indian woman in ethnic wear
    'https://images.pexels.com/photos/3777961/pexels-photo-3777961.jpeg',  # Indian man in smart casual
    'https://images.pexels.com/photos/3777964/pexels-photo-3777964.jpeg',  # Indian woman in contemporary dress
    'https://images.pexels.com/photos/3777967/pexels-photo-3777967.jpeg',  # Indian man in business casual
    'https://images.pexels.com/photos/3777970/pexels-photo-3777970.jpeg',  # Indian woman in fusion wear
    'https://images.pexels.com/photos/3777973/pexels-photo-3777973.jpeg',  # Indian man in traditional kurta
    'https://images.pexels.com/photos/3777976/pexels-photo-3777976.jpeg',  # Indian woman in salwar kameez
    'https://images.pexels.com/photos/3777979/pexels-photo-3777979.jpeg',  # Indian man in western formal
    'https://images.pexels.com/photos/3777982/pexels-photo-3777982.jpeg',  # Indian woman in modern ethnic
    'https://images.pexels.com/photos/3777985/pexels-photo-3777985.jpeg',  # Indian man in casual ethnic
    'https://images.pexels.com/photos/3777988/pexels-photo-3777988.jpeg',  # Indian woman in contemporary fusion
]
TIFFIN_IMAGES = [
    'https://images.pexels.com/photos/461382/pexels-photo-461382.jpeg',  # Indian thali
    'https://images.pexels.com/photos/106343/pexels-photo-106343.jpeg',  # Indian curry
    'https://images.pexels.com/photos/2232/vegetables-italian-pizza-restaurant.jpg',  # Indian veg food
    'https://images.pexels.com/photos/461382/pexels-photo-461382.jpeg',  # Indian thali (repeat for more variety)
    'https://images.pexels.com/photos/209540/pexels-photo-209540.jpeg',  # Indian dal rice
]
EVENT_IMAGES = [
    'https://images.pexels.com/photos/1679825/pexels-photo-1679825.jpeg',
    'https://images.pexels.com/photos/20787/pexels-photo.jpg',
    'https://images.pexels.com/photos/21014/pexels-photo.jpg',
]

ONLINE_STUDENT_IMAGES = [
    "https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg",
    "https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg",
    "https://images.pexels.com/photos/1468379/pexels-photo-1468379.jpeg",
    "https://images.pexels.com/photos/1707830/pexels-photo-1707830.jpeg",
    "https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg",
    "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg",
    "https://images.pexels.com/photos/91227/pexels-photo-91227.jpeg",
    "https://images.pexels.com/photos/1130627/pexels-photo-1130627.jpeg",
    "https://images.pexels.com/photos/2916828/pexels-photo-2916828.jpeg",
    "https://images.pexels.com/photos/1468378/pexels-photo-1468378.jpeg",
    "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg",
    "https://images.pexels.com/photos/1468377/pexels-photo-1468377.jpeg",
    "https://images.pexels.com/photos/1707828/pexels-photo-1707828.jpeg",
    "https://images.pexels.com/photos/1468376/pexels-photo-1468376.jpeg",
    "https://images.pexels.com/photos/2916829/pexels-photo-2916829.jpeg",
    "https://images.pexels.com/photos/1468375/pexels-photo-1468375.jpeg",
    "https://images.pexels.com/photos/2916830/pexels-photo-2916830.jpeg",
    "https://images.pexels.com/photos/1468374/pexels-photo-1468374.jpeg",
    "https://images.pexels.com/photos/2916831/pexels-photo-2916831.jpeg",
    "https://images.pexels.com/photos/1468373/pexels-photo-1468373.jpeg",
]

INDIAN_STUDENT_IMAGES = [
    f"static/images/roommates/student{i+1}.jpg" for i in range(20)
]

def seed_pgs(db, PG):
    amenities_list = ['WiFi', 'AC', 'Laundry', 'Food', 'Parking', 'CCTV', 'Power Backup', 'Gym', 'Swimming Pool', 'Housekeeping', 'Security', 'Garden', 'Balcony', 'Lift', 'Fire Safety']
    sharing_types = ['Single', 'Double', 'Triple', 'Dormitory']
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
    property_types = [('PG', 30), ('Villa', 20), ('Flat', 20)]
    descriptions = [
        "Spacious and well-ventilated, perfect for students and working professionals. Close to metro and market.",
        "Modern amenities with 24/7 security and power backup. Peaceful neighborhood and friendly community.",
        "Fully furnished with high-speed WiFi, daily housekeeping, and delicious home-cooked meals.",
        "Ideal for those seeking comfort and convenience. Walking distance to major IT parks and colleges.",
        "Elegant interiors, ample parking, and a beautiful garden. Experience luxury living at an affordable price.",
        "Safe and secure with biometric entry, CCTV surveillance, and dedicated maintenance staff.",
        "Enjoy a vibrant lifestyle with access to gym, swimming pool, and recreational areas.",
        "Pet-friendly property with spacious rooms and a large balcony for relaxation.",
        "Prime location with easy access to public transport, shopping malls, and hospitals.",
        "Perfect blend of privacy and community living. Join a diverse group of residents from across India.",
        "Recently renovated with modern fittings, modular kitchen, and stylish bathrooms.",
        "Eco-friendly property with rainwater harvesting and solar panels for sustainable living.",
        "Exclusive villa with private lawn, barbecue area, and rooftop terrace for parties.",
        "Family-friendly flat with kids’ play area, study room, and 24/7 water supply.",
        "Affordable PG with flexible meal plans, laundry service, and regular social events."
    ]
    indian_gallery = [
        'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg',
        'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg',
        'https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg',
        'https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg',
        'https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg',
        'https://images.pexels.com/photos/210604/pexels-photo-210604.jpeg',
        'https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg',
        'https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg',
    ]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for ptype, count in property_types:
        for _ in range(count):
            amenities = ', '.join(fake.random_elements(elements=amenities_list, length=random.randint(4, 7), unique=True))
            gallery = ','.join(fake.random_elements(elements=indian_gallery, length=5, unique=True))
            weekly_menu = {"days": []}
            for day in days:
                breakfast = fake.random_elements(elements=["Aloo Paratha", "Poha", "Idli Sambar", "Masala Dosa", "Upma", "Puri Bhaji"], length=3, unique=True)
                lunch = fake.random_elements(elements=["Dal Tadka", "Paneer Butter Masala", "Rajma Chawal", "Chole Rice", "Mix Veg", "Bhindi Masala"], length=3, unique=True)
                dinner = fake.random_elements(elements=["Boondi Raita", "Cabbage Mutter", "Chapati", "Dhaba Dal", "Green Salad", "Jeera Rice"], length=3, unique=True)
                weekly_menu["days"].append({
                    "day": day,
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner
                })
            pg = PG(
                name=fake.company() + f' {ptype}',
                city=random.choice(cities),
                address=fake.address(),
                price=random.randint(4000, 25000) if ptype != 'Flat' else random.randint(10000, 50000),
                sharing_type=ptype,
                amenities=amenities,
                image_url=random.choice(indian_gallery),
                description=random.choice(descriptions) + ' ' + fake.paragraph(nb_sentences=3),
                gallery_images=gallery,
                food_menu=json.dumps(weekly_menu)
            )
            db.session.add(pg)
    db.session.commit()

def seed_roommates(db, Roommate):
    indian_names = [
        'Rahul Sharma', 'Priya Mehta', 'Aman Khan', 'Sneha Singh', 'Rohit Verma', 'Anjali Patel',
        'Vikram Joshi', 'Pooja Nair', 'Siddharth Gupta', 'Neha Reddy', 'Arjun Kapoor', 'Zara Khan',
        'Aditya Malhotra', 'Ishita Sharma', 'Rohan Desai', 'Kavya Iyer', 'Dhruv Patel', 'Mira Joshi',
        'Karan Singh', 'Tanvi Reddy'
    ]
    indian_cities = [
        'Rajouri Garden, Delhi', 'HSR Layout, Bangalore', 'Hinjewadi, Pune', 'Gomti Nagar, Lucknow',
        'Powai, Mumbai', 'Salt Lake, Kolkata', 'Banjara Hills, Hyderabad', 'Anna Nagar, Chennai',
        'Sector 62, Noida', 'Vastrapur, Ahmedabad', 'Koramangala, Bangalore', 'Andheri West, Mumbai',
        'Koregaon Park, Pune', 'Gurgaon Sector 56, Delhi NCR', 'JP Nagar, Bangalore', 'Thane West, Mumbai',
        'Kharadi, Pune', 'Whitefield, Bangalore', 'Noida Sector 135, Delhi NCR', 'Chembur, Mumbai'
    ]
    bios = [
        'Looking for a friendly flatmate to share chai and late-night study sessions.',
        'Early riser, working in IT, need peaceful PG near office.',
        'Veg, non-smoker, love cricket and movies. Need a fun roommate!',
        'MBA student, prefer clean and quiet place. Study-friendly environment.',
        'Love to cook, want foodie roommate. Gym lover, early morning walks.',
        'Working professional, prefer calm and safe locality.',
        'Binge-watcher, gamer, and chai addict. Need easy-going flatmate.',
        'Love music and travel. Looking for a positive and tidy roommate.',
        'College student, need someone to share rent and good vibes.',
        'Book lover, introvert, need peaceful PG for studies.',
        'Software developer, love coding and coffee. Need tech-savvy roommate.',
        'Medical student, need quiet environment for studies. Prefer vegetarian roommate.',
        'Marketing professional, social butterfly, love Bollywood movies and food.',
        'Design student, creative soul, love art and music. Need inspiring roommate.',
        'Finance analyst, organized and clean. Looking for responsible flatmate.',
        'Journalism student, love writing and photography. Need creative roommate.',
        'Law student, serious about studies. Prefer quiet and focused environment.',
        'Architecture student, love design and travel. Need artistic roommate.',
        'Engineering student, love gadgets and gaming. Need tech-friendly roommate.',
        'Fashion design student, creative and stylish. Looking for trendy roommate.'
    ]
    budgets = [3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000]
    genders = ['Male', 'Female']
    hobbies_list = [
        'cricket, music, movies',
        'reading, yoga, cooking',
        'football, coding, music',
        'dancing, painting, reading',
        'gym, cooking, badminton',
        'movies, meditation, running',
        'gaming, music, chai',
        'travel, photography, music',
        'books, chess, movies',
        'gardening, reading, yoga',
        'coding, coffee, tech',
        'studies, reading, meditation',
        'Bollywood, food, socializing',
        'art, music, creativity',
        'finance, organization, fitness',
        'writing, photography, journalism',
        'law, studies, focus',
        'design, travel, architecture',
        'gaming, gadgets, technology',
        'fashion, style, creativity'
    ]
    for i in range(20):
        local_img = INDIAN_STUDENT_IMAGES[i]
        # Use local image if it exists, else fallback to online image
        if os.path.exists(local_img):
            image_url = local_img
        else:
            image_url = ONLINE_STUDENT_IMAGES[i]
        roommate = Roommate(
            name=indian_names[i],
            gender=genders[i % 2],
            location=indian_cities[i],
            budget=budgets[i],
            about=bios[i],
            image_url=image_url,
            hobbies=hobbies_list[i]
        )
        db.session.add(roommate)
    db.session.commit()
    print(f"Seeded {Roommate.query.count()} roommates.")

def seed_tiffin_services(db, TiffinService):
    for _ in range(10):
        tiffin = TiffinService(
            name=fake.company() + ' Tiffin',
            menu=fake.sentence(nb_words=10),
            cost=random.randint(1500, 5000),
            area_covered=fake.city(),
            contact_info=fake.phone_number(),
            image_url=random.choice(TIFFIN_IMAGES)
        )
        db.session.add(tiffin)
    db.session.commit()

def seed_tiffin_vendors(db, TiffinVendor):
    import json
    # Delete all existing vendors
    TiffinVendor.query.delete()
    db.session.commit()
    vendor_names = [
        'Delight Tiffins', 'HomeTaste Foods', 'Spicy Curry House', 'Healthy Meals', 'Urban Tiffin',
        'Maa Ki Rasoi', 'Tiffin Express', 'Veggie Treats', 'Desi Zaika', 'City Tiffin Service'
    ]
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    breakfast_options = [
        'Aloo Paratha', 'Poha', 'Idli Sambar', 'Masala Dosa', 'Upma', 'Puri Bhaji', 'Coconut Chutney', 'Plain Idly', 'South Mango Sambar', 'Live Tea - Ginger', 'Bread Pakora'
    ]
    lunch_options = [
        'Dal Tadka', 'Paneer Butter Masala', 'Rajma Chawal', 'Chole Rice', 'Mix Veg', 'Bhindi Masala', 'Brinjal Aloo Mokai Kara Kulambu', 'Curd Rice With Fruits', 'Curry Leaves Rasam', 'Pickle', 'Plain Rice', 'Veg Pachadi', 'Butter Milk - South Style'
    ]
    snacks_options = [
        'Live Tea - cardamom', 'Pani Poori', 'Samosa', 'Pakora', 'Fruit Salad', 'Biscuits'
    ]
    dinner_options = [
        'Chapati', 'Curry Leaves Rasam', 'Egg Masala South', 'Ghee Rice', 'Gobhi Capsicum Masala', 'Plain Rice', 'Dal Makhani', 'Veg Biryani', 'Aloo Tamatar', 'Bhindi Fry'
    ]
    for i in range(10):
        # Build weekly menu
        weekly_menu = {"days": []}
        for d in days:
            weekly_menu["days"].append({
                "day": d,
                "breakfast": random.sample(breakfast_options, 4),
                "lunch": random.sample(lunch_options, 6),
                "snacks": random.sample(snacks_options, 2),
                "dinner": random.sample(dinner_options, 5)
            })
        vendor = TiffinVendor(
            name=vendor_names[i],
            description=fake.paragraph(nb_sentences=3),
            location=random.choice(locations),
            phone=fake.phone_number(),
            image_url=random.choice(TIFFIN_IMAGES),
            is_approved=True,
            food_menu=json.dumps(weekly_menu)
        )
        db.session.add(vendor)
    db.session.commit()

def seed_events(db, Event):
    event_names = [
        'PG Fresher Welcome Party',
        'Roommate Meetup & Chai',
        'Tiffin Food Festival',
        'Flatmate Cricket Match',
        'Diwali Celebration Night'
    ]
    event_dates = [
        '15-07-2025', '22-07-2025', '05-08-2025', '12-08-2025', '01-11-2025'
    ]
    event_times = [
        '6:00 PM', '5:30 PM', '1:00 PM', '8:00 AM', '7:00 PM'
    ]
    event_locations = [
        'Rajouri Garden, Delhi', 'HSR Layout, Bangalore', 'Powai, Mumbai', 'Gomti Nagar, Lucknow', 'Salt Lake, Kolkata'
    ]
    event_descriptions = [
        'Welcome new PG mates with music, snacks, and fun games! All are invited.',
        'Meet your future roommates over chai and samosa. Share your preferences and make friends.',
        'Taste the best tiffin services in town! Free samples and special offers for students.',
        'Join us for a friendly cricket match between flatmates. All skill levels welcome!',
        'Celebrate Diwali with your PG family. Diyas, sweets, and fireworks!'
    ]
    event_images = [
        'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg',  # Party
        'https://images.pexels.com/photos/163077/pexels-photo-163077.jpeg',   # Chai meetup
        'https://images.pexels.com/photos/461382/pexels-photo-461382.jpeg',   # Food fest
        'https://images.pexels.com/photos/1632091/pexels-photo-1632091.jpeg', # Cricket
        'https://images.pexels.com/photos/1695052/pexels-photo-1695052.jpeg'  # Diwali
    ]
    event_contacts = [
        '+91-9876543210', '+91-9123456789', '+91-9988776655', '+91-9001122334', '+91-9876123450'
    ]
    for i in range(5):
        event = Event(
            name=event_names[i],
            date=event_dates[i],
            time=event_times[i],
            location=event_locations[i],
            description=event_descriptions[i],
            image_url=event_images[i],
            contact_info=event_contacts[i]
        )
        db.session.add(event)
    db.session.commit()

def main():
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        seed_pgs(db, PG)
        seed_roommates(db, Roommate)
        seed_tiffin_services(db, TiffinService)
        seed_tiffin_vendors(db, TiffinVendor)
        seed_events(db, Event)
        print('Database seeded!')

if __name__ == '__main__':
    main() 