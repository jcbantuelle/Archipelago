from typing import Dict, List, Set, Optional, TextIO, Union
from BaseClasses import Item, MultiWorld, Tutorial, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from .Options import lamulana_options, starting_location_names, starting_weapon_names, is_option_enabled, get_option_value
from .WorldState import LaMulanaWorldState
from .NPCs import get_npc_checks, get_npc_entrance_room_names, get_shop_location_names
from .Items import item_table, shop_inventory_codes, get_items_by_category
from .Locations import get_locations_by_region
from .Regions import create_regions_and_locations

client_version = 1

class LaMulanaWebWorld(WebWorld):
	tutorial_en = Tutorial(
		"Multiworld Setup Tutorial",
		"A guide for how to set up La-Mulana multiworld",
		"English",
		"setup_en.md",
		"setup/en",
		["Author's-name"]
	)
	tutorials = [tutorial_en]

class LaMulanaWorld(World):
	"""
	Challenge the ruins in the 2012 remake of La-Mulana, a puzzle platformer that focuses
	on exploration and combat as much as it does on solving the puzzles and mysteries of the ruins.
	"""
	game = "La-Mulana"
	option_definitions = lamulana_options
	web = LaMulanaWebWorld()
	required_client_version = (0, 4, 0) #Placeholder version number

	worldstate: LaMulanaWorldState
	
	item_name_to_id = {name: data.code for name, data in item_table.items()}
	location_name_to_id = {location.name: location.code for locations in get_locations_by_region(None, None, None).values() for location in locations}
	location_name_to_id.update({location.name: location.code for locations in get_npc_checks(None, None).values() for location in locations})
	item_name_groups = get_items_by_category()

	def __init__(self, world : MultiWorld, player: int):
		super().__init__(world, player)
		self.worldstate = LaMulanaWorldState(self.multiworld, self.player)

	def generate_early(self) -> None:
		#Do stuff that can still modify settings
		if self.is_option_enabled('StartWithHolyGrail'):
			self.multiworld.start_inventory[self.player].value['Holy Grail'] = 1
		if self.is_option_enabled('StartWithMirai'):
			self.multiworld.start_inventory[self.player].value['mirai.exe'] = 1
		if self.is_option_enabled('StartWithHermesBoots'):
			self.multiworld.start_inventory[self.player].value["Hermes' Boots"] = 1
		if self.is_option_enabled('StartWithTextTrax'):
			self.multiworld.start_inventory[self.player].value['bunemon.exe'] = 1
		"""	if self.multiworld.start_inventory[self.player].value.pop("Holy Grail", 0) > 0:
			self.multiworld.StartWithHolyGrail[self.player].value = self.multiworld.StartWithHolyGrail[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("mirai.exe", 0) > 0:
			self.multiworld.StartWithMirai[self.player].value = self.multiworld.StartWithMirai[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Hermes' Boots", 0) > 0:
			self.multiworld.StartWithHermesBoots[self.player].value = self.multiworld.StartWithHermesBoots[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("bunemon.exe", 0) > 0:
			self.multiworld.StartWithTextTrax[self.player].value = self.multiworld.StartWithTextTrax[self.player].option_true
"""
		starting_weapon = get_option_value(self.multiworld, self.player, "StartingWeapon")
		self.multiworld.start_inventory[self.player].value[starting_weapon_names[starting_weapon]] = 1

		starting_location = get_option_value(self.multiworld, self.player, "StartingLocation")
		if starting_location_names[starting_location] == 'goddess':
			self.multiworld.start_inventory[self.player].value['Plane Model'] = 1
		elif starting_location_names[starting_location] == 'twin (front)':
			self.multiworld.start_inventory[self.player].value['Twin Statue'] = 1
		elif starting_location_names[starting_location] == 'extinction':
			if is_option_enabled(self.multiworld, self.player, "RequireFlareGun") and starting_weapon_names[starting_weapon] != 'Flare Gun':
				self.multiworld.start_inventory[self.player].value['Flare Gun'] = 1


	def create_regions(self) -> None:
		create_regions_and_locations(self.multiworld, self.player, self.worldstate)

	def create_items(self) -> None:
		self.assign_event_items()
		shop_items = self.generate_shop_items()
		self.multiworld.itempool += shop_items
		self.multiworld.itempool += self.generate_item_pool(len(shop_items))
		print('Currently', len(self.multiworld.get_unfilled_locations()), 'unfilled locations in the pool')

	def set_rules(self) -> None:
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all({'Mother Defeated', 'NPC: Mulbruk'}, self.player)

	def extend_hint_information(self, hint_data: Dict[int, Dict[int,str]]):
		if self.worldstate.cursed_chests:
			for cursed_chest_name in self.worldstate.cursed_chests:
				location = self.multiworld.get_location(cursed_chest_name, self.player)
				setattr(location, '_hint_text', cursed_chest_name + ' (Cursed)')
		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			npc_hint_info = {}
			room_names = get_npc_entrance_room_names()
			npc_checks = get_npc_checks(self.multiworld, self.player)
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name, locationdata_list in npc_checks.items():
				if npc_name in reverse_map:
					door_name = reverse_map[npc_name]
					for locationdata in locationdata_list:
						if not locationdata.is_event:
							npc_hint_info[locationdata.code] = room_names[door_name]
			hint_data[self.player] = npc_hint_info

	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		spoiler_handle.write(f'Cursed Chests:		{self.worldstate.cursed_chests}\n')
		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			spoiler_handle.write(f'NPC Randomizer:\n')
			room_names = get_npc_entrance_room_names()
			space_count = lambda name: ' ' * (25 - len(name))  
			for npc_door, npc_name in self.worldstate.npc_mapping.items():
				spoiler_handle.write(f'	- {npc_name}:{space_count(npc_name)}{room_names[npc_door]}\n')
		#Maybe also transition info? It's gonna be a lot

	def fill_slot_data(self) -> Dict[str, object]:
		slot_data : Dict[str, object] = {}
		for option_name in lamulana_options:
			slot_data[option_name] = self.get_option_value(option_name)
		return slot_data

	def assign_event_items(self):
		for location in self.multiworld.get_locations(self.player):
			if location.address is None:
				item = Item(location.name, ItemClassification.progression, None, self.player)
				location.place_locked_item(item)

	def generate_shop_items(self):
		shop_item_pool: List[Item] = []
		starting_weapon = starting_weapon_names[self.get_option_value('StartingWeapon')]

		if starting_weapon in {'Shuriken', 'Rolling Shuriken', 'Flare Gun', 'Earth Spear', 'Bomb', 'Chakram', 'Caltrops', 'Pistol'}:
			required_subweapon_ammo = starting_weapon + ' Ammo'
		else:
			required_subweapon_ammo = None

		shop_locations: Set[str] = get_shop_location_names(self.multiworld, self.player)

		#Little Brother needs weights
		self.place_locked_item('Yiegah Kungfu Shop Item 1', '5 Weights')
		shop_locations.remove('Yiegah Kungfu Shop Item 1')

		print('StartingLocation', self.get_option_value('StartingLocation'), ' -- name: ', starting_location_names[self.get_option_value('StartingLocation')])
		if starting_location_names[self.get_option_value('StartingLocation')] == 'surface':
			shop_locations.remove('Starting Shop Item 1')
			shop_locations.remove('Starting Shop Item 2')
			shop_locations.remove('Starting Shop Item 3')
			if not self.is_option_enabled('RandomizeNPCs'):
				self.place_locked_item('Sidro Shop Item 1', '5 Weights')
				shop_locations.remove('Sidro Shop Item 1')
				if required_subweapon_ammo:
					self.place_locked_item('Sidro Shop Item 2', required_subweapon_ammo)
					shop_locations.remove('Sidro Shop Item 2')
		else:
			self.place_locked_item('Starting Shop Item 1', '5 Weights')
			shop_locations.remove('Starting Shop Item 1')
			if required_subweapon_ammo:
				self.place_locked_item('Starting Shop Item 2', required_subweapon_ammo)
				shop_locations.remove('Starting Shop Item 2')

		slot_amount = len(shop_locations) - self.get_option_value('ShopDensity')

		local_shop_inventory_list = self.multiworld.random.sample(list(shop_locations), slot_amount)
		print(slot_amount, 'Shop slots selected for ammo/weights:', local_shop_inventory_list)
		#for location_name in local_shop_inventory_list:
		for location in self.multiworld.get_unfilled_locations(self.player):
			if location.address:
				if location.name in local_shop_inventory_list:
					add_item_rule(location, lambda item: item.player == self.player and item.code in shop_inventory_codes)
				else:
					add_item_rule(location, lambda item: item and not item.code in shop_inventory_codes)
					if location.name == 'Twin Labyrinths Escape Coin Chest':
						#local progression/chains would be a problem for the escape coin chest
						add_item_rule(location, lambda item: item.classification != ItemClassification.progression or item.player != self.player)

		#Guaranteed minimum amounts per ammo type and weights
		ammo_types = ['Shuriken Ammo', 'Rolling Shuriken Ammo', 'Earth Spear Ammo', 'Flare Gun Ammo', 'Bomb Ammo', 'Chakram Ammo', 'Caltrops Ammo', 'Pistol Ammo']
		for ammo_name in ammo_types:
			shop_item_pool.append(self.create_item(ammo_name))
		for _ in range(4):
			shop_item_pool.append(self.create_item('5 Weights'))
		if slot_amount >= 20:
			#2 guaranteed slots per subweapon ammo if enough shop slots
			for ammo_name in ammo_types:
				shop_item_pool.append(self.create_item(ammo_name))

		for shop_item_name in self.multiworld.random.choices(ammo_types + ['5 Weights'], k=slot_amount - len(shop_item_pool)):
			shop_item_pool.append(self.create_item(shop_item_name))

		print('final shop item pool', len(shop_item_pool), ':', shop_item_pool)
		return shop_item_pool

	def generate_item_pool(self, shop_item_count: int) -> List[Item]:
		item_pool: List[Item] = []

		for name, data in item_table.items():
			for _ in range(data.count - (self.multiworld.start_inventory[self.player].value[name] if name in self.multiworld.start_inventory[self.player].value else 0)):
				item = self.create_item(name)
				item_pool.append(item)

		if self.is_option_enabled('AlternateMotherAnkh'):
			item_pool.append(self.create_item('Ankh Jewel'))

		filler_pool_size = len(self.multiworld.get_unfilled_locations(self.player)) - shop_item_count - len(item_pool)

		print(len(self.multiworld.get_unfilled_locations(self.player)), 'unfilled locations - ', shop_item_count, 'items already in pool (shops) - ', len(item_pool), 'items currently being added - ', filler_pool_size, 'current filler items')
		for i in range(filler_pool_size):
			item_pool.append(self.create_item(self.get_filler_item(i)))

		return item_pool

	def create_item(self, name: str) -> Item:
		data = item_table[name]

		if data.progression:
			classification = ItemClassification.progression
		elif data.useful:
			classification = ItemClassification.useful
		elif data.trap:
			classification = ItemClassification.trap
		else:
			classification = ItemClassification.filler

		item = Item(name, classification, data.code, self.player)

		if not item.advancement:
			return item

		if name == 'guild.exe' and self.is_option_enabled('HellTempleReward'):
			item.classification = ItemClassification.filler
		elif name == 'miracle.exe' and not self.is_option_enabled('RandomizeNPCs') and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'mekuri.exe' and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'Mulana Talisman' and not self.is_option_enabled('RandomizeCursedChests') and self.get_option_value('CursedChestCount') == 0:
			item.classification = ItemClassification.filler

		return item

	def get_filler_item(self, k: Optional[int]):
		if k == 1:
			return '200 coins'
		elif k == 2 or k == 3:
			return '100 coins'
		return self.multiworld.random.choices(['50 coins', '30 coins', '10 coins', '1 Weight'], weights=[1, 3, 6, 2], k=1)[0]

	def place_locked_item(self, location_name: str, item_name: str):
		self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(item_name))

	def is_option_enabled(self, option: str) -> bool:
		return is_option_enabled(self.multiworld, self.player, option)

	def get_option_value(self, option: str) -> Union[int, Dict, List]:
		return get_option_value(self.multiworld, self.player, option)