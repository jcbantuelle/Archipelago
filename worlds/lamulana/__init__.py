from typing import Dict, List, Set, Optional, TextIO, Union
from BaseClasses import Item, MultiWorld, Tutorial, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from .Options import lamulana_options, starting_location_names, starting_weapon_names, is_option_enabled, get_option_value
from .WorldState import LaMulanaWorldState
from .NPCs import get_npc_checks, get_npc_entrance_room_names, get_shop_location_names, npc_hint_order
from .Items import item_table, get_items_by_category, item_exclusion_order
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
		self.place_shop_items()
		self.multiworld.itempool += self.generate_item_pool()
		print('Currently', len(self.multiworld.get_unfilled_locations()), 'unfilled locations in the pool')

	def set_rules(self) -> None:
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all({'Mother Defeated', 'NPC: Mulbruk'}, self.player)
		
		if self.is_option_enabled('RandomizeCoinChests'):
			#local progression would be a problem for the escape coin chest - if it involves another player and loops back to us, that's fine
			escape_location = self.multiworld.get_location('Twin Labyrinths Escape Coin Chest', self.player)
			add_item_rule(escape_location, lambda item: item.player != self.player or item.classification != ItemClassification.progression)

	def extend_hint_information(self, hint_data: Dict[int, Dict[int,str]]):
		hint_info = {}
		if self.worldstate.cursed_chests:
			for cursed_chest_name in self.worldstate.cursed_chests:
				location = self.multiworld.get_location(cursed_chest_name, self.player)
				hint_info[location.address] = 'Cursed'
		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			room_names = get_npc_entrance_room_names()
			npc_checks = get_npc_checks(self.multiworld, self.player)
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name, locationdata_list in npc_checks.items():
				if npc_name in reverse_map:
					door_name = reverse_map[npc_name]
					print(npc_name, '-', room_names[door_name])
					for locationdata in locationdata_list:
						if not locationdata.is_event:
							hint_info[locationdata.code] = room_names[door_name]
		hint_data[self.player] = hint_info

	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		spoiler_handle.write(f'Cursed Chests:		{self.worldstate.cursed_chests}\n')
		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			spoiler_handle.write(f'NPC Randomizer:\n')
			room_names = get_npc_entrance_room_names()
			space_count = lambda name: ' ' * (25 - len(name))
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name in npc_hint_order:
				if npc_name in reverse_map:
					npc_door = reverse_map[npc_name]
					spoiler_handle.write(f'    - {npc_name}:{space_count(npc_name)}{room_names[npc_door]}\n')
		#Maybe also transition info? It's gonna be a lot

	def fill_slot_data(self) -> Dict[str, object]:
		slot_data : Dict[str, object] = {}
		for option_name in lamulana_options:
			slot_data[option_name] = self.get_option_value(option_name)
		return slot_data

	def assign_event_items(self):
		for location in self.multiworld.get_locations(self.player):
			if location.address is None:
				item_name = location.name
				if '—' in location.name:
					item_name = location.name[:location.name.find('—')].strip()
				item = Item(item_name, ItemClassification.progression, None, self.player)
				location.place_locked_item(item)

	def place_shop_items(self):
		starting_weapon = starting_weapon_names[self.get_option_value('StartingWeapon')]

		if starting_weapon in {'Shuriken', 'Rolling Shuriken', 'Flare Gun', 'Earth Spear', 'Bomb', 'Chakram', 'Caltrops', 'Pistol'}:
			required_subweapon_ammo = starting_weapon + ' Ammo'
		else:
			required_subweapon_ammo = None

		shop_locations: Set[str] = get_shop_location_names(self.multiworld, self.player)

		#Little Brother needs weights
		lil_bro_slot = self.multiworld.random.choice(['Yiegah Kungfu Shop Item 1', 'Yiegah Kungfu Shop Item 2', 'Yiegah Kungfu Shop Item 3'])
		self.place_locked_item(lil_bro_slot, '5 Weights')
		shop_locations.remove(lil_bro_slot)

		print('StartingLocation', self.get_option_value('StartingLocation'), ' -- name: ', starting_location_names[self.get_option_value('StartingLocation')])
		if starting_location_names[self.get_option_value('StartingLocation')] == 'surface':
			#Starting Shop doesn't exist in surface starts
			shop_locations.remove('Starting Shop Item 1')
			shop_locations.remove('Starting Shop Item 2')
			shop_locations.remove('Starting Shop Item 3')
			if self.is_option_enabled('RandomizeNPCs'):
				surface_shop_slots = []
				npc_checks = get_npc_checks(self.multiworld, self.player)
				#Assumes Xelpud is placed on his or Former Mekuri Master's spot - which WorldState handles
				for surface_npc_door in {'Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Hiner', 'Moger', 'Former Mekuri Master'}:
					npc_name = self.worldstate.npc_mapping[surface_npc_door]
					if npc_name in npc_checks:
						for location in npc_checks[npc_name]:
							if location.name in shop_locations:
								surface_shop_slots.append(location.name)
			else:
				surface_shop_slots = ['Nebur Shop Item 1', 'Nebur Shop Item 2', 'Nebur Shop Item 3', 'Sidro Shop Item 1', 'Sidro Shop Item 2', 'Sidro Shop Item 3', 'Modro Shop Item 1', 'Modro Shop Item 2', 'Modro Shop Item 3']
			if len(surface_shop_slots) > 0:
				weight_slot = self.multiworld.random.choice(surface_shop_slots)
				self.place_locked_item(weight_slot, '5 Weights')
				shop_locations.remove(weight_slot)
				if required_subweapon_ammo:
					surface_shop_slots.remove(weight_slot)
					ammo_slot = self.multiworld.random.choice(surface_shop_slots)
					self.place_locked_item(ammo_slot, required_subweapon_ammo)
					shop_locations.remove(ammo_slot)
		else:
			self.place_locked_item('Starting Shop Item 1', '5 Weights')
			shop_locations.remove('Starting Shop Item 1')
			if required_subweapon_ammo:
				self.place_locked_item('Starting Shop Item 2', required_subweapon_ammo)
				shop_locations.remove('Starting Shop Item 2')

		slot_amount = len(shop_locations) - self.get_option_value('ShopDensity')

		print('---------------', slot_amount, 'shop slots -----------------')
		#Guaranteed minimum amounts per ammo type and weights
		shop_items: List[str] = ['5 Weights', '5 Weights', '5 Weights']
		ammo_types = ['Shuriken Ammo', 'Rolling Shuriken Ammo', 'Earth Spear Ammo', 'Flare Gun Ammo', 'Bomb Ammo', 'Chakram Ammo', 'Caltrops Ammo', 'Pistol Ammo']
		for ammo_name in ammo_types:
			shop_items.extend([ammo_name, ammo_name])
		if slot_amount >= 20:
			shop_items.extend(['5 Weights'] + self.multiworld.random.choices(ammo_types + ['5 Weights'], k=slot_amount - len(shop_items) - 1))

		local_shop_inventory_list = self.multiworld.random.sample(list(shop_locations), slot_amount)

		print('shop inventory:', len(local_shop_inventory_list), ' - vs shop item amt:', len(shop_items))
		#print(slot_amount, 'Shop slots selected for ammo/weights:', local_shop_inventory_list)
		for ndx, location_name in enumerate(local_shop_inventory_list):
			location = self.place_locked_item(location_name, shop_items[ndx])

	def get_excluded_items(self) -> Set[str]:
		#101 base locations (chests + NPC checks) + 24 coin chests + 4 trap items + number of randomized items in shops + 1 Hell Temple check
		location_pool_size = 101 + (24 if self.is_option_enabled('RandomizeCoinChests') else 0) + (4 if self.is_option_enabled('RandomizeTrapItems') else 0) + self.get_option_value('ShopDensity') + (1 if self.is_option_enabled('HellTempleReward') else 0)

		item_pool_size = 125
		if self.is_option_enabled('AlternateMotherAnkh'):
			item_pool_size += 1
		
		if not self.is_option_enabled('HellTempleReward'):
			item_exclusion_order.append('guild.exe')

		for item_name, amt in self.multiworld.start_inventory[self.player].value.items():
			item_pool_size -= min(amt, item_table[item_name].count)
			if item_name in item_exclusion_order:
				item_exclusion_order.remove(item_name)

		pool_diff = item_pool_size - location_pool_size
		if pool_diff <= 0:
			return None

		return set(item_exclusion_order[:pool_diff])

	def generate_item_pool(self) -> List[Item]:
		item_pool: List[Item] = []
		excluded_items = self.get_excluded_items()

		for name, data in item_table.items():
			if excluded_items and name in excluded_items:
				continue
			for _ in range(data.count - (self.multiworld.start_inventory[self.player].value[name] if name in self.multiworld.start_inventory[self.player].value else 0)):
				item = self.create_item(name)
				item_pool.append(item)

		if self.is_option_enabled('AlternateMotherAnkh'):
			item_pool.append(self.create_item('Ankh Jewel'))

		filler_pool_size = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)

		print(len(self.multiworld.get_unfilled_locations(self.player)), 'unfilled locations - ', len(item_pool), 'items currently being added - ', filler_pool_size, 'current filler items')

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

		if name == 'guild.exe' and not self.is_option_enabled('HellTempleReward'):
			item.classification = ItemClassification.filler
		elif name == 'miracle.exe' and not self.is_option_enabled('RandomizeNPCs') and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'mekuri.exe' and not self.is_option_enabled('RequireKeyFairyCombo'):
			item.classification = ItemClassification.useful
		elif name == 'Mulana Talisman' and not self.is_option_enabled('RandomizeCursedChests') and self.get_option_value('CursedChestCount') == 0:
			item.classification = ItemClassification.filler

		return item

	def get_filler_item(self, k: Optional[int]):
		if k == 0:
			return '200 coins'
		elif k <= 2:
			return '100 coins'
		return self.multiworld.random.choices(['50 coins', '30 coins', '10 coins', '1 Weight'], weights=[1, 4, 6, 2], k=1)[0]

	def place_locked_item(self, location_name: str, item_name: str):
		self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(item_name))

	def is_option_enabled(self, option: str) -> bool:
		return is_option_enabled(self.multiworld, self.player, option)

	def get_option_value(self, option: str) -> Union[int, Dict, List]:
		return get_option_value(self.multiworld, self.player, option)