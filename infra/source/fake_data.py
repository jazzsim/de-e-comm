# List of 10 random product categories with descriptions
CATEGORIES = [
    {"category": "Electronics", "description": "Devices and gadgets powered by electricity, ranging from smartphones to computers."},
    {"category": "Home Appliances", "description": "Household items designed to simplify tasks such as cooking, cleaning, and maintenance."},
    {"category": "Clothing", "description": "Wearable items including garments, shoes, and accessories for all seasons and occasions."},
    {"category": "Sports Equipment", "description": "Gear and tools used for sports and physical activities, from soccer balls to tennis rackets."},
    {"category": "Beauty Products", "description": "Cosmetic items for skincare, haircare, and makeup that enhance appearance and well-being."},
    {"category": "Toys & Games", "description": "Play items for children or adults, including board games, action figures, and puzzles."},
    {"category": "Books", "description": "Printed or digital works of literature, including fiction, non-fiction, and educational texts."},
    {"category": "Furniture", "description": "Functional and decorative pieces for home or office spaces, including chairs, tables, and storage."},
    {"category": "Groceries", "description": "Everyday food and household items bought from a grocery store."},
    {"category": "Health & Wellness", "description": "Products focused on maintaining or improving physical and mental health, including supplements and fitness tools."}
]

# List of 20 products based on the above categories, with descriptions
PRODUCTS = [
    {"product": "Smartphone", "category": "Electronics", "description": "A handheld mobile device for communication, internet browsing, and media consumption."},
    {"product": "Laptop", "category": "Electronics", "description": "A portable personal computer with a screen, keyboard, and battery."},
    {"product": "Bluetooth Speaker", "category": "Electronics", "description": "A wireless speaker that connects to devices via Bluetooth to play audio."},
    {"product": "Smartwatch", "category": "Electronics", "description": "A wearable device that offers timekeeping, fitness tracking, and notifications."},
    {"product": "Headphones", "category": "Electronics", "description": "Audio devices worn over or in the ears to listen to music, calls, or podcasts."},
    
    {"product": "Washing Machine", "category": "Home Appliances", "description": "An appliance used to wash laundry automatically."},
    {"product": "Air Purifier", "category": "Home Appliances", "description": "A device that removes contaminants from the air to improve indoor air quality."},
    {"product": "Refrigerator", "category": "Home Appliances", "description": "An appliance used to store food and drinks at low temperatures to preserve freshness."},
    {"product": "Microwave Oven", "category": "Home Appliances", "description": "An appliance used to quickly heat or cook food using microwave radiation."},
    {"product": "Vacuum Cleaner", "category": "Home Appliances", "description": "A device for cleaning floors, carpets, and upholstery by suction."},
    
    {"product": "T-shirt", "category": "Clothing", "description": "A casual short-sleeved shirt made from cotton or synthetic fabric."},
    {"product": "Jeans", "category": "Clothing", "description": "A pair of pants made from denim fabric, typically worn casually."},
    {"product": "Jacket", "category": "Clothing", "description": "A lightweight outerwear garment, typically with sleeves, worn to protect against weather."},
    {"product": "Sneakers", "category": "Clothing", "description": "Comfortable shoes designed for athletic use or casual wear."},
    {"product": "Sweater", "category": "Clothing", "description": "A knitted garment worn on the upper body, typically for warmth."},
    
    {"product": "Soccer Ball", "category": "Sports Equipment", "description": "A spherical ball used for the sport of soccer (football), usually made of leather or synthetic materials."},
    {"product": "Yoga Mat", "category": "Sports Equipment", "description": "A non-slip mat used for performing yoga or exercises."},
    {"product": "Tennis Racket", "category": "Sports Equipment", "description": "A sports implement used to hit a tennis ball, consisting of a frame and strings."},
    {"product": "Basketball", "category": "Sports Equipment", "description": "A round ball used for playing basketball, typically made of rubber or synthetic materials."},
    {"product": "Dumbbells", "category": "Sports Equipment", "description": "Handheld weights used in strength training and fitness exercises."},
    
    {"product": "Face Cream", "category": "Beauty Products", "description": "A moisturizing cream for the face that helps hydrate and protect the skin."},
    {"product": "Lipstick", "category": "Beauty Products", "description": "A cosmetic applied to the lips to add color and texture."},
    {"product": "Shampoo", "category": "Beauty Products", "description": "A liquid used to cleanse the hair and scalp."},
    {"product": "Nail Polish", "category": "Beauty Products", "description": "A lacquer applied to the nails to enhance appearance and provide color."},
    {"product": "Perfume", "category": "Beauty Products", "description": "A fragrant liquid used to enhance personal scent and fragrance."},
    
    {"product": "Lego Set", "category": "Toys & Games", "description": "A construction toy consisting of interlocking plastic bricks for building structures."},
    {"product": "Action Figure", "category": "Toys & Games", "description": "A movable figurine, often based on characters from movies or comics."},
    {"product": "Board Game", "category": "Toys & Games", "description": "A tabletop game that typically involves pieces, a board, and rules for play."},
    {"product": "Puzzle", "category": "Toys & Games", "description": "A game or problem designed to test skill and ingenuity by assembling pieces into a solution."},
    {"product": "Toy Car", "category": "Toys & Games", "description": "A small, miniature vehicle designed for play, often used by children."},
    
    {"product": "Fiction Book", "category": "Books", "description": "A literary work based on imagination, typically a novel or short story."},
    {"product": "Cookbook", "category": "Books", "description": "A collection of recipes and cooking tips for preparing various dishes."},
    {"product": "Self-Help Book", "category": "Books", "description": "A book focused on providing advice or techniques for personal improvement."},
    {"product": "Biography", "category": "Books", "description": "A written account of someone's life story, often from an autobiographical perspective."},
    {"product": "Textbook", "category": "Books", "description": "An educational book used for academic study, often used in schools or universities."},
    
    {"product": "Sofa", "category": "Furniture", "description": "A comfortable, padded seating piece for multiple people, often placed in living rooms."},
    {"product": "Dining Table", "category": "Furniture", "description": "A table designed for eating meals, often placed in a dining room."},
    {"product": "Office Chair", "category": "Furniture", "description": "A chair designed for use in an office setting, typically adjustable and ergonomic."},
    {"product": "Bookshelf", "category": "Furniture", "description": "A piece of furniture designed to hold and display books."},
    {"product": "Coffee Table", "category": "Furniture", "description": "A low table placed in front of seating areas, used for drinks, books, or decorations."},
    
    {"product": "Organic Apples", "category": "Groceries", "description": "Fresh, pesticide-free apples grown using organic farming practices."},
    {"product": "Whole Wheat Bread", "category": "Groceries", "description": "Bread made from whole wheat flour, offering more fiber and nutrients than white bread."},
    {"product": "Milk", "category": "Groceries", "description": "A dairy product commonly consumed as a drink or used in cooking."},
    {"product": "Eggs", "category": "Groceries", "description": "Eggs from hens, commonly used in cooking and baking."},
    {"product": "Rice", "category": "Groceries", "description": "A staple grain commonly used as a base for meals, especially in Asian and Mediterranean cuisines."},
    
    {"product": "Vitamins", "category": "Health & Wellness", "description": "Supplements containing essential nutrients to support overall health."},
    {"product": "Yoga Mat", "category": "Health & Wellness", "description": "A non-slip mat used for practicing yoga, stretching, and other fitness exercises."},
    {"product": "Protein Powder", "category": "Health & Wellness", "description": "A dietary supplement used to increase protein intake, commonly consumed by athletes and fitness enthusiasts."},
    {"product": "Massage Gun", "category": "Health & Wellness", "description": "A handheld device used for deep tissue massage to relieve muscle soreness and tension."},
    {"product": "Fitness Tracker", "category": "Health & Wellness", "description": "A wearable device that monitors physical activity, sleep, and other health metrics."}
]