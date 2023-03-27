from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import is_option_enabled, get_option_value
from .Locations import get_locations_by_region

def create_regions_and_locations(world: MultiWorld, player: int):
	locations = get_locations_by_region(world, player)

	regions = [
		create_region(world, player, "Menu", locations),
		create_region(world, player, "Surface [Main]", locations),
		create_region(world, player, "Surface [Ruin Path Upper]", locations),
		create_region(world, player, "Surface [Ruin Path Lower]", locations),
		create_region(world, player, "Gate of Guidance [Main]", locations),
		create_region(world, player, "Gate of Guidance [Door]", locations),
		create_region(world, player, "Gate of Illusion [Eden]", locations),
		create_region(world, player, "Gate of Illusion [Lower]", locations),
		create_region(world, player, "Gate of Illusion [Middle]", locations),
		create_region(world, player, "Gate of Illusion [Dracuet]", locations),
		create_region(world, player, "Gate of Illusion [Grail]", locations),
		create_region(world, player, "Gate of Illusion [Ruin]", locations),
		create_region(world, player, "Gate of Illusion [Upper]", locations),
		create_region(world, player, "Gate of Illusion [Pot Room]", locations),
		create_region(world, player, "Mausoleum of the Giants", locations),
		create_region(world, player, "Graveyard of the Giants [West]", locations),
		create_region(world, player, "Graveyard of the Giants [Grail]", locations),
		create_region(world, player, "Graveyard of the Giants [East]", locations),
		create_region(world, player, "Temple of the Sun [Top Entrance]", locations),
		create_region(world, player, "Temple of the Sun [Grail]", locations),
		create_region(world, player, "Temple of the Sun [Main]", locations),
		create_region(world, player, "Temple of the Sun [West]", locations),
		create_region(world, player, "Temple of the SUn [East]", locations),
		create_region(world, player, "Temple of the Sun [Sphinx]", locations),
		create_region(world, player, "Temple of Moonlight [Pyramid]", locations),
		create_region(world, player, "Temple of Moonlight [Upper]", locations),
		create_region(world, player, "Temple of Moonlight [Lower]", locations),
		create_region(world, player, "Temple of Moonlight [Eden]", locations),
		create_region(world, player, "Temple of Moonlight [Grail]", locations),
		create_region(world, player, "Temple of Moonlight [Grapple]", locations),
		create_region(world, player, "Temple of Moonlight [Map]", locations),
		create_region(world, player, "Temple of Moonlight [Southeast]", locations),
		create_region(world, player, "Spring in the Sky [Main]", locations),
		create_region(world, player, "Spring in the Sky [Upper]", locations),
		create_region(world, player, "Spring in the Sky [Waterfall]", locations),
		create_region(world, player, "Tower of the Goddess [Lower]", locations),
		create_region(world, player, "Tower of the Goddess [Lamp]", locations),
		create_region(world, player, "Tower of the Goddess [Grail]", locations),
		create_region(world, player, "Tower of the Goddess [Spaulder]", locations),
		create_region(world, player, "Tower of the Goddess [Shield Statue]", locations),
		create_region(world, player, "Inferno Cavern [Main]", locations),
		create_region(world, player, "Inferno Cavern [Viy]", locations),
		create_region(world, player, "Inferno Cavern [Lava]", locations),
		create_region(world, player, "Inferno Cavern [Spikes]", locations),
		create_region(world, player, "Tower of Ruin [Southeast]", locations),
		create_region(world, player, "Tower of Ruin [Southwest]", locations),
		create_region(world, player, "Tower of Ruin [Southwest Door]", locations),
		create_region(world, player, "Tower of Ruin [La-Mulanese]", locations),
		create_region(world, player, "Tower of Ruin [Illusion]", locations),
		create_region(world, player, "Tower of Ruin [Grail]", locations),
		create_region(world, player, "Tower of Ruin [Spirits]", locations),
		create_region(world, player, "Tower of Ruin [Medicine]", locations),
		create_region(world, player, "Tower of Ruin [Top]", locations),
		create_region(world, player, "Chamber of Extinction [Map]", locations),
		create_region(world, player, "Chamber of Extinction [Main]", locations),
		create_region(world, player, "Chamber of Extinction [Left Main]", locations),
		create_region(world, player, "Chamber of Extinction [Teleport]", locations),
		create_region(world, player, "Chamber of Extinction [Magatama Left]", locations),
		create_region(world, player, "Chamber of Extinction [Magatama Right]", locations),
		create_region(world, player, "Chamber of Extinction [Magatama]", locations),
		create_region(world, player, "Chamber of Extinction [Magatama Mantra]", locations),
		create_region(world, player, "Chamber of Extinction [Ankh Upper]", locations),
		create_region(world, player, "Chamber of Extinction [Ankh Lower]", locations),
		create_region(world, player, "Chamber of Birth [West Entrance]", locations),
		create_region(world, player, "Chamber of Birth [West]", locations),
		create_region(world, player, "Chamber of Birth [Grail]", locations),
		create_region(world, player, "Chamber of Birth [Skanda]", locations),
		create_region(world, player, "Chamber of Birth [Dance]", locations),
		create_region(world, player, "Chamber of Birth [Northeast]", locations),
		create_region(world, player, "Chamber of Birth [Southeast]", locations),
		create_region(world, player, "Twin Labyrinths [Loop]", locations),
		create_region(world, player, "Twin Labyrinths [Lower]", locations),
		create_region(world, player, "Twin Labyrinths [Poison 1]", locations),
		create_region(world, player, "Twin Labyrinths [Poison 2]", locations),
		create_region(world, player, "Twin Labyrinths [Upper Grail]", locations),
		create_region(world, player, "Twin Labyrinths [Jewel]", locations),
		create_region(world, player, "Twin Labyrinths [Katana]", locations),
		create_region(world, player, "Twin Labyrinths [Poseidon]", locations),
		create_region(world, player, "Twin Labyrinths [Upper Left]", locations),
		create_region(world, player, "Endless Corridor [1F]", locations),
		create_region(world, player, "Endless Corridor [2F]", locations),
		create_region(world, player, "Endless Corridor [3F Upper]", locations),
		create_region(world, player, "Endless Corridor [3F Lower]", locations),
		create_region(world, player, "Endless Corridor [4F]", locations),
		create_region(world, player, "Endless Corridor [5F]", locations),
		create_region(world, player, "Dimensional Corridor [Lower]", locations),
		create_region(world, player, "Dimensional Corridor [Grail]", locations),
		create_region(world, player, "Dimensional Corridor [Upper]", locations),
		create_region(world, player, "Shrine of the Mother [Main]", locations),
		create_region(world, player, "Shrine of the Mother [Lower]", locations),
		create_region(world, player, "Shrine of the Mother [Seal]", locations),
		create_region(world, player, "Shrine of the Mother [Map]", locations),
		create_region(world, player, "True Shrine of the Mother", locations),
		create_region(world, player, "Gate of Time [Mausoleum Lower]", locations),
		create_region(world, player, "Gate of Time [Mausoleum Upper]", locations),
		create_region(world, player, "Gate of Time [Guidance]", locations),
		create_region(world, player, "Gate of Time [Surface]", locations),
	]

	if get_option_value("ProvocativeBathingSuit") == 2 or is_option_enabled("RandomizeDracuetsShop"):
		regions.extend([
			create_region(world, player, "Hell Temple [Entrance]", locations),
			create_region(world, player, "Hell Temple [Shop]", locations),
			create_region(world, player, "Hell Temple [Dracuet]", locations),
		])

	world.regions += regions

def create_location(player: int, location_data: LocationData, region: Region):
	location = Location(player, location_data.name, location_data.code, region)
	location.access_rule = location_data.logic
	if location_data.is_event:
		location.event = True
		location.locked = True
	return location

def create_region(world: MultiWorld, player: int, region_name: str, locations_per_region: Dict[str, List[LocationData]]):
	region = Region(region_name, player, world)
	if region_name in locations_per_region:
		for location_data in locations_per_region[region_name]:
			location = create_location(player, location_data, region)
			region.locations.append(location)
	return region

