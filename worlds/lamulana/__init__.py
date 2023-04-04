from typing import Dict, TextIO
from BaseClasses import Item, MultiWorld, Tutorial, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Options import lamulana_options, starting_location_ids, starting_weapon_ids, is_option_enabled, get_option_value
from .WorldState import LaMulanaWorldState
from .NPCs import get_npc_checks, get_npc_entrance_room_names

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
	required_client_version = (0, 3, 100) #Placeholder version number
	
	worldstate: LaMulanaWorldState

	def __init__(self, world : MultiWorld, player: int):
		super().init(world, player)
		self.worldstate = LaMulanaWorldState(self.multiworld, self.player)

	def generate_early(self) -> None:
		#Do stuff that can still modify settings
		if self.multiworld.start_inventory[self.player].value.pop("Holy Grail", 0) > 0:
			self.multiworld.StartWithHolyGrail[self.player].value = self.multiworld.StartWithHolyGrail[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Hand Scanner", 0) > 0:
			self.multiworld.StartWithHandScanner[self.player].value = self.multiworld.StartWithHandScanner[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Reader", 0) > 0:
			self.multiworld.StartWithReader[self.player].value = self.multiworld.StartWithReader[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Hermes' Boots", 0) > 0:
			self.multiworld.StartWithHermesBoots[self.player].value = self.multiworld.StartWithHermesBoots[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Grapple Claw", 0) > 0:
			self.multiworld.StartWithGrappleClaw[self.player].value = self.multiworld.StartWithGrappleClaw[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Feather", 0) > 0:
			self.multiworld.StartWithFeather[self.player].value = self.multiworld.StartWithFeather[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Isis Pendant", 0) > 0:
			self.multiworld.StartWithIsisPendant[self.player].value = self.multiworld.StartWithIsisPendant[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Bronze Mirror", 0) > 0:
			self.multiworld.StartWithBronzeMirror[self.player].value = self.multiworld.StartWithBronzeMirror[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("Ring", 0) > 0:
			self.multiworld.StartWithRing[self.player].value = self.multiworld.StartWithRing[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("mirai.exe", 0) > 0:
			self.multiworld.StartWithMirai[self.player].value = self.multiworld.StartWithMirai[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("TextTrax", 0) > 0:
			self.multiworld.StartWithTextTrax[self.player].value = self.multiworld.StartWithTextTrax[self.player].option_true
		if self.multiworld.start_inventory[self.player].value.pop("xmailer.exe", 0) > 0:
			self.multiworld.StartWithXmailer[self.player].value = self.multiworld.StartWithXmailer[self.player].option_true
		#Give starting weapon, plane model on Goddess start, twin statue on Twin front start, flare gun on extinction start w/o the setting, maybe leather whip on Sun start if grailless and your starting weapon doesn't hit sides? etc

	def create_regions(self) -> None:
		create_regions_and_locations(self.multiworld, self.player)

	def create_items(self) -> None:
		pass

	def set_rules(self) -> None:
		victory_condition_1 = "Mother Defeated"
		victory_condition_2 = "NPC: Mulbruk"
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all({victory_condition_1, victory_condition_2}, self.player)

	def extend_hint_information(self, hint_data: Dict[int, Dict[int,str]]):
		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			npc_hint_info = {}
			room_names = get_npc_entrance_room_names()
			npc_checks = get_npc_checks(self.multiworld, self.player)
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name, locationdata_list in npc_checks.items():
				if npc_name != 'Starting Shop':
					door_name = reverse_map[npc_name]
					for locationdata in locationdata_list:
						if not locationdata.is_event:
							npc_hint_info[locationdata.code] = room_names[door_name]
			hint_data[self.player] = npc_hint_info


	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		locations = {y: x for x, y in starting_location_ids.items()}
		weapons = {y: x for x, y in starting_weapon_ids.items()}
		spoiler_handle.write(f'Starting weapon:		{weapons[self.get_option_value("StartingWeapon")]}\n')
		spoiler_handle.write(f'Starting area:		{locations[self.get_option_value("StartingLocation")]}\n')
		#Maybe also transition info? It's gonna be a lot

	def fill_slot_data(self) -> Dict[str, object]:
		slot_data : Dict[str, object] = {}
		for option_name in lamulana_options:
			slot_data[option_name] = self.get_option_value(option_name)
		return slot_data

	def is_option_enabled(self, option: str) -> bool:
		return is_option_enabled(self.multiworld, self.player, option)

	def get_option_value(self, option: str) -> Union[int, Dict, List]:
		return get_option_value(self.multiworld, self.player, option)