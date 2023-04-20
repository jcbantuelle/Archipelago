from typing import List, Set, Dict, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location, CollectionState
from .Options import is_option_enabled, get_option_value, starting_location_ids
from .Locations import LocationData
from .LogicShortcuts import LaMulanaLogicShortcuts
from .WorldState import LaMulanaWorldState

class LaMulanaNPCDoor(NamedTuple):
	checks: List[LocationData] = []
	logic: Optional[Callable[CollectionState,bool]] = None

def get_shop_location_names(world: MultiWorld, player: int) -> Set[str]:
	locations : Set[str] = set()
	npc_to_checks = get_npc_checks(world, player)
	for checks in npc_to_checks.values():
		for check in checks:
			if check.is_shop:
				locations.add(check.name)
	return locations

def get_npc_checks(world: Optional[MultiWorld], player: Optional[int]) -> Dict[str,List[LocationData]]:
	s = LaMulanaLogicShortcuts(world, player)
	include_dracuet = not world or is_option_enabled(world, player, 'RandomizeDracuetsShop')
	return {
		'Starting Shop': [
			LocationData('Starting Shop Item 1', 2359200, is_shop=True),
			LocationData('Starting Shop Item 2', 2359201, is_shop=True),
			LocationData('Starting Shop Item 3', 2359202, is_shop=True)
		],
		'Elder Xelpud': [
			LocationData('Xelpud xmailer.exe Gift', 2359203),
			LocationData('Xelpud Mulana Talisman Gift', 2359204, lambda state: state.has('Diary', player)),
			LocationData('NPC: Xelpud', None, lambda state: True, True),
		],
		'Nebur': [
			LocationData('Nebur Shop Item 1', 2359205, is_shop=True),
			LocationData('Nebur Shop Item 2', 2359206, is_shop=True),
			LocationData('Nebur Shop Item 3', 2359207, is_shop=True),
			#Must be an item, so doesn't get marked as shop
			LocationData('Nebur Shop Item - 4 Guardians', 2359208, lambda state: s.guardian_count(state) >= 4)
		],
		'Sidro': [
			LocationData('Sidro Shop Item 1', 2359209, is_shop=True),
			LocationData('Sidro Shop Item 2', 2359210, is_shop=True),
			LocationData('Sidro Shop Item 3', 2359211, is_shop=True)
		],
		'Modro': [
			LocationData('Modro Shop Item 1', 2359212, is_shop=True),
			LocationData('Modro Shop Item 2', 2359213, is_shop=True),
			LocationData('Modro Shop Item 3', 2359214, is_shop=True)
		],
		'Former Mekuri Master': [
			LocationData('Former Mekuri Master mekuri.exe Gift', 2359215)
		],
		'Penadvent of Ghost': [
			LocationData('Penadvent of Ghost Shop Item 1', 2359216, is_shop=True),
			LocationData('Penadvent of Ghost Shop Item 2', 2359217, is_shop=True),
			LocationData('Penadvent of Ghost Shop Item 3', 2359218, is_shop=True)
		],
		'Greedy Charlie': [
			LocationData('Greedy Charlie Shop Item 1', 2359219, is_shop=True),
			LocationData('Greedy Charlie Shop Item 2', 2359220, is_shop=True),
			LocationData('Greedy Charlie Shop Item 3', 2359221, is_shop=True)
		],
		'Mulbruk': [
			LocationData('Mulbruk Book of the Dead Gift', 2359222, lambda state: state.can_reach('Temple of Moonlight [Southeast]', 'Region', player)),
			LocationData('NPC: Mulbruk', None, lambda state: True, True),
		],
		'Shalom III': [
			LocationData('Shalom III Shop Item 1', 2359223, is_shop=True),
			LocationData('Shalom III Shop Item 2', 2359224, is_shop=True),
			LocationData('Shalom III Shop Item 3', 2359225, is_shop=True)
		],
		'Usas VI': [
			LocationData('Usas VI Shop Item 1', 2359226, is_shop=True),
			LocationData('Usas VI Shop Item 2', 2359227, is_shop=True),
			LocationData('Usas VI Shop Item 3', 2359228, is_shop=True)
		],
		'Kingvalley I': [
			LocationData('Kingvalley I Shop Item 1', 2359229, is_shop=True),
			LocationData('Kingvalley I Shop Item 2', 2359230, is_shop=True),
			LocationData('Kingvalley I Shop Item 3', 2359231, is_shop=True)
		],
		'Philosopher Giltoriyo': [
			LocationData('NPC: Philosopher Giltoriyo', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Mr. Fishman (Original)': [
			LocationData('Mr. Fishman (Original) Shop Item 1', 2359232, is_shop=True),
			LocationData('Mr. Fishman (Original) Shop Item 2', 2359233, is_shop=True),
			LocationData('Mr. Fishman (Original) Shop Item 3', 2359234, is_shop=True)
		],
		'Mr. Fishman (Alt)': [
			LocationData('Mr. Fishman (Alt) Shop Item 1', 2359235, is_shop=True),
			LocationData('Mr. Fishman (Alt) Shop Item 2', 2359236, is_shop=True),
			LocationData('Mr. Fishman (Alt) Shop Item 3', 2359237, is_shop=True)
		],
		'Hot-blooded Nemesistwo': [
			LocationData('Hot-blooded Nemesistwo Shop Item 1', 2359238, is_shop=True),
			LocationData('Hot-blooded Nemesistwo Shop Item 2', 2359239, is_shop=True),
			LocationData('Hot-blooded Nemesistwo Shop Item 3', 2359240, is_shop=True)
		],
		'Operator Combaker': [
			LocationData('Operator Combaker Shop Item 1', 2359241, is_shop=True),
			LocationData('Operator Combaker Shop Item 2', 2359242, is_shop=True),
			LocationData('Operator Combaker Shop Item 3', 2359243, is_shop=True)
		],
		'Yiegah Kungfu': [
			LocationData('Yiegah Kungfu Shop Item 1', 2359244, is_shop=True),
			LocationData('Yiegah Kungfu Shop Item 2', 2359245, is_shop=True),
			LocationData('Yiegah Kungfu Shop Item 3', 2359246, is_shop=True),
			LocationData('NPC: Yiegah Kungfu', None, lambda state: True, True)
		],
		'Yiear Kungfu': [
			LocationData('Yiear Kungfu Shop Item 1', 2359247, is_shop=True),
			LocationData('Yiear Kungfu Shop Item 2', 2359248, is_shop=True),
			LocationData('Yiear Kungfu Shop Item 3', 2359249, is_shop=True)
		],
		'Arrogant Sturdy Snake': [
			LocationData('Arrogant Sturdy Snake Shop Item 1', 2359250, is_shop=True),
			LocationData('Arrogant Sturdy Snake Shop Item 2', 2359251, is_shop=True),
			LocationData('Arrogant Sturdy Snake Shop Item 3', 2359252, is_shop=True)
		],
		'Arrogant Metagear': [
			LocationData('Arrogant Metagear Shop Item 1', 2359253, is_shop=True),
			LocationData('Arrogant Metagear Shop Item 2', 2359254, is_shop=True),
			LocationData('Arrogant Metagear Shop Item 3', 2359255, is_shop=True)
		],
		'Fairy Queen': [
			LocationData('Fairies Unlocked', None, lambda state: state.has("Isis' Pendant", player), True)
		],
		'Affected Knimare': [
			LocationData('Affected Knimare Shop Item 1', 2359256, is_shop=True),
			LocationData('Affected Knimare Shop Item 2', 2359257, is_shop=True),
			LocationData('Affected Knimare Shop Item 3', 2359258, is_shop=True)
		],
		'Mr. Slushfund': [
			LocationData('Mr. Slushfund Pepper Gift', 2359259),
			LocationData('Mr. Slushfund Anchor Gift', 2359260, lambda state: state.has('Treasures', player))
		],
		'Priest Alest': [
			LocationData('Priest Alest Mini Doll Gift', 2359261)
		],
		'Mover Athleland': [
			LocationData('Mover Athleland Shop Item 1', 2359262, is_shop=True),
			LocationData('Mover Athleland Shop Item 2', 2359263, is_shop=True),
			LocationData('Mover Athleland Shop Item 3', 2359264, is_shop=True)
		],
		'Giant Mopiran': [
			LocationData('Giant Mopiran Shop Item 1', 2359265, is_shop=True),
			LocationData('Giant Mopiran Shop Item 2', 2359266, is_shop=True),
			LocationData('Giant Mopiran Shop Item 3', 2359267, is_shop=True)
		],
		'Philosopher Alsedana': [
			LocationData('NPC: Philosopher Alsedana', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Kingvalley II': [
			LocationData('Kingvalley II Shop Item 1', 2359268, is_shop=True),
			LocationData('Kingvalley II Shop Item 2', 2359269, is_shop=True),
			LocationData('Kingvalley II Shop Item 3', 2359270, is_shop=True)
		],
		'Philosopher Samaranta': [
			LocationData('NPC: Philosopher Samaranta', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Energetic Belmont': [
			LocationData('Energetic Belmont Shop Item 1', 2359271, is_shop=True),
			LocationData('Energetic Belmont Shop Item 2', 2359272, is_shop=True),
			LocationData('Energetic Belmont Shop Item 3', 2359273, is_shop=True)
		],
		'Mechanical Efspi': [
			LocationData('Mechanical Efspi Shop Item 1', 2359274, is_shop=True),
			LocationData('Mechanical Efspi Shop Item 2', 2359275, is_shop=True),
			LocationData('Mechanical Efspi Shop Item 3', 2359276, is_shop=True)
		],
		'Mudman Qubert': [
			LocationData('Mudman Qubert Shop Item 1', 2359277, is_shop=True),
			LocationData('Mudman Qubert Shop Item 2', 2359278, is_shop=True),
			LocationData('Mudman Qubert Shop Item 3', 2359279, is_shop=True)
		],
		'Philosopher Fobos': [
			LocationData('NPC: Philosopher Fobos', None, lambda state: state.has("Philosopher's Ocarina", player), True)
		],
		'Tailor Dracuet': [
			LocationData('Tailor Dracuet Shop Item 1', 2359280, is_shop=True),
			LocationData('Tailor Dracuet Shop Item 2', 2359281, is_shop=True),
			LocationData('Tailor Dracuet Shop Item 3', 2359282, is_shop=True)
		] if include_dracuet else []
	}


def get_npc_entrances(world: MultiWorld, player: int, worldstate: LaMulanaWorldState, s: LaMulanaLogicShortcuts) -> Dict[str,List[LaMulanaNPCDoor]]:
	npc_checks = get_npc_checks(world, player)
	if worldstate.npc_rando and worldstate.npc_mapping:
		get_entrance_checks = lambda door: npc_checks[worldstate.npc_mapping[door]] if door in worldstate.npc_mapping and worldstate.npc_mapping[door] in npc_checks else [] 
	else:
		get_entrance_checks = lambda door: npc_checks[door] if door in npc_checks else []

	is_surface_start = get_option_value(world, player, "StartingLocation") == starting_location_ids['surface']

	npc_doors = {
		'Menu': [
			#Starting shop exists only in non-surface starts, and isn't affected by NPC rando
			LaMulanaNPCDoor(npc_checks['Starting Shop'])
		] if not is_surface_start else [],
		'Surface [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Elder Xelpud')),
			LaMulanaNPCDoor(get_entrance_checks('Nebur'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Sidro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Modro'), lambda state: state.has('NPC: Xelpud', player)),
			LaMulanaNPCDoor(get_entrance_checks('Moger'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor(get_entrance_checks('Hiner'), lambda state: state.has("NPC: Xelpud", player)),
			LaMulanaNPCDoor(get_entrance_checks('Former Mekuri Master'), lambda state: s.attack_far(state) or s.attack_s_straight(state) or s.attack_earth_spear(state) or state.has("Katana", player)),
		],
		'Gate of Guidance [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Zarnac')),
			LaMulanaNPCDoor(get_entrance_checks('Penadvent of Ghost')),
		],
		'Mausoleum of the Giants': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Xanado')),
			LaMulanaNPCDoor(get_entrance_checks('Greedy Charlie'), lambda state: s.attack_chest_any(state)),
		],
		'Temple of the Sun [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Mulbruk'), lambda state: s.guardian_count(state) >= 1 and state.has(worldstate.get_seal_name('Sun Mulbruk Origin'), player)),
			LaMulanaNPCDoor(get_entrance_checks('Shalom III'), lambda state: s.attack_shuriken(state) or s.attack_bomb(state) or s.glitch_catpause(state) or (state.has('Feather', player) and (s.attack_forward(state) or s.attack_chakram(state)))),
			LaMulanaNPCDoor(get_entrance_checks('Usas VI')),
			LaMulanaNPCDoor(get_entrance_checks('Kingvalley I'), lambda state: state.has_all({'Feather', worldstate.get_seal_name('Sun Death')}, player)),
		],
		'Temple of the Sun [Sphinx]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Madomo')),
		],
		'Spring in the Sky [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Hidlyda'), lambda state: s.spring_npc(state)),
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Giltoriyo')),
		],
		'Spring in the Sky [Upper]': [
			LaMulanaNPCDoor(get_entrance_checks('Mr. Fishman (Original)'), lambda state: state.has_all({'Helmet', worldstate.get_seal_name('Spring Fishman Origin')}, player)),
			LaMulanaNPCDoor(get_entrance_checks('Mr. Fishman (Alt)'), lambda state: state.has_all({'Helmet', worldstate.get_seal_name('Spring Fishman Origin')}, player) and s.state_key_fairy_access(state)),
		],
		'Inferno Cavern [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Gailious')),
			LaMulanaNPCDoor(get_entrance_checks('Hot-blooded Nemesistwo'), lambda state: s.attack_chest_any(state)),
		],
		'Inferno Cavern [Pazuzu]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Romancis')),
		],
		'Chamber of Extinction [Main]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Aramo'), lambda state: s.attack_chest_any(state)),
		],
		'Chamber of Extinction [Ankh Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Triton'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor(get_entrance_checks('Operator Combaker'), lambda state: s.attack_chest_any(state)),
		],
		'Twin Labyrinths [Loop]': [
			LaMulanaNPCDoor(get_entrance_checks('Yiegah Kungfu')),
			LaMulanaNPCDoor(get_entrance_checks('Yiear Kungfu'), lambda state: state.has('NPC: Yiegah Kungfu', player)),
		],
		'Twin Labyrinths [Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Arrogant Sturdy Snake'), lambda state: state.has('Feather', player)),
			LaMulanaNPCDoor(get_entrance_checks('Arrogant Metagear'), lambda state: (state.has('Feather', player) and s.attack_bomb(state)) or (state.has('Zu Defeated', player) and s.glitch_raindrop(state))),
		],
		'Twin Labyrinths [Poseidon]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Jaguarfiv')),
		],
		'Endless Corridor [1F]': [
			LaMulanaNPCDoor(get_entrance_checks('Fairy Queen')),
			LaMulanaNPCDoor(get_entrance_checks('Affected Knimare'), lambda state: state.has(worldstate.get_seal_name('Endless Origin'), player)),
		],
		'Gate of Illusion [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('duplex'), lambda state: state.has('Chi You Defeated', player) and s.attack_forward(state) and s.combo_dev_npcs(state)),
		],
		'Gate of Illusion [Dracuet]': [
			LaMulanaNPCDoor(get_entrance_checks('Mr. Slushfund'), lambda state: s.attack_chest(state)),
			LaMulanaNPCDoor(get_entrance_checks('Priest Alest'), lambda state: s.attack_chest(state) and state.has('Anchor', player)),
		],
		'Gate of Illusion [Middle]': [
			LaMulanaNPCDoor(get_entrance_checks('Mover Athleland')),
		],
		'Graveyard of the Giants [West]': [
			LaMulanaNPCDoor(get_entrance_checks('Giant Mopiran')),
		],
		'Graveyard of the Giants [East]': [
			LaMulanaNPCDoor(get_entrance_checks('Giant Thexde'), lambda state: state.has('Feather', player)),
		],
		'Temple of Moonlight [Pyramid]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Alsedana')),
		],
		'Temple of Moonlight [Upper]': [
			LaMulanaNPCDoor(get_entrance_checks('Samieru'), lambda state: s.combo_dev_npcs(state) and ((s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state)))) and (s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state)))
		],
		'Temple of Moonlight [Southeast]': [
			LaMulanaNPCDoor(get_entrance_checks('Kingvalley II'), lambda state: s.attack_bomb(state) or (s.glitch_catpause(state) and s.attack_forward(state))),
		],
		'Tower of the Goddess [Lower]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Samaranta'), lambda state: state.has('Flooded Tower of the Goddess', player)),
			LaMulanaNPCDoor(get_entrance_checks('Naramura'), lambda state: s.combo_dev_npcs(state)),
			LaMulanaNPCDoor(get_entrance_checks('Energetic Belmont'), lambda state: ((state.has('Flooded Tower of the Goddess', player) and s.state_lamp(state)) or (s.glitch_raindrop(state) and state.has('Feather', player))) and state.has_any({'Anchor', 'Holy Grail'}, player)),
		],
		'Tower of Ruin [Southwest]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Laydoc')),
		],
		'Tower of Ruin [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('Mechanical Efspi'), lambda state: state.has_any({'Feather', 'Grapple Claw'}, player) and (s.attack_below(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_rolling_shuriken(state) or s.attack_caltrops(state))),
		],
		'Chamber of Birth [West]': [
			LaMulanaNPCDoor(get_entrance_checks('Priest Ashgine')),
			LaMulanaNPCDoor(get_entrance_checks('Mudman Qubert'), lambda state: state.has('Mudmen Awakened', player)),
		],
		'Dimensional Corridor [Grail]': [
			LaMulanaNPCDoor(get_entrance_checks('Philosopher Fobos'), lambda state: state.has('Left Side Children Defeated', player)),
		],
		'Gate of Time [Surface]': [
			LaMulanaNPCDoor(get_entrance_checks('8-bit Elder'))
		]
	}

	if is_option_enabled(world, player, "RandomizeDracuetsShop"):
		npc_doors['Hell Temple [Shop]'] = [
			LaMulanaNPCDoor(get_entrance_checks('Tailor Dracuet'))
		]

	return npc_doors

npc_hint_order = ['Elder Xelpud', 'Mulbruk', 'Fairy Queen', 'Philosopher Fobos', 'Philosopher Alsedana', 'Philosopher Giltoriyo', 'Philosopher Samaranta', 'Former Mekuri Master', 'Mr. Slushfund', 'Priest Alest', 'Nebur', 'Sidro', 'Modro', 'Penadvent of Ghost', 'Greedy Charlie', 'Shalom III', 'Usas VI', 'Kingvalley I', 'Mr. Fishman (Original)', 'Mr. Fishman (Alt)', 'Hot-blooded Nemesistwo', 'Operator Combaker', 'Yiegah Kungfu', 'Yiear Kungfu', 'Arrogant Sturdy Snake', 'Arrogant Metagear', 'Affected Knimare', 'Mover Athleland', 'Giant Mopiran', 'Kingvalley II', 'Energetic Belmont', 'Mechanical Efspi', 'Mudman Qubert', 'Tailor Dracuet']

def get_npc_entrance_room_names() -> Dict[str,str]:
	return {
		'Elder Xelpud': 'Surface - Village of Departure (Xelpud)',
		'Nebur': 'Surface - Village of Departure (Nebur)',
		'Sidro': 'Surface - Village of Departure (Sidro)',
		'Modro': 'Surface - Village of Departure (Modro)',
		'Moger': 'Surface - Village of Departure (Moger)',
		'Hiner': 'Surface - Altar Hill',
		'Former Mekuri Master': 'Surface - Bahrun\'s Waterfall',
		'Priest Zarnac': 'Gate of Guidance - Pit of the Holy Grail',
		'Penadvent of Ghost': 'Gate of Guidance - Monument of Time',
		'Priest Xanado': 'Mausoleum of the Giants - Room of Redemption',
		'Greedy Charlie': 'Mausoleum of the Giants - Monument to Hermes',
		'Mulbruk': 'Temple of the Sun - Thoth\'s Room',
		'Shalom III': 'Temple of the Sun - Altar of War',
		'Usas VI': 'Temple of the Sun - Sanctuary',
		'Kingvalley I': 'Temple of the Sun - Horus\' Room of Pillars',
		'Priest Madomo': 'Temple of the Sun - Great Colonnade, Right-side room',
		'Priest Hidlyda': 'Spring in the Sky - Mirror Waterfall',
		'Philosopher Giltoriyo': 'Spring in the Sky - Mural of Oannes',
		'Mr. Fishman (Original)': 'Spring in the Sky - Waterfall Approach',
		'Mr. Fishman (Alt)': 'Spring in the Sky - Waterfall Approach (Key Fairy)',
		'Priest Gailious': 'Inferno Cavern - Pit of Fire',
		'Hot-blooded Nemesistwo': 'Inferno Cavern - Anterior Chamber',
		'Priest Romancis': 'Inferno Cavern - Pazuzu\'s Room',
		'Priest Aramo': 'Chamber of Extinction - Mural of Light',
		'Priest Triton': 'Chamber of Extinction - Palenque\'s Coffin',
		'Operator Combaker': 'Chamber of Extinction - Shiva\'s Crucifix',
		'Yiegah Kungfu': 'Twin Labyrinths - Twin\'s Surrounding Wall (Little Brother)',
		'Yiear Kungfu': 'Twin Labyrinths - Twin\'s Surrounding Wall (Big Brother)',
		'Arrogant Sturdy Snake': 'Twin Labyrinths - Treasury (Right)',
		'Arrogant Metagear': 'Twin Labyrinths - Treasury (Left)',
		'Priest Jaguarfiv': 'Twin Labyrinths - Sanctuary',
		'Fairy Queen': 'Endless Corridor - First Endless Corridor (Fairy Queen)',
		'Affected Knimare': 'Endless Corridor - First Endless Corridor (Seal)',
		'duplex': 'Gate of Illusion - Chi You\'s Room',
		'Mr. Slushfund': 'Gate of Illusion - Sacred Lake of the Sky (Mr. Slushfund)',
		'Priest Alest': 'Gate of Illusion - Sacred Lake of the Sky (Mini Doll)',
		'Mover Athleland': 'Gate of Illusion - Lizard\'s Room',
		'Giant Mopiran': 'Graveyard of the Giants - First Tomb',
		'Giant Thexde': 'Graveyard of the Giants - Anterior Chamber',
		'Philosopher Alsedana': 'Temple of Moonlight - Moon Watchtower',
		'Samieru': 'Temple of Moonlight - Serdab of Power',
		'Kingvalley II': 'Temple of Moonlight - Serdab of Treasure',
		'Philosopher Samaranta': 'Tower of the Goddess - Scales of the Heart',
		'Naramura': 'Tower of the Goddess - Skuld\'s Tower',
		'Energetic Belmont': 'Tower of the Goddess - Verdandi\'s Tower',
		'Priest Laydoc': 'Tower of Ruin - Fountain of Heat',
		'Mechanical Efspi': 'Tower of Ruin - One Who Reads Tablets',
		'Priest Ashgine': 'Chamber of Birth - Brahma\'s Room',
		'Mudman Qubert': 'Chamber of Birth - Brahma\'s Room (Mudman Qubert)',
		'Philosopher Fobos': 'Dimensional Corridor - Kuusarikku\'s Room',
		'8-bit Elder': 'Gate of Time - 8-bit Surface',
		'Tailor Dracuet': 'Hell Temple - Room 14'
	}