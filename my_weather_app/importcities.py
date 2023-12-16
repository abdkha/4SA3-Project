from pymongo import MongoClient

# Connect to MongoDB
# Initialize MongoDB
db_uri = "mongodb+srv://primoo357:#h#E67AP@mangodb.0xoamzf.mongodb.net/"
db_name = "my_weather_app_db"
client = MongoClient(db_uri)
db = client[db_name]
collection = db['cities']

# List of Canadian cities
canadian_cities = [
    "Alexandria", "Algonquin Park (Brent)", "Algonquin Park (Lake of Two Rivers)", "Alliston", "Apsley", "Armstrong",
    "Atikokan", "Attawapiskat", "Bancroft", "Barrie", "Barry's Bay", "Belleville", "Big Trout Lake", "Blind River",
    "Bracebridge", "Brampton", "Brantford", "Brockville", "Burk's Falls", "Burlington", "Caledon", "Cambridge",
    "Chapleau", "Chatham-Kent", "Cobourg", "Cochrane", "Collingwood", "Cornwall", "Deep River", "Dorion", "Dryden",
    "Dunchurch", "Dundalk", "Ear Falls", "Earlton", "Elliot Lake", "Fort Albany", "Fort Erie", "Fort Frances",
    "Fort Severn", "Gananoque", "Goderich", "Gogama", "Gore Bay", "Gravenhurst", "Greater Napanee", "Greater Sudbury",
    "Greenstone (Beardmore)", "Greenstone (Geraldton)", "Greenstone (Nakina)", "Guelph", "Gull Bay",
    "Haldimand County", "Haliburton", "Halton Hills", "Hamilton", "Hawkesbury", "Hearst", "Hornepayne", "Huntsville",
    "Ignace", "Kakabeka Falls", "Kaladar", "Kapuskasing", "Kawartha Lakes (Fenelon Falls)", "Kawartha Lakes (Lindsay)",
    "Kemptville", "Kenora", "Killarney", "Kincardine", "Kingston", "Kirkland Lake", "Kitchener-Waterloo",
    "Lake Superior (Provincial Park)", "Lambton Shores", "Lansdowne House", "Leamington", "Lincoln", "London",
    "Marathon", "Markham", "Midland", "Mine Centre", "Mississauga", "Montreal River Harbour", "Moosonee", "Morrisburg",
    "Mount Forest", "Muskoka", "New Tecumseth", "Newmarket", "Niagara Falls", "Nipigon", "Norfolk", "North Bay",
    "North Perth", "Oakville", "Ogoki", "Orangeville", "Orillia", "Oshawa", "Ottawa (Kanata - Orléans)",
    "Ottawa (Richmond - Metcalfe)", "Owen Sound", "Oxtongue Lake", "Parry Sound", "Peawanuck", "Pembroke", "Petawawa",
    "Peterborough", "Pickering", "Pickle Lake", "Pikangikum", "Port Carling", "Port Colborne", "Port Elgin",
    "Port Perry", "Prince Edward (Picton)", "Quinte West", "Red Lake", "Renfrew", "Richmond Hill", "Rodney",
    "Rondeau (Provincial Park)", "Sachigo Lake", "Sandy Lake", "Sarnia", "Saugeen Shores", "Sault Ste. Marie",
    "Savant Lake", "Sharbot Lake", "Shelburne", "Simcoe", "Sioux Lookout", "Sioux Narrows", "Smiths Falls",
    "South Bruce Peninsula", "St. Catharines", "St. Thomas", "Stirling", "Stratford", "Strathroy", "Sudbury (Greater)",
    "Sydenham", "Temiskaming Shores", "Terrace Bay", "Thunder Bay", "Tillsonburg", "Timmins", "Tobermory", "Toronto",
    "Toronto Island", "Trenton", "Upsala", "Vaughan", "Vineland", "Walkerton", "Wawa", "Webequie", "Welland",
    "West Nipissing", "Westport", "Whitby", "White River", "Wiarton", "Winchester", "Windsor", "Wingham", "Woodstock",
    "Wunnummin Lake"
]

# Insert each city into MongoDB
for city in canadian_cities:
    city_data = {'name': f'{city}, CA'}
    collection.insert_one(city_data)

print("Data insertion complete.")
