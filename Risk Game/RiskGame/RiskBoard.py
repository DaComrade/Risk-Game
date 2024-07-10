class Territory:
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.armies = 0
        self.adjacent_territories = []

    def add_adjacent_territory(self, territory):
        self.adjacent_territories.append(territory)


class Continent:
    def __init__(self, name):
        self.name = name
        self.territories = []

    def add_territory(self, territory):
        self.territories.append(territory)


class Board:
    def __init__(self):
        self.territories = {}
        self.continents = {}
        self.current_phase = 'placing_armies'


    def add_continent(self, continent):
        self.continents[continent.name] = continent

    def add_territory(self, territory, continent_name):
        self.territories[territory.name] = territory
        self.continents[continent_name].add_territory(territory)

    def connect_territories(self, territory1, territory2):
        self.territories[territory1].add_adjacent_territory(self.territories[territory2])
        self.territories[territory2].add_adjacent_territory(self.territories[territory1])

    def set_current_phase(self, phase):
        """Set the current phase of the game."""
        self.current_phase = phase

    # Example method to initialize the board
    def initialize_board(self):
        # Add continents
        asia = Continent("Asia")
        australia = Continent("Australia")
        europe = Continent("Europe")
        africa = Continent("Africa")
        north_america = Continent("North America")
        south_america = Continent("South America")
        self.add_continent(asia)
        self.add_continent(australia)
        self.add_continent(europe)
        self.add_continent(africa)
        self.add_continent(north_america)
        self.add_continent(south_america)

        # Add territories

        #Asia

        afghanistan = Territory("Afghanistan")
        china = Territory("China")
        india = Territory("India")
        irkutsk = Territory('Irkutsk')
        japan = Territory('Japan')
        kamchatka = Territory('Kamchatka')
        middle_east = Territory('Middle East')
        mongolia = Territory('Mongolia')
        siam = Territory('Siam')
        siberia = Territory('Siberia')
        ural = Territory('Ural')
        yakutsk = Territory('Yakutsk')
        self.add_territory(afghanistan, "Asia")
        self.add_territory(china, "Asia")
        self.add_territory(india, "Asia")
        self.add_territory(irkutsk, "Asia")
        self.add_territory(japan, "Asia")
        self.add_territory(kamchatka, "Asia")
        self.add_territory(middle_east, "Asia")
        self.add_territory(mongolia, "Asia")
        self.add_territory(siam, "Asia")
        self.add_territory(siberia, "Asia")
        self.add_territory(ural, "Asia")
        self.add_territory(yakutsk, "Asia")

        #Australia

        eastern_australia = Territory('Eastern Australia')
        indonesia = Territory('Indonesia')
        new_guinea = Territory('New Guinea')
        western_australia = Territory('Western Australia')
        self.add_territory(eastern_australia, "Australia")
        self.add_territory(indonesia, "Australia")
        self.add_territory(new_guinea, "Australia")
        self.add_territory(western_australia, "Australia")

        #Europe

        great_britain = Territory('Great Britain')
        iceland = Territory('Iceland')
        northern_europe = Territory('Northern Europe')
        scandinavia = Territory('Scandinavia')
        southern_europe = Territory('Southern Europe')
        ukraine = Territory('Ukraine')
        western_europe = Territory('Western Europe')
        self.add_territory(great_britain, "Europe")
        self.add_territory(iceland, "Europe")
        self.add_territory(northern_europe, "Europe")
        self.add_territory(scandinavia, "Europe")
        self.add_territory(southern_europe, "Europe")
        self.add_territory(ukraine, "Europe")
        self.add_territory(western_europe, "Europe")

        #Africa

        congo = Territory('Congo')
        east_africa = Territory('East Africa')
        egypt = Territory('Egypt')
        madagascar = Territory('Madagascar')
        north_africa = Territory('North Africa')
        south_africa = Territory('South Africa')
        self.add_territory(congo, "Africa")
        self.add_territory(east_africa, "Africa")
        self.add_territory(egypt, "Africa")
        self.add_territory(madagascar, "Africa")
        self.add_territory(north_africa, "Africa")
        self.add_territory(south_africa, "Africa")

        #North America

        alaska = Territory('Alaska')
        alberta = Territory('Alberta')
        central_america = Territory('Central America')
        eastern_united_states = Territory('Eastern United States')
        greenland = Territory('Greenland')
        northwest_territory = Territory('Northwest Territory')
        ontario = Territory('Ontario')
        quebec = Territory('Quebec')
        western_united_states = Territory('Western United States')
        self.add_territory(alaska, "North America")
        self.add_territory(alberta, "North America")
        self.add_territory(central_america, "North America")
        self.add_territory(eastern_united_states, "North America")
        self.add_territory(greenland, "North America")
        self.add_territory(northwest_territory, "North America")
        self.add_territory(ontario, "North America")
        self.add_territory(quebec, "North America")
        self.add_territory(western_united_states, "North America")

        #South America

        argentina = Territory('Argentina')
        brazil = Territory('Brazil')
        peru = Territory('Peru')
        venezuela = Territory('Venezuela')
        self.add_territory(argentina, "South America")
        self.add_territory(brazil, "South America")
        self.add_territory(peru, "South America")
        self.add_territory(venezuela, "South America")


        # Connect territories

        #Asia

        self.connect_territories('Afghanistan','Ukraine')
        self.connect_territories('Afghanistan', 'Ural')
        self.connect_territories('Afghanistan', 'China')
        self.connect_territories('Afghanistan', 'India')
        self.connect_territories('Afghanistan', 'Middle East')
        self.connect_territories("China", "India")
        self.connect_territories("China", "Ural")
        self.connect_territories("China", "Siberia")
        self.connect_territories("China", "Mongolia")
        self.connect_territories("China", "Siam")
        self.connect_territories("India", "Middle East")
        self.connect_territories("India", "Siam")
        self.connect_territories("Irkutsk", "Siberia")
        self.connect_territories("Irkutsk", "Yakutsk")
        self.connect_territories("Irkutsk", "Kamchatka")
        self.connect_territories("Irkutsk", "Mongolia")
        self.connect_territories("Japan", "Kamchatka")
        self.connect_territories("Japan", "Mongolia")
        self.connect_territories("Kamchatka", "Alaska")
        self.connect_territories("Kamchatka", "Yakutsk")
        self.connect_territories("Kamchatka", "Mongolia")
        self.connect_territories("Middle East", "Egypt")
        self.connect_territories("Middle East", "Southern Europe")
        self.connect_territories("Middle East", "Ukraine")
        self.connect_territories("Middle East", "Egypt")
        self.connect_territories("Mongolia", "Siberia")
        self.connect_territories("Siam", "Indonesia")
        self.connect_territories("Siberia", "Ural")
        self.connect_territories("Siberia", "Yakutsk")
        self.connect_territories("Ural", "Ukraine")

        # Australia

        self.connect_territories("Eastern Australia", "New Guinea")
        self.connect_territories("Eastern Australia", "Western Australia")
        self.connect_territories("New Guinea", "Indonesia")
        self.connect_territories("New Guinea", "Western Australia")
        self.connect_territories("Indonesia", "Western Australia")

        #Europe

        self.connect_territories("Great Britain", "Iceland")
        self.connect_territories("Great Britain", "Scandinavia")
        self.connect_territories("Great Britain", "Northern Europe")
        self.connect_territories("Great Britain", "Western Europe")
        self.connect_territories("Iceland", "Greenland")
        self.connect_territories("Iceland", "Scandinavia")
        self.connect_territories("Northern Europe", "Scandinavia")
        self.connect_territories("Northern Europe", "Ukraine")
        self.connect_territories("Northern Europe", "Southern Europe")
        self.connect_territories("Northern Europe", "Western Europe")
        self.connect_territories("Scandinavia", "Ukraine")
        self.connect_territories("Southern Europe", "Western Europe")
        self.connect_territories("Southern Europe", "Ukraine")
        self.connect_territories("Southern Europe", "Egypt")
        self.connect_territories("Southern Europe", "North Africa")
        self.connect_territories("Western Europe", "North Africa")

        #Africa

        self.connect_territories("Congo", "North Africa")
        self.connect_territories("Congo", "East Africa")
        self.connect_territories("Congo", "South Africa")
        self.connect_territories("East Africa", "North Africa")
        self.connect_territories("East Africa", "Egypt")
        self.connect_territories("East Africa", "Madagascar")
        self.connect_territories("East Africa", "South Africa")
        self.connect_territories("Egypt", "North Africa")
        self.connect_territories("Madagascar", "South Africa")
        self.connect_territories("North Africa", "Brazil")

        #North America

        self.connect_territories("Alaska", "Alberta")
        self.connect_territories("Alaska", "Northwest Territory")
        self.connect_territories("Alberta", "Northwest Territory")
        self.connect_territories("Alberta", "Ontario")
        self.connect_territories("Alberta", "Western United States")
        self.connect_territories("Central America", "Venezuela")
        self.connect_territories("Central America", "Eastern United States")
        self.connect_territories("Central America", "Western United States")
        self.connect_territories("Eastern United States", "Western United States")
        self.connect_territories("Eastern United States", "Ontario")
        self.connect_territories("Eastern United States", "Quebec")
        self.connect_territories("Greenland", "Northwest Territory")
        self.connect_territories("Greenland", "Ontario")
        self.connect_territories("Greenland", "Quebec")
        self.connect_territories("Greenland", "Northwest Territory")
        self.connect_territories("Northwest Territory", "Ontario")
        self.connect_territories("Ontario", "Quebec")
        self.connect_territories("Ontario", "Western United States")

        #South America

        self.connect_territories("Argentina", "Peru")
        self.connect_territories("Argentina", "Brazil")
        self.connect_territories("Brazil", "Peru")
        self.connect_territories("Brazil", "Venezuela")
        self.connect_territories("Peru", "Venezuela")

        print(f"Board initialized with territories: {list(self.territories.keys())}")
    def get_neighbors(self, territory_name):
            # Debugging print statement
            print(f"Available territories in board: {list(self.territories.keys())}")
            print(f"Requested territory: {territory_name}")

            if territory_name not in self.territories:
                raise KeyError(f"Territory '{territory_name}' not found in RiskBoard territories.")

            territory = self.territories[territory_name]
            return [neighbor.name for neighbor in territory.adjacent_territories]







