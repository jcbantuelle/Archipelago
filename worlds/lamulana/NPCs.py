from typing import List, Dict, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location, CollectionState
from .Options import is_option_enabled
from .Locations import LocationData
from .LogicShortcuts import LaMulanaLogicShortcuts
from random import shuffle

def build_npc_checks(randomized_shops: bool, s: LaMulanaLogicShortcuts) -> Dict[str,List[LocationData]]:
	return {
		'Elder Xelpud': [
			LocationData('NPC: Xelpud', 1, state: lambda: True, True),
			LocationData('Xelpud xmailer.exe Gift', 1),
			LocationData('Xelpud Mulana Talisman Gift', 1, lambda state: state.has('Diary', player))
		],
		'Nebur': [
			LocationData('Nebur Shop Item 1', 1),
			LocationData('Nebur Shop Item 2', 1),
			LocationData('Nebur Shop Item 3', 1),
			LocationData('Nebur Shop Item - 4 Guardians', 1, lambda state: s.guardian_count(state) >= 4)
		] if randomized_shops else [
			LocationData('Nebur Shop Item - 4 Guardians', 1, lambda state: s.guardian_count(state) >= 4)
		],
		'Sidro': [
			LocationData('Sidro Shop Item 1', 1),
			LocationData('Sidro Shop Item 2', 1),
			LocationData('Sidro Shop Item 3', 1)
		] if randomized_shops else [],
		'Modro': [
			LocationData('Modro Shop Item 1', 1),
			LocationData('Modro Shop Item 2', 1),
			LocationData('Modro Shop Item 3', 1)
		] if randomized_shops else [],
		'Former Mekuri Master': [
			LocationData('Former Mekuri Master mekuri.exe Gift', 1)
		],
		'Penadvent of Ghost': [
			LocationData('Penadvent of Ghost Shop Item 1', 1),
			LocationData('Penadvent of Ghost Shop Item 2', 1),
			LocationData('Penadvent of Ghost Shop Item 3', 1)
		] if randomized_shops else [],
		'Greedy Charlie': [
			LocationData('Greedy Charlie Shop Item 1', 1),
			LocationData('Greedy Charlie Shop Item 2', 1),
			LocationData('Greedy Charlie Shop Item 3', 1)
		] if randomized_shops else [],
		'Mulbruk': [
			LocationData('NPC: Mulbruk', 1, lambda state: True, True),
			LocationData('Mulbruk Book of the Dead Gift', 1, lambda state: state.can_reach('Temple of Moonlight [Southeast]'))
		],
		'Shalom III': [
			LocationData('Shalom III Shop Item 1', 1),
			LocationData('Shalom III Shop Item 2', 1),
			LocationData('Shalom III Shop Item 3', 1)
		] if randomized_shops else [],
		'Usas VI': [
			LocationData('Usas VI Shop Item 1', 1),
			LocationData('Usas VI Shop Item 2', 1),
			LocationData('Usas VI Shop Item 3', 1)
		] if randomized_shops else [],
		'Kingvalley I': [
			LocationData('Kingvalley I Shop Item 1', 1),
			LocationData('Kingvalley I Shop Item 2', 1),
			LocationData('Kingvalley I Shop Item 3', 1)
		] if randomized_shops else [],
		'Philosopher Giltoriyo': [
			LocationData('NPC: Philosopher Giltoriyo', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Mr. Fishman (Original)': [
			LocationData('Mr. Fishman (Original) Shop Item 1', 1),
			LocationData('Mr. Fishman (Original) Shop Item 2', 1),
			LocationData('Mr. Fishman (Original) Shop Item 3', 1)
		] if randomized_shops else [],
		'Mr. Fishman (Alt)': [
			LocationData('Mr. Fishman (Alt) Shop Item 1', 1),
			LocationData('Mr. Fishman (Alt) Shop Item 2', 1),
			LocationData('Mr. Fishman (Alt) Shop Item 3', 1)
		] if randomized_shops else [],
		'Hot-blooded Nemesistwo': [
			LocationData('Hot-blooded Nemesistwo Shop Item 1', 1),
			LocationData('Hot-blooded Nemesistwo Shop Item 2', 1),
			LocationData('Hot-blooded Nemesistwo Shop Item 3', 1)
		] if randomized_shops else [],
		'Operator Combaker': [
			LocationData('Operator Combaker Shop Item 1', 1),
			LocationData('Operator Combaker Shop Item 2', 1),
			LocationData('Operator Combaker Shop Item 3', 1)
		] if randomized_shops else [],
		'Yiegah Kungfu': [
			LocationData('Yiegah Kungfu Shop Item 1', 1),
			LocationData('Yiegah Kungfu Shop Item 2', 1),
			LocationData('Yiegah Kungfu Shop Item 3', 1),
			LocationData('NPC: Yiegah Kungfu', 1, lambda state: True, True)
		] if randomized_shops else [
			LocationData('NPC: Yiegah Kungfu', 1, lambda state: True, True)
		],
		'Yiear Kungfu': [
			LocationData('Yiear Kungfu Shop Item 1', 1),
			LocationData('Yiear Kungfu Shop Item 2', 1),
			LocationData('Yiear Kungfu Shop Item 3', 1)
		] if randomized_shops else [],
		'Arrogant Sturdy Snake': [
			LocationData('Arrogant Sturdy Snake Shop Item 1', 1),
			LocationData('Arrogant Sturdy Snake Shop Item 2', 1),
			LocationData('Arrogant Sturdy Snake Shop Item 3', 1)
		] if randomized_shops else [],
		'Arrogant Metagear': [
			LocationData('Arrogant Metagear Shop Item 1', 1),
			LocationData('Arrogant Metagear Shop Item 2', 1),
			LocationData('Arrogant Metagear Shop Item 3', 1)
		] if randomized_shops else [],
		'Fairy Queen': [
			LocationData('Fairies Unlocked', 1, lambda state: state.has("Isis' Pendant", player), True)
		],
		'Affected Knimare': [
			LocationData('Affected Knimare Shop Item 1', 1),
			LocationData('Affected Knimare Shop Item 2', 1),
			LocationData('Affected Knimare Shop Item 3', 1)
		] if randomized_shops else [],
		'Mr. Slushfund': [
			LocationData('Mr. Slushfund Pepper Gift', 1),
			LocationData('Mr. Slushfund Anchor Gift', 1, lambda state: state.has('Treasures', player))
		],
		'Priest Alest': [
			LocationData('Priest Alest Mini Doll Gift', 1)
		],
		'Mover Athleland': [
			LocationData('Mover Athleland Shop Item 1', 1),
			LocationData('Mover Athleland Shop Item 2', 1),
			LocationData('Mover Athleland Shop Item 3', 1)
		] if randomized_shops else [],
		'Giant Mopiran': [
			LocationData('Giant Mopiran Shop Item 1', 1),
			LocationData('Giant Mopiran Shop Item 2', 1),
			LocationData('Giant Mopiran Shop Item 3', 1)
		] if randomized_shops else [],
		'Philosopher Alsedana': [
			LocationData('NPC: Philosopher Alsedana', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Kingvalley II': [
			LocationData('Kingvalley II Shop Item 1', 1),
			LocationData('Kingvalley II Shop Item 2', 1),
			LocationData('Kingvalley II Shop Item 3', 1)
		] if randomized_shops else [],
		'Philosopher Samaranta': [
			LocationData('NPC: Philosopher Samaranta', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Energetic Belmont': [
			LocationData('Energetic Belmont Shop Item 1', 1),
			LocationData('Energetic Belmont Shop Item 2', 1),
			LocationData('Energetic Belmont Shop Item 3', 1)
		] if randomized_shops else [],
		'Mechanical Efspi': [
			LocationData('Mechanical Efspi Shop Item 1', 1),
			LocationData('Mechanical Efspi Shop Item 2', 1),
			LocationData('Mechanical Efspi Shop Item 3', 1)
		] if randomized_shops else [],
		'Mudman Qubert': [
			LocationData('Mudman Qubert Shop Item 1', 1),
			LocationData('Mudman Qubert Shop Item 2', 1),
			LocationData('Mudman Qubert Shop Item 3', 1)
		] if randomized_shops else [],
		'Philosopher Fobos': [
			LocationData('NPC: Philosopher Fobos', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Tailor Dracuet': [
			LocationData('Tailor Dracuet Shop Item 1', 1),
			LocationData('Tailor Dracuet Shop Item 2', 1),
			LocationData('Tailor Dracuet Shop Item 3', 1)
		] if randomized_shops else []
	}

def randomize_npcs(npc_list):
	randomized_list = npc_list.copy()
	shuffle(randomized_list)
	return {npc_list[i]: randomized_list[i] for i in range(len(npc_list))}

def npc_rando_checks_passed(mapping) -> bool:
	for surface_npc in ['Nebur', 'Sidro', 'Modro', 'Hiner', 'Moger']:
		if mapping[surface_npc] == 'Elder Xelpud':
			return False
	if mapping['Yiear Kungfu'] == 'Yiegah Kungfu':
		return False
	if 'Tailor Dracuet' in mapping and mapping['Tailor Dracuet'] == 'Fairy Queen':
		return False
	return True

def get_npc_mapping(npc_rando_on: bool, include_dracuet: bool):
	npc_names = ['Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Hiner', 'Moger', 'Former Mekuri Master', 'Priest Zarnac', 'Penadvent of Ghost', 'Priest Xanado', 'Greedy Charlie', 'Mulbruk', 'Shalom III', 'Usas VI', 'Kingvalley I', 'Priest Madomo', 'Priest Hidlyda', 'Philosopher Giltoriyo', 'Mr. Fishman (Original)', 'Mr. Fishman (Alt)', 'Priest Gailious', 'Hot-blooded Nemesistwo', 'Priest Romancis', 'Priest Aramo', 'Priest Triton', 'Operator Combaker', 'Yiegah Kungfu', 'Yiear Kungfu', 'Arrogant Sturdy Snake', 'Arrogant Metagear', 'Priest Jaguarfiv', 'Fairy Queen', 'Affected Knimare', 'duplex', 'Mr. Slushfund', 'Priest Alest', 'Mover Athleland', 'Giant Mopiran', 'Giant Thexde', 'Philosopher Alsedana', 'Samieru', 'Kingvalley II', 'Philosopher Samaranta', 'Naramura', 'Energetic Belmont', 'Priest Laydoc', 'Mechanical Efspi', 'Priest Ashgine', 'Mudman Qubert', 'Philosopher Fobos', '8-bit Elder']
	if include_dracuet:
		npc_names.append('Tailor Dracuet')
	if npc_rando_on:
		mapping = randomize_npcs(npc_names)
		while not npc_rando_checks_passed(mapping):
			mapping = randomize_npcs(npc_names)
		return mapping
	else:
		return {npc: npc for npc in npc_names}

def spring_npc(state: CollectionState, player: int, s: LaMulanaLogicShortcuts) -> bool:
	can_escape = s.state_shield(state) or s.attack_shuriken(state) or s.attack_flare_gun(state) or s.attack_caltrops(state) or state.has_any({'Leather Whip', 'Chain Whip', 'Flail Whip', 'Axe', 'Holy Grail'}, player)
	if not can_escape:
		return False
	if s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_caltrops(state) or s.attack_flare_gun(state) or state.has_any({'Knife', 'Axe', 'Katana'}, player):
		return True
	return state.has_any({'Helmet', 'Scalesphere', 'Sacred Orb'}, player) and state.has_any({'Leather Whip', 'Chain Whip', 'Flail Whip', 'Key Sword'}, player)

def get_npc_checks(npc_checks: Dict[str,List[LocationData]], mapping: Dict[str,str], door_name: str) -> List[LocationData]:
	npc_name = mapping[door_name]
	if npc_name in npcs_checks:
		return npc_checks[npc_name]
	return []


class LaMulanaNPCDoor(NamedTuple):
	name: str
	room_name: str
	checks: List[LocationData] = []
	logic: Optional[Callable[CollectionState,bool]] = None


def get_npcs(world: MultiWorld, player: int, s: LaMulanaLogicShortcuts) -> Dict[str,LaMulanaNPCDoor]:
	npc_rando = is_option_enabled(world, player, "RandomizeNPCs")
	shop_rando = is_option_enabled(world, player, "RandomizeShops")
	include_dracuet = is_option_enabled(world, player, "RandomizeDracuetsShop")
	mapping = get_npc_mapping(npc_rando, include_dracuet)

	npc_checks = build_npc_checks(shop_rando, s)

	npc_doors = {
		'Surface [Main]': [
			LaMulanaNPCDoor('Elder Xelpud', 'Surface - Village of Departure (Xelpud)', get_npc_checks(npc_checks, mapping, 'Elder Xelpud')),
			LaMulanaNPCDoor('Nebur', 'Surface - Village of Departure (Nebur)', get_npc_checks(npc_checks, mapping, 'Nebur'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor('Sidro', 'Surface - Village of Departure (Sidro)', get_npc_checks(npc_checks, mapping, 'Sidro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor('Modro', 'Surface - Village of Departure (Modro)', get_npc_checks(npc_checks, mapping, 'Modro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor('Hiner', 'Surface - Altar Hill', get_npc_checks(npc_checks, mapping, 'Hiner'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor('Moger', 'Surface - Village of Departure (Moger)', get_npc_checks(npc_checks, mapping, 'Moger'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor('Former Mekuri Master', 'Surface - Bahrun\'s Waterfall', get_npc_checks(npc_checks, mapping, 'Former Mekuri Master'), lambda state: s.attack_far(state) or s.attack_s_straight(state) or s.attack_earth_spear(state) or state.has("Katana", player)),
		],
		'Gate of Guidance [Main]': [
			LaMulanaNPCDoor('Priest Zarnac', 'Gate of Guidance - Pit of the Holy Grail', get_npc_checks(npc_checks, mapping, 'Priest Zarnac')),
			LaMulanaNPCDoor('Penadvent of Ghost', 'Gate of Guidance - Monument of Time', get_npc_checks(npc_checks, mapping, 'Penadvent of Ghost')),
		],
		'Mausoleum of the Giants': [
			LaMulanaNPCDoor('Priest Xanado', 'Mausoleum of the Giants (Room of Redemption)', get_npc_checks(npc_checks, mapping, 'Priest Xanado')),
			LaMulanaNPCDoor('Greedy Charlie', 'Mausoleum of the Giants (Monument to Hermes)', get_npc_checks(npc_checks, mapping, 'Greedy Charlie'), lambda state: s.attack_chest_any(state)),
		],
		'Temple of the Sun [Main]': [
			LaMulanaNPCDoor('Mulbruk', 'Temple of the Sun - Thoth\'s Room', get_npc_checks(npc_checks, mapping, 'Mulbruk'), lambda state: s.boss_count(state) >= 1 and state.has('Origin Seal', player)),
			LaMulanaNPCDoor('Shalom III', 'Temple of the Sun - Altar of War', get_npc_checks(npc_checks, mapping, 'Shalom III'), lambda state: s.attack_shuriken(state) or s.attack_bomb(state) or s.glitch_catpause(state) or (state.has('Feather', player) and (s.attack_forward(state) or s.attack_chakram(state)))),
			LaMulanaNPCDoor('Usas VI', 'Temple of the Sun - Sanctuary', get_npc_checks(npc_checks, mapping, 'Usas VI')),
			LaMulanaNPCDoor('Kingvalley I', 'Temple of the Sun - Horus\' Room of Pillars', get_npc_checks(npc_checks, mapping, 'Kingvalley I'), lambda state: state.has_all({'Feather', 'Death Seal'}, player)),
		],
		'Temple of the Sun [Sphinx]': [
			LaMulanaNPCDoor('Priest Madomo', 'Temple of the Sun - Great Colonnade, Right-side room', get_npc_checks(npc_checks, mapping, 'Priest Madomo')),
		],
		'Spring in the Sky [Main]': [
			LaMulanaNPCDoor('Priest Hidlyda', 'Spring in the Sky - Mirror Waterfall', get_npc_checks(npc_checks, mapping, 'Priest Hidlyda'), lambda state: spring_npc(state, player, s)),
			LaMulanaNPCDoor('Philosopher Giltoriyo', 'Spring in the Sky - Mural of Oannes', get_npc_checks(npc_checks, mapping, 'Philosopher Giltoriyo')),
		],
		'Spring in the Sky [Upper]': [
			LaMulanaNPCDoor('Mr. Fishman (Original)', 'Spring in the Sky - Waterfall Approach (Original)', get_npc_checks(npc_checks, mapping, 'Mr. Fishman (Original)'), lambda state: state.has_all({'Helmet', 'Origin Seal'}, player)),
			LaMulanaNPCDoor('Mr. Fishman (Alt)', 'Spring in the Sky - Waterfall Approach (Alt)', get_npc_checks(npc_checks, mapping, 'Mr. Fishman (Alt)'), lambda state: state.has_all({'Helmet', 'Origin Seal'}) and s.state_key_fairy_access(state)),
		],
		'Inferno Cavern [Main]': [
			LaMulanaNPCDoor('Priest Gailious', 'Inferno Cavern - Pit of Fire', get_npc_checks(npc_checks, mapping, 'Priest Gailious')),
			LaMulanaNPCDoor('Hot-blooded Nemesistwo', 'Inferno Cavern - Anterior Chamber', get_npc_checks(npc_checks, mapping, 'Hot-blooded Nemesistwo'), lambda state: s.attack_chest_any(state)),
		],
		'Inferno Cavern [Pazuzu]': [
			LaMulanaNPCDoor('Priest Romancis', 'Inferno Cavern - Pazuzu\'s Room', get_npc_checks(npc_checks, mapping, 'Priest Romancis')),
		],
		'Chamber of Extinction [Main]': [
			LaMulanaNPCDoor('Priest Aramo', 'Chamber of Extinction - Mural of Light', get_npc_checks(npc_checks, mapping, 'Priest Aramo'), lambda state: s.attack_chest_any(state)),
		],
		'Chamber of Extinction [Ankh Lower]': [
			LaMulanaNPCDoor('Priest Triton', 'Chamber of Extinction - Palenque\'s Coffin', get_npc_checks(npc_checks, mapping, 'Priest Triton'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor('Operator Combaker', 'Chamber of Extinction - Shiva\'s Crucifix', get_npc_checks(npc_checks, mapping, 'Operator Combaker'), lambda state: s.attack_chest_any(state)),
		],
		'Twin Labyrinths [Loop]': [
			LaMulanaNPCDoor('Yiegah Kungfu', 'Twin Labyrinths - Twin\'s Surrounding Wall (Little Brother)', get_npc_checks(npc_checks, mapping, 'Yiegah Kungfu')),
			LaMulanaNPCDoor('Yiear Kungfu', 'Twin Labyrinths - Twin\'s Surrounding Wall (Big Brother)', get_npc_checks(npc_checks, mapping, 'Yiear Kungfu'), lambda state: state.has('NPC: Yiegah Kungfu', player)),
		],
		'Twin Labyrinths [Lower]': [
			LaMulanaNPCDoor('Arrogant Sturdy Snake', 'Twin Labyrinths - Treasury (Right)', get_npc_checks(npc_checks, mapping, 'Arrogant Sturdy Snake'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor('Arrogant Metagear', 'Twin Labyrinths - Treasury (Left)', get_npc_checks(npc_checks, mapping, 'Arrogant Metagear'), lambda state: (state.has('Feather', player) and s.attack_bomb(state)) or s.glitch_raindrop(state)),
		],
		'Twin Labyrinths [Poseidon]': [
			LaMulanaNPCDoor('Priest Jaguarfiv', 'Twin Labyrinths - Sanctuary', get_npc_checks(npc_checks, mapping, 'Priest Jaguarfiv')),
		],
		'Endless Corridor [1F]': [
			LaMulanaNPCDoor('Fairy Queen', 'Endless Corridor - First Endless Corridor (Fairy Queen)', get_npc_checks(npc_checks, mapping, 'Fairy Queen')),
			LaMulanaNPCDoor('Affected Knimare', 'Endless Corridor - First Endless Corridor (Seal)', get_npc_checks(npc_checks, mapping, 'Affected Knimare'), lambda state: state.has('Origin Seal', player)),
		],
		'Gate of Illusion [Grail]': [
			LaMulanaNPCDoor('duplex', 'Gate of Illusion - Chi You\'s Room', get_npc_checks(npc_checks, mapping, 'duplex'), lambda state: state.has('Chi You Defeated', player) and s.attack_forward(state) and s.combo_dev_npcs(state)),
		],
		'Gate of Illusion [Dracuet]': [
			LaMulanaNPCDoor('Mr. Slushfund', 'Gate of Illusion - Sacred Lake of the Sky (Mr. Slushfund)', get_npc_checks(npc_checks, mapping, 'Mr. Slushfund'), lambda state: s.attack_chest(state)),
			LaMulanaNPCDoor('Priest Alest', 'Gate of Illusion - Sacred Lake of the Sky (Mini Doll)', get_npc_checks(npc_checks, mapping, 'Priest Alest'), lambda state: s.attack_chest(state) and state.has('Anchor', player)),
		],
		'Gate of Illusion [Middle]': [
			LaMulanaNPCDoor('Mover Athleland', 'Gate of Illusion - Lizard\'s Room', get_npc_checks(npc_checks, mapping, 'Mover Athleland')),
		],
		'Graveyard of the Giants [West]': [
			LaMulanaNPCDoor('Giant Mopiran', 'Graveyard of the Giants - First Tomb', get_npc_checks(npc_checks, mapping, 'Giant Mopiran')),
		],
		'Graveyard of the Giants [East]': [
			LaMulanaNPCDoor('Giant Thexde', 'Graveyard of the Giants - Anterior Chamber', get_npc_checks(npc_checks, mapping, 'Giant Thexde'), lambda state: state.has('Feather', player)),
		],
		'Temple of Moonlight [Pyramid]': [
			LaMulanaNPCDoor('Philosopher Alsedana', 'Temple of Moonlight - Moon Watchtower', get_npc_checks(npc_checks, mapping, 'Philosopher Alsedana')),
		],
		'Temple of Moonlight [Upper]': [
			LaMulanaNPCDoor('Samieru', 'Temple of Moonlight - Serdab of Power', get_npc_checks(npc_checks, mapping, 'Samieru'), lambda state: s.combo_dev_npcs(state) and ((s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state)))) and (s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state)))
		],
		'Temple of Moonlight [Southeast]': [
			LaMulanaNPCDoor('Kingvalley II', 'Temple of Moonlight - Serdab of Treasure', get_npc_checks(npc_checks, mapping, 'Kingvalley II'), lambda state: s.attack_bomb(state) or (s.glitch_catpause(state) and s.attack_forward(state))),
		],
		'Tower of the Goddess [Lower]': [
			LaMulanaNPCDoor('Philosopher Samaranta', 'Tower of the Goddess - Scales of the Heart', get_npc_checks(npc_checks, mapping, 'Philosopher Samaranta'), lambda state: state.has('Flooded Tower of the Goddess', player)),
			LaMulanaNPCDoor('Naramura', 'Tower of the Goddess - Skuld\'s Tower', get_npc_checks(npc_checks, mapping, 'Naramura'), lambda state: s.combo_dev_npcs(state)),
			LaMulanaNPCDoor('Energetic Belmont', 'Tower of the Goddess - Verdandi\'s Tower', get_npc_checks(npc_checks, mapping, 'Energetic Belmont'), lambda state: ((state.has('Flooded Tower of the Goddess', player) and s.state_lamp(state)) or (s.glitch_raindrop(state) and state.has('Feather', player))) and state.has_any({'Anchor', 'Holy Grail'}, player)),
		],
		'Tower of Ruin [Southwest]': [
			LaMulanaNPCDoor('Priest Laydoc', 'Tower of Ruin - Fountain of Heat', get_npc_checks(npc_checks, mapping, 'Priest Laydoc')),
		],
		'Tower of Ruin [Grail]': [
			LaMulanaNPCDoor('Mechanical Efspi', 'Tower of Ruin - One Who Reads Tablets', get_npc_checks(npc_checks, mapping, 'Mechanical Efspi'), lambda state: state.has_any({'Feather', 'Grapple Claw'}, player) and (s.attack_below(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_rolling_shuriken(state) or s.attack_caltrops(state))),
		],
		'Chamber of Birth [West]': [
			LaMulanaNPCDoor('Priest Ashgine', 'Chamber of Birth - Brahma\'s Room (Priest Ashgine)', get_npc_checks(npc_checks, mapping, 'Priest Ashgine')),
			LaMulanaNPCDoor('Mudman Qubert', 'Chamber of Birth - Brahma\'s Room (Mudman Qubert)', get_npc_checks(npc_checks, mapping, 'Mudman Qubert'), lambda state: state.has('Mudmen Awakened', player)),
		],
		'Dimensional Corridor [Grail]': [
			LaMulanaNPCDoor('Philosopher Fobos', 'Dimensional Corridor - Kuusarikku\'s Room', get_npc_checks(npc_checks, mapping, 'Philosopher Fobos'), lambda state: state.has('Left Side Children Defeated')),
		],
		'Gate of Time [Surface]': [
			LaMulanaNPCDoor('8-bit Elder', 'Gate of Time [Surface]', 'Gate of Time - 8-bit Surface', get_npc_checks(npc_checks, mapping, '8-bit Elder'))
		]
	}

	if include_dracuet:
		npc_doors['Hell Temple [Shop]'] = [
			LaMulanaNPCDoor('Tailor Dracuet', 'Hell Temple - Room 14', get_npc_checks(npc_checks, mapping, 'Tailor Dracuet'))
		]

	return npc_doors