"""Home page content, taken from the existing site plus the real Google profile."""

TRUST = [
    ("4", "States Served"),
    ("100+", "Communities Served"),
    ("100%", "Background Checked"),
    ("100%", "Satisfaction Guarantee"),
]

# Three services get the editorial treatment; the rest are a dense list.
FEATURE_SERVICES = [
    ("/services/recurring-cleaning/", "Standard & Recurring Cleaning",
     "Keep your home consistently clean",
     "Weekly, biweekly, or monthly premium home cleaning. Consistent teams who learn your "
     "home's unique needs, working from a detailed checklist customised to your space so the "
     "standard never drifts from one visit to the next.",
     "/images/source/05-carousel-primary-bedroom.webp",
     "/images/source/04-carousel-primary-bedroom.jpg",
     "Primary bedroom with a made bed and crisp linen bedding after a Salt & Slate recurring house cleaning",
     1024, 1024),
    ("/services/deep-cleaning/", "Deep Cleaning",
     "Catch up on months of buildup",
     "Detailed home cleaning with baseboards, cabinet exteriors, doors, windowsills and "
     "shower-grout scrubbing. Refrigerator, oven and dishwasher interiors, and interior window "
     "glass and tracks, are paid add-ons.",
     "/images/source/03-carousel-kitchen.webp",
     "/images/source/02-carousel-kitchen.jpg",
     "Kitchen with a marble waterfall island and brass pendants after a Salt & Slate deep cleaning",
     1024, 1024),
    ("/services/post-construction-cleaning/", "Post-Construction Cleaning",
     "Finish a build or remodel",
     "Detailed final cleaning after construction or renovation: loose construction dust, "
     "cabinet interiors, trim, window tracks, glass doors and floors, once the trades have "
     "finished and cleared the space.",
     "/images/source/34-img-4757-1764112803330.webp",
     "/images/source/33-img-4757-1764112803330.jpg",
     "Newly tiled shower left spotless after a Salt & Slate post-construction cleaning",
     1125, 1500),
]

LIST_SERVICES = [
    ("/services/move-in-cleaning/", "Move-In Cleaning",
     "Prepare your next home before unpacking. Our checklist covers empty cabinets, drawers and "
     "closets, refrigerator and oven interiors, kitchens, bathrooms and floors."),
    ("/services/move-out-cleaning/", "Move-Out Cleaning",
     "Lease-end and pre-sale cleaning with empty cabinet, drawer and closet interiors, "
     "refrigerator and oven interiors, kitchens, bathrooms and floors."),
    ("/services/vacation-home-cleaning/", "Vacation Home Cleaning",
     "Cleaning before your next stay or between visits to your mountain, desert or lake home, "
     "with access arranged while you are away."),
    ("/services/airbnb-cleaning/", "Airbnb & Rental Cleaning",
     "Turnover cleaning for your guest schedule, including fridge interior cleaning, fresh linen "
     "changes and bed making."),
    ("/services/estate-cleaning/", "Estate Cleaning",
     "Detailed cleaning for larger residences using our deep-clean checklist and products suited "
     "to your home's materials and finishes."),
    ("/services/specialty-cleaning/", "Specialty Cleaning",
     "Expert care for natural stone, marble, granite, hardwood, wine cellars, home gyms, radiant "
     "heated floors, and other premium surfaces."),
]

COMMERCIAL_CARDS = [
    ("/commercial/office-cleaning/", "Office Cleaning",
     "Desks, conference rooms, break areas and restrooms — scheduled around your operating hours."),
    ("/commercial/medical-office-cleaning/", "Medical Office Cleaning",
     "Cleaning for medical offices and outpatient practices, scheduled outside patient hours."),
    ("/commercial/dental-office-cleaning/", "Dental Office Cleaning",
     "Cleaning for dental practices, scheduled around patient appointments."),
    ("/commercial/law-firm-cleaning/", "Law Firm Cleaning",
     "After-hours cleaning for legal offices. Discreet service that respects sensitive document areas."),
    ("/commercial/gym-cleaning/", "Gym & Fitness Cleaning",
     "Cleaning for gyms, fitness centers and 24/7-access facilities."),
    ("/commercial/restaurant-cleaning/", "Restaurant Cleaning",
     "After-hours cleaning for restaurants and kitchens, scheduled around your service hours."),
    ("/commercial/warehouse-cleaning/", "Warehouse Cleaning",
     "Cleaning for warehouses, distribution centers and fulfillment facilities."),
    ("/commercial/retail-cleaning/", "Retail Cleaning",
     "Cleaning for retail stores and showrooms."),
]

# Verticals the business serves that do not have their own page here.
COMMERCIAL_MORE = [
    "Church Cleaning", "Event Venue Cleaning", "Property Management Cleaning",
    "Daycare Cleaning", "Salon & Spa Cleaning", "Coworking Space Cleaning",
    "Commercial Construction Cleanup",
]

WHY = [
    ("Same Standard Every Visit",
     "A detailed room-by-room checklist on every cleaning so the standard, the coverage, and the "
     "satisfaction guarantee stay the same from visit to visit."),
    ("Licensed, Background-Checked & Insured",
     "Salt & Slate is a licensed and fully insured cleaning company. Every cleaner passes a "
     "comprehensive background check before stepping foot in your home."),
    ("Decades of Experience",
     "Our team members bring decades of professional cleaning experience to every home and "
     "business we serve."),
    ("24-Hour Satisfaction Guarantee",
     "If anything falls short, we return to make it right at no additional charge. No fine print."),
]

BEFORE_AFTER = [
    ("luxury-kitchen", "Luxury kitchen clean", "Park City estate kitchen",
     "/images/source/16-img-2487-1754950975730.webp", "/images/source/15-img-2487-1754950975730.jpg",
     "Luxury kitchen before a Salt & Slate clean",
     "/images/source/18-img-2519-1754950975730.webp", "/images/source/17-img-2519-1754950975730.jpg",
     "The same luxury kitchen spotless after a Salt & Slate clean", 1500, 1125),
    ("kitchen-deep", "Kitchen deep clean", "Counters, backsplash and appliance exteriors",
     "/images/source/20-img-2489-1754950987754.webp", "/images/source/19-img-2489-1754950987754.jpg",
     "Kitchen with built-up grime before a Salt & Slate deep clean",
     "/images/source/22-img-2521-1754950987754.webp", "/images/source/21-img-2521-1754950987754.jpg",
     "The same kitchen fully detailed after a Salt & Slate deep clean", 1500, 1125),
    ("fridge-deep", "Refrigerator deep clean", "Interior shelving and drawers",
     "/images/source/24-img-2579-1754951015393.webp", "/images/source/23-img-2579-1754951015393.jpg",
     "Refrigerator interior with spills and residue before a Salt & Slate deep clean",
     "/images/source/26-img-2575-1754951015393.webp", "/images/source/25-img-2575-1754951015393.jpg",
     "The same refrigerator interior cleaned and reset by Salt & Slate", 768, 1024),
    ("fridge-refresh", "Refrigerator refresh", "Door shelves and seals",
     "/images/source/28-img-2578-1754951015393.webp", "/images/source/27-img-2578-1754951015393.jpg",
     "Refrigerator door shelves soiled before a Salt & Slate cleaning",
     "/images/source/30-img-2572-1754951015393.webp", "/images/source/29-img-2572-1754951015393.jpg",
     "The same refrigerator door shelves wiped clean by Salt & Slate", 768, 1024),
    ("post-construction", "Post-construction clean", "Construction dust removal",
     "/images/source/32-img-4761-1764112803329.webp", "/images/source/31-img-4761-1764112803329.jpg",
     "Newly tiled shower with construction dust and debris before a Salt & Slate clean",
     "/images/source/34-img-4757-1764112803330.webp", "/images/source/33-img-4757-1764112803330.jpg",
     "The same tiled shower left spotless after a Salt & Slate post-construction clean", 1125, 1500),
    ("sink-deep", "Sink deep clean", "Hard-water and mineral buildup",
     "/images/source/36-img-4783-1764259564770.webp", "/images/source/35-img-4783-1764259564770.jpg",
     "Kitchen sink with hard-water mineral buildup before a Salt & Slate deep clean",
     "/images/source/38-img-4784-1764259564769.webp", "/images/source/37-img-4784-1764259564769.jpg",
     "The same kitchen sink scrubbed and restored by Salt & Slate", 1280, 960),
]

SHOWCASE = [
    ("/images/source/13-luxuryhom2-1764622932087.webp",
     "Luxury home marble floors and grand entryway in Utah cleaned by Salt & Slate",
     "Luxury Homes", 683, 1024),
    ("/images/source/14-luxuryhome3-1764622946784.webp",
     "Luxury home living room with mountain views in Utah cleaned by Salt & Slate",
     "Homes Over 10,000 Sq Ft", 683, 1024),
]

RECOGNIZED = [
    ("The Watch Party",
     "Six weeks of recurring service at Salt Lake City's Civic Center event hub during the "
     "inaugural Watch Party event series, February through March 2026."),
    ("Salt Lake City Mayor's Office",
     "Commissioned by the Salt Lake City Mayor's Office as recurring commercial cleaning partner "
     "for a high-profile civic event series in downtown Salt Lake City."),
    ("Major Studio Productions",
     "Recurring residential service for Park City and Deer Valley luxury estates — including "
     "private homes used as on-location sets by HBO and other major film and television studios."),
]

RECOGNIZED_NOTE = ("References describe engagements where the listed entity directly contracted "
                   "Salt & Slate. No endorsement or affiliation is implied beyond the scope described.")

# Quoted verbatim from the business's Google Business Profile.
FEATURED_REVIEWS = [
    ("I hired Salt & Slate Cleaning Company for a deep clean and they exceeded all of my "
     "expectations. Marie & Dorothea were absolutely fantastic and diligent in their work. They "
     "arrived right on time, were incredibly professional and worked hard from start to finish.",
     "M G.", "5 stars on Google"),
    ("We loved having them come and do a thorough deep cleaning across our home. We now have the "
     "monthly service and our home looks clean. They’ve been professional and kind.",
     "Kristen", "5 stars on Google"),
    ("Best service from a cleaning company. Reliable and fast. I trust them with my cleaning "
     "needs. Will hire again.",
     "Mari K.", "5 stars on Google"),
]

# Further verbatim Google reviews carried over from the existing site.
MORE_REVIEWS = [
    ("I am happy with my experience! Scheduling was easy and flexible. The deep cleaning was very "
     "thorough and my house looks great!", "Jayme Trevino", "5 months ago · on Google"),
    ("Thank you so much for a wonderful job cleaning. Ana was so thorough and communicative with "
     "how she cleaned. The house smells amazing!", "Hannah Montiel", "6 months ago · on Google"),
    ("Tammy was absolutely lovely. Communicative and focused on all the (very problematic) areas "
     "we discussed. Even gave tips on keeping up with some of the tougher issues with hard water. "
     "I’m absolutely booking again and grateful.", "Sarah Speaks", "7 months ago · on Google"),
    ("Both cleaners were fantastic! I will definitely be using this service again. They were "
     "efficient and paid attention to detail. They were very respectful of my home and belongings.",
     "Kelsey Blackstone", "7 months ago · on Google"),
    ("We hired them to do a post construction clean for our new construction 5,000 square foot "
     "house in Holladay. It was a multi day project and we could not be happier. The cleaners were "
     "professional, on time and took a lot of pride in their work.",
     "Lacey Fontaneau", "9 months ago · on Google"),
    ("WOW. Carmen and Michelle are absolute magicians. Professional, thorough, communicative, and "
     "polite. I keep catching all the little things they cleaned and realizing how much better it "
     "all looks. Highly recommend!", "Audrey Vander Most", "9 months ago · on Google"),
    ("They came in after a mold restoration and shower renovation project, my home was SO dusty. I "
     "just walked in and am super impressed! The place looks completely different and it smells "
     "great. I’m grateful I chose them to do my post construction cleaning.",
     "Alexis Wien", "2 months ago · on Google"),
    ("I own a high end Airbnb in Park City and we were recommended Salt and Slate Cleaning. Marta "
     "and her team are very thorough. They even left local Utah honey, chocolates and a candle "
     "after our first clean. This company understands customer service.",
     "Mark Conroy", "a year ago · on Google"),
    ("We interviewed a few different companies for a post construction clean of our Westlake home "
     "and ultimately chose salt and slate cleaning company due to fabulous reviews and "
     "before/after photos. They did a great job. They now service our home for bi-weekly cleans.",
     "Neal Bermeyer", "3 weeks ago · on Google"),
]

AREAS = [
    ("/locations/utah/", "Utah",
     "Park City · Coalville · Kamas · Francis · Oakley · Henefer · Midway · Heber City",
     "+ 42 more cities"),
    ("/locations/arizona/", "Arizona",
     "Scottsdale · Paradise Valley · Fountain Hills · Phoenix · Cave Creek · Gilbert · Chandler · Carefree",
     "+ 9 more cities"),
    ("/locations/nevada/", "Nevada",
     "Henderson · Las Vegas · Summerlin · Boulder City · North Las Vegas",
     ""),
    ("/locations/texas/", "Texas",
     "Dallas · Highland Park · University Park · Coppell · Irving · Addison · Richardson · Frisco",
     "+ 26 more cities"),
]

STEPS = [
    ("01", "Get Your Quote",
     "Tell us about your property. We'll send you flat-rate pricing so you know the full cost "
     "upfront — no surprises."),
    ("02", "Cleaner Standards",
     "Every Salt & Slate cleaner is licensed, background-checked, and fully insured. We brief them "
     "on your home — which surfaces need special care, where you want extra attention, what to skip."),
    ("03", "Enjoy the Results",
     "The same detailed checklist on every visit, backed by our 24-hour satisfaction guarantee. If "
     "anything's not right, we come back at no charge."),
]
