from typing import Dict
from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value
from .NPCs import get_npc_names

class LaMulanaWorldState:
	world: MultiWorld
	player: int
	npc_rando: bool
	include_dracuet: bool
	vanilla_transitions: bool
	npc_mapping: Dict[str,str]

	def __init__(self, world: MultiWorld, player: int):
		self.world = world
		self.player = player
		self.npc_rando = is_option_enabled(world, player, "RandomizeNPCs")
		self.include_dracuet = is_option_enabled(world, player, "RandomizeDracuetsShop")
		if self.npc_rando:
			self.build_npc_mapping()

	def randomize_npcs(self, npc_list: List[str]) -> Dict[str,str]:
		randomized_list = npc_list.copy()
		self.world.random.shuffle(randomized_list)
		return {npc_list[i]: randomized_list[i] for i in range(len(npc_list))}

	def npc_rando_checks_passed(self) -> bool:
		for surface_npc in ['Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner']:
			if mapping[surface_npc] == 'Elder Xelpud':
				return False
		if mapping['Yiear Kungfu'] == 'Yiegah Kungfu':
			return False
		if 'Tailor Dracuet' in mapping and mapping['Tailor Dracuet'] in ['Mulbruk', 'Fairy Queen', 'Elder Xelpud']:
			return False
		return True

	def build_npc_mapping(self):
		npc_names = get_npc_names(self.include_dracuet)
		mapping = self.randomize_npcs(npc_names)
		while not self.npc_rando_checks_passed():
			mapping = self.randomize_npcs(npc_names)
		self.npc_mapping = mapping