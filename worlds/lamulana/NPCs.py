from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location, CollectionState
from .Options import is_option_enabled
from .Locations import LocationData
from .LogicShortcuts import LaMulanaLogicShortcuts

class LaMulanaNPC(NamedTuple):
	name: str
	region: str
	room_name: str
	logic: Callable[CollectionState,bool] = lambda state: True
	checks: List[LocationData] = []

def spring_npc(state: CollectionState, player: int, s: LaMulanaLogicShortcuts) -> bool:
	can_escape = s.state_shield(state) or s.attack_shuriken(state) or s.attack_flare_gun(state) or s.attack_caltrops(state) or state.has_any({'Leather Whip', 'Chain Whip', 'Flail Whip', 'Axe', 'Holy Grail'}, player)
	if not can_escape:
		return False
	if s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_caltrops(state) or s.attack_flare_gun(state) or state.has_any({'Knife', 'Axe', 'Katana'}, player):
		return True
	return state.has_any({'Helmet', 'Scalesphere', 'Sacred Orb'}, player) and state.has_any({'Leather Whip', 'Chain Whip', 'Flail Whip', 'Key Sword'}, player)

def get_npcs(world: MultiWorld, player: int, s: LaMulanaLogicShortcuts):
	npc_list = [
		LaMulanaNPC('Elder Xelpud', 'Surface [Main]', lambda state: True, [
				LocationData('NPC: Xelpud', 1, state: lambda: True, True),
				LocationData('Xelpud xmailer.exe Gift', 1),
				LocationData('Xelpud Mulana Talisman Gift', 1, lambda state: state.has('Diary', player))
			]),
		LaMulanaNPC('Nebur', 'Surface [Main]', '', lambda state: state.has('NPC: Xelpud', player), [
				LocationData('Nebur Shop Item 1', 1),
				LocationData('Nebur Shop Item 2', 1),
				LocationData('Nebur Shop Item 3', 1),
				LocationData('Nebur Shop Item - 4 Guardians', 1, lambda state: s.guardian_count(state) >= 4)
			]),
		LaMulanaNPC('Sidro', 'Surface [Main]', '', lambda state: state.has('NPC: Xelpud', player), [
				LocationData('Sidro Shop Item 1', 1),
				LocationData('Sidro Shop Item 2', 1),
				LocationData('Sidro Shop Item 3', 1)
			]),
		LaMulanaNPC('Modro', 'Surface [Main]', '', lambda state: state.has('NPC: Xelpud', player), [
				LocationData('Modro Shop Item 1', 1),
				LocationData('Modro Shop Item 2', 1),
				LocationData('Modro Shop Item 3', 1)
			]),
		LaMulanaNPC('Hiner', 'Surface [Main]', '', lambda state: state.has("NPC: Xelpud", player)),
		LaMulanaNPC('Moger', 'Surface [Main]', '', lambda state: state.has("NPC: Xelpud", player)),
		LaMulanaNPC('Former Mekuri Master', 'Surface [Main]', '', lambda state: s.attack_far(state) or s.attack_s_straight(state) or s.attack_earth_spear(state) or state.has("Katana", player), [
				LocationData('Former Mekuri Master mekuri.exe Gift', 1)
			]),
		LaMulanaNPC('Priest Zarnac', 'Gate of Guidance [Main]', ''),
		LaMulanaNPC('Penadvent of Ghost', 'Gate of Guidance [Main]', '', lambda state: True, [
				LocationData('Penadvent of Ghost Shop Item 1', 1),
				LocationData('Penadvent of Ghost Shop Item 2', 1),
				LocationData('Penadvent of Ghost Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Xanado', 'Mausoleum of the Giants', 'Mausoleum of the Giants (Room of Redemption)'),
		LaMulanaNPC('Greedy Charlie', 'Mausoleum of the Giants', '', lambda state: s.attack_chest_any(state), [
				LocationData('Greedy Charlie Shop Item 1', 1),
				LocationData('Greedy Charlie Shop Item 2', 1),
				LocationData('Greedy Charlie Shop Item 3', 1)
			]),
		#You don't need to awaken Mulbruk to escape, but oh well
		LaMulanaNPC('Mulbruk', 'Temple of the Sun [Main]', lambda state: s.boss_count(state) >= 1 and state.has('Origin Seal'), [
				LocationData('NPC: Mulbruk', 1, lambda state: True, True),
				LocationData('Mulbruk Book of the Dead Gift', 1, lambda state: state.can_reach('Temple of Moonlight [Southeast]'))
			]),
		LaMulanaNPC('Shalom III', 'Temple of the Sun [Main]', '', lambda state: s.attack_shuriken(state) or s.attack_bomb(state) or s.glitch_catpause(state) or (state.has('Feather', player) and (s.attack_forward(state) or s.attack_chakram(state))), [
				LocationData('Shalom III Shop Item 1', 1),
				LocationData('Shalom III Shop Item 2', 1),
				LocationData('Shalom III Shop Item 3', 1)
			]),
		LaMulanaNPC('Usas VI', 'Temple of the Sun [Main]', '', lambda state: True, [
				LocationData('Usas VI Shop Item 1', 1),
				LocationData('Usas VI Shop Item 2', 1),
				LocationData('Usas VI Shop Item 3', 1)
			]),
		LaMulanaNPC('Kingvalley I', 'Temple of the Sun [Main]', '', lambda state: state.has_all({'Feather', 'Death Seal'}, player), [
				LocationData('Kingvalley I Shop Item 1', 1),
				LocationData('Kingvalley I Shop Item 2', 1),
				LocationData('Kingvalley I Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Madomo', 'Temple of the Sun [Sphinx]', ''),
		LaMulanaNPC('Priest Hidlyda', 'Spring in the Sky [Main]', '', lambda state: spring_npc(state, player, s)),
		LaMulanaNPC('Philosopher Giltoriyo', 'Spring in the Sky [Main]', 'Spring in the Sky (Mural of Oannes)', lambda state: True, [
				LocationData('NPC: Philosopher Giltoriyo', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
			]),
		LaMulanaNPC('Mr. Fishman (Original)', 'Spring in the Sky [Upper]', '', lambda state: state.has_all({'Helmet', 'Origin Seal'}, player), [
				LocationData('Mr. Fishman (Original) Shop Item 1', 1),
				LocationData('Mr. Fishman (Original) Shop Item 2', 1),
				LocationData('Mr. Fishman (Original) Shop Item 3', 1)
			]),
		LaMulanaNPC('Mr. Fishman (Alt)', 'Spring in the Sky [Upper]', '', lambda state: state.has_all({'Helmet', 'Origin Seal'}) and s.state_key_fairy_access(state), [
				LocationData('Mr. Fishman (Alt) Shop Item 1', 1),
				LocationData('Mr. Fishman (Alt) Shop Item 2', 1),
				LocationData('Mr. Fishman (Alt) Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Gailious', 'Inferno Cavern [Main]', ''),
		LaMulanaNPC('Hot-blooded Nemesistwo', 'Inferno Cavern [Main]', '', lambda state: s.attack_chest_any(state), [
				LocationData('Hot-blooded Nemesistwo Shop Item 1', 1),
				LocationData('Hot-blooded Nemesistwo Shop Item 2', 1),
				LocationData('Hot-blooded Nemesistwo Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Romancis', 'Inferno Cavern [Pazuzu]', ''),
		LaMulanaNPC('Priest Aramo', 'Chamber of Extinction [Main]', '', lambda state: s.attack_chest_any(state)),
		LaMulanaNPC('Priest Triton', 'Chamber of Extinction [Ankh Lower]', '', lambda state: state.has('Feather', player)),
		LaMulanaNPC('Operator Combaker', 'Chamber of Extinction [Ankh Lower]', '', lambda state: s.attack_chest_any(state), [
				LocationData('Operator Combaker Shop Item 1', 1),
				LocationData('Operator Combaker Shop Item 2', 1),
				LocationData('Operator Combaker Shop Item 3', 1)
			]),
		LaMulanaNPC('Yiegah Kungfu', 'Twin Labyrinths [Loop]', '', lambda state: True, [
				LocationData('Yiegah Kungfu Shop Item 1', 1),
				LocationData('Yiegah Kungfu Shop Item 2', 1),
				LocationData('Yiegah Kungfu Shop Item 3', 1),
				LocationData('NPC: Yiegah Kungfu', 1, lambda state: True, True)
			]),
		LaMulanaNPC('Yiear Kungfu', 'Twin Labyrinths [Loop]', '', lambda state: state.has('NPC: Yiegah Kungfu', player), [
				LocationData('Yiear Kungfu Shop Item 1', 1),
				LocationData('Yiear Kungfu Shop Item 2', 1),
				LocationData('Yiear Kungfu Shop Item 3', 1)
			]),
		LaMulanaNPC('Arrogant Sturdy Snake', 'Twin Labyrinths [Lower]', '', lambda state: state.has('Feather', player), [
				LocationData('Arrogant Sturdy Snake Shop Item 1', 1),
				LocationData('Arrogant Sturdy Snake Shop Item 2', 1),
				LocationData('Arrogant Sturdy Snake Shop Item 3', 1)
			]),
		LaMulanaNPC('Arrogant Metagear', 'Twin Labyrinths [Lower]', '', lambda state: (state.has('Feather', player) and s.attack_bomb(state)) or s.glitch_raindrop(state), [
				LocationData('Arrogant Metagear Shop Item 1', 1),
				LocationData('Arrogant Metagear Shop Item 2', 1),
				LocationData('Arrogant Metagear Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Jaguarfiv', 'Twin Labyrinths [Poseidon]', ''),
		LaMulanaNPC('Fairy Queen', 'Endless Corridor [1F]', '', lambda state: True, [
				LocationData('NPC: Fairy Queen', 1, lambda state: True, True)
			]),
		LaMulanaNPC('Affected Knimare', 'Endless Corridor [1F]', '', lambda state: state.has('Origin Seal', player), [
				LocationData('Affected Knimare Shop Item 1', 1),
				LocationData('Affected Knimare Shop Item 2', 1),
				LocationData('Affected Knimare Shop Item 3', 1)
			]),
		LaMulanaNPC('duplex', 'Gate of Illusion [Grail]', '', lambda state: state.has('Chi You Defeated', player) and s.attack_forward(state) and s.combo_dev_npcs(state)),
		LaMulanaNPC('Mr. Slushfund', 'Gate of Illusion [Dracuet]', '', lambda state: s.attack_chest(state), [
				LocationData('Mr. Slushfund Pepper Gift', 1),
				LocationData('Mr. Slushfund Anchor Gift', 1, lambda state: state.has('Treasures', player))
			]),
		LaMulanaNPC('Priest Alest', 'Gate of Illusion [Dracuet]', '', lambda state: s.attack_chest(state) and state.has('Anchor', player), [
				LocationData('Priest Alest Mini Doll Gift', 1)
			]),
		LaMulanaNPC('Mover Athleland', 'Gate of Illusion [Middle]', '', lambda state: True, [
				LocationData('Mover Athleland Shop Item 1', 1),
				LocationData('Mover Athleland Shop Item 2', 1),
				LocationData('Mover Athleland Shop Item 3', 1)
			]),
		LaMulanaNPC('Giant Mopiran', 'Graveyard of the Giants [West]', '', lambda state: True, [
				LocationData('Giant Mopiran Shop Item 1', 1),
				LocationData('Giant Mopiran Shop Item 2', 1),
				LocationData('Giant Mopiran Shop Item 3', 1)
			]),
		LaMulanaNPC('Giant Thexde', 'Graveyard of the Giants [East]', '', lambda state: state.has('Feather', player)),
		LaMulanaNPC('Philosopher Alsedana', 'Temple of Moonlight [Pyramid]', '', lambda state: True, [
				LocationData('NPC: Philosopher Alsedana', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
			]),
		LaMulanaNPC('Samieru', 'Temple of Moonlight [Upper]', '', lambda state: s.combo_dev_npcs(state) and ((s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state)))) and (s.attack_below(state) or s.attack_bomb(state) or s.attack_earth_spear(state) or s.attack_rolling_shuriken(state)))
		LaMulanaNPC('Kingvalley II', 'Temple of Moonlight [Southeast]', '', lambda state: s.attack_bomb(state) or (s.glitch_catpause(state) and s.attack_forward(state)), [
				LocationData('Kingvalley II Shop Item 1', 1),
				LocationData('Kingvalley II Shop Item 2', 1),
				LocationData('Kingvalley II Shop Item 3', 1)
			]),
		LaMulanaNPC('Philosopher Samaranta', 'Tower of the Goddess [Lower]', lambda state: state.has('Flooded Tower of the Goddess', player), [
				LocationData('NPC: Philosopher Samaranta', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
			]),
		LaMulanaNPC('Naramura', 'Tower of the Goddess [Lower]', lambda state: s.combo_dev_npcs(state)),
		LaMulanaNPC('Energetic Belmont', 'Tower of the Goddess [Lower]', '', lambda state: ((state.has('Flooded Tower of the Goddess', player) and s.state_lamp(state)) or (s.glitch_raindrop(state) and state.has('Feather', player))) and state.has_any({'Anchor', 'Holy Grail'}, player), [
				LocationData('Energetic Belmont Shop Item 1', 1),
				LocationData('Energetic Belmont Shop Item 2', 1),
				LocationData('Energetic Belmont Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Laydoc', 'Tower of Ruin [Southwest]', ''),
		LaMulanaNPC('Mechanical Efspi', 'Tower of Ruin [Grail]', '', lambda state: state.has_any({'Feather', 'Grapple Claw'}, player) and (s.attack_below(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_rolling_shuriken(state) or s.attack_caltrops(state)), [
				LocationData('Mechanical Efspi Shop Item 1', 1),
				LocationData('Mechanical Efspi Shop Item 2', 1),
				LocationData('Mechanical Efspi Shop Item 3', 1)
			]),
		LaMulanaNPC('Priest Ashgine', 'Chamber of Birth [West]', ''),
		LaMulanaNPC('Mudman Qubert', 'Chamber of Birth [West]', '', lambda state: state.has('Mudmen Awakened', player), [
				LocationData('Mudman Qubert Shop Item 1', 1),
				LocationData('Mudman Qubert Shop Item 2', 1),
				LocationData('Mudman Qubert Shop Item 3', 1)
			]),
		LaMulanaNPC('Philosopher Fobos', 'Dimensional Corridor [Grail]', lambda state: state.has('Left Side Children Defeated'), [
				LocationData('NPC: Philosopher Fobos', 1, lambda state: state.has("Philosopher's Ocarina", player), True)
			])
		LaMulanaNPC('8-bit Elder', 'Gate of Time [Surface]', ''),
	]

	if is_option_enabled(world, player, "RandomizeDracuetsShop"):
		npc_list.append(
			LaMulanaNPC('Tailor Dracuet', 'Hell Temple [Shop]', '', lambda state: True, [
					LocationData('Tailor Dracuet Shop Item 1', 1),
					LocationData('Tailor Dracuet Shop Item 2', 1),
					LocationData('Tailor Dracuet Shop Item 3', 1)
				])
			)

	return npc_list