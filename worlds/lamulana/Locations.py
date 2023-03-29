from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location, CollectionState
from .Options import is_option_enabled
from .LogicShortcuts import LaMulanaLogicShortcuts
from .CombatLogic import LaMulanaCombatLogic

class LocationData(NamedTuple):
	name: str
	code: Optional[int]
	logic: Callable[[CollectionState, int], bool] = lambda state: True
	is_event: bool = False

#4 vanilla cursed chests
cursed_chests = ['Crystal Skull Chest', 'Dimensional Key Chest']

def roll_cursed_chests(world: MultiWorld, include_coin_chests: bool, include_trap_items: bool) -> None:
	possible_cursed_chests = ['Birth Seal Chest', 'Feather Chest', 'Sacred Orb (Surface) Chest', 'Shell Horn Chest', 'Ankh Jewel (Gate of Guidance) Chest', 'Crucifix Chest', 'Sacred Orb (Gate of Guidance) Chest', '']
	if include_coin_chests:
		possible_cursed_chests.extend([])
	if include_trap_items:
		possible_cursed_chests.extend(['Graveyard of the Giants Trap Chest', 'Gate of Illusion Trap Chest'])
	cursed_chests = world.random.choices(possible_cursed_chests, k=4)

def get_locations_by_region(world: MultiWorld, player: int, s: LaMulanaLogicShortcuts) -> Dict[str, List[LocationData]]:
	combat = LaMulanaCombatLogic(world, player, s)
	
	include_coin_chests = is_option_enabled(world, player, "RandomizeCoinChests")
	include_trap_items = is_option_enabled(world, player, "RandomizeTrapItems")
	if is_option_enabled(world, player, "RandomizeCursedChests"):
		roll_cursed_chests(world, include_coin_chests, include_trap_items)

	locations = {
		"Surface [Main]": [
			LocationData("Birth Seal Chest", 1, lambda state: s.attack_chest(state) and state.has_all({"Origin Seal", "Helmet"}, player) and state.has_any({"Hermes' Boots", "Feather", "Bahamut Defeated"}))
			LocationData("deathv.exe Location", 1, lambda state: s.attack_forward(state) and (state.has("NPC: Xelpud", player) or s.glitch_raindrop(state))),
			LocationData("Feather Chest", 1, lambda state: s.attack_chest(state) and state.has("Argus Defeated", player)),
			LocationData("Map (Surface) Location", 1, lambda state: state.has("Hand Scanner", player)),
			LocationData("Sacred Orb (Surface) Chest", 1, lambda state: state.has("Helmet", player) and state.has_any({"Hermes' Boots", "Bahamut Defeated"}, player) and (attack_above(state) or attack_shuriken(state) or attack_chakram(state) or attack_bomb(state) or attack_pistol(state) or (attack_s_above(state) and attack_chest(state)) or (attack_rolling_shuriken(state) and state.has("Bahamut Defeated", player)))),
			LocationData("Shell Horn Chest", 1, lambda state: s.attack_chest(state)),
			LocationData("Argus Defeated", 1, lambda state: state.has("Serpent Staff", player) and combat.argus(state), True),
			LocationData("Surface Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Gate of Guidance [Main]": [
			LocationData("Ankh Jewel (Gate of Guidance) Chest", 1, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state)),
			LocationData("Crucifix Chest", 1, lambda state: s.attack_flare_gun(state) and s.attack_chest(state) and state.has("Life Seal", player)),
			LocationData("Holy Grail Chest", 1, lambda state: s.attack_chest(state)),
			LocationData("Map (Gate of Guidance) Chest", 1, lambda state: s.attack_chest(state)),
			LocationData("Sacred Orb (Gate of Guidance) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Shuriken Location", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Treasures Chest", 1, lambda state: s.attack_chest_any(state) and state.has("Pepper", player)),
			LocationData("Gate of Guidance Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Gate of Guidance [Door]": [
			LocationData("yagostr.exe Chest", 1, lambda state: s.attack_chest(state))
		],
		"Mausoleum of the Giants": [
			LocationData("Ankh Jewel (Mausoleum of the Giants) Chest", 1, lambda state: s.attack_chest(state)),
			LocationData("Map (Mausoleum of the Giants) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Rolling Shuriken Location", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Sacred Orb (Mausoleum of the Giants) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Mausoleum of the Giants Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Temple of the Sun [Main]": [
			LocationData("Ankh Jewel (Temple of the Sun) Chest", 1, lambda state: attack_chest(state)),
			LocationData("Knife Location", 1, lambda state: attack_shuriken(state) or (attack_chakram(state) and state.has_any({"Feather", "Grapple Claw"}, player)) or attack_bomb(state) or (attack_flare_gun(state) and attack_forward(state) and state.has("Feather", player)) or glitch_catpause(state)),
			LocationData("Sacred Orb (Temple of the Sun) Chest", 1, lambda state: attack_chest_any(state))
		],
		"Temple of the Sun [West]": [
			LocationData("Isis' Pendant Chest", 1, lambda state: state.has("Buer Defeated", player) and s.state_literacy(state) and s.state_mobility(state) and (s.attack_above(state) or s.attack_s_above(state)))
			LocationData("Buer Defeated", 1, lambda state: combat.buer(state), True)
		],
		"Temple of the Sun [East]": [
			LocationData("Bronze Mirror Chest", 1, lambda state: ???),
			LocationData("Talisman Location", 1, lambda state: state.has("Viy Defeated", player))
		],
		"Temple of the Sun [Top Entrance]": [
			#Simplified other logic options to "Can climb watchtower" (attack-forward or flares)
			LocationData("Map (Temple of the Sun) Chest", 1, lambda state: s.attack_chest(state) and s.sun_watchtower(state)),
			LocationData("Temple of the Sun Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Spring in the Sky [Main]": [
			LocationData("Caltrops Location", 1),
			LocationData("Map (Spring in the Sky) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Sacred Orb (Spring in the Sky)", 1, lambda state: s.attack_chest_any(state) and state.has("Birth Seal", player)),
			LocationData("Spring in the Sky Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Spring in the Sky [Upper]": [
			LocationData("Glove Chest", 1, lambda state: state.has("Flooded Spring in the Sky", player) and s.attack_chest_any(state)),
			LocationData("Origin Seal Chest", 1, lambda state: state.has_all({"Helmet", "Nuckelavee Defeated"}, player) and (s.attack_forward(state) or (state.has("Feather", player) and s.attack_earth_spear(state)))),
			LocationData("Scalesphere Chest", 1, lambda state: s.attack_chest(state) and state.has("Helmet", player)),
			LocationData("Nuckelavee Defeated", 1, lambda state: state.has("Helmet", player) and combat.nuckelavee(state), True),
			LocationData("Flooded Spring in the Sky", 1, lambda state: state.has_all({"Helmet", "Origin Seal"}, player), True)
		],
		"Inferno Cavern [Main]": [
			LocationData("bunplus.exe Location", 1, lambda state: s.attack_forward(state)),
			LocationData("Flare Gun Location", 1, lambda state: s.attack_forward(state)),
			LocationData("Ice Cape Chest", 1, lambda state: s.attack_chest(state)),
			LocationData("Map (Inferno Cavern) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("Inferno Cavern Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Inferno Cavern [Pazuzu]": [
			LocationData("Chain Whip Location", 1, lambda state: state.has("Pazuzu Defeated", player)),
			LocationData("Pazuzu Defeated", 1, lambda state: combat.pazuzu(state), True),
		],
		"Chamber of Extinction [Main]": [
			LocationData("Chakram Location", 1, lambda state: s.state_extinction_light(state) and (state.has("Centimani Defeated", player) or s.glitch_catpause(state))),
			LocationData("Life Seal Chest", 1, lambda state: s.state_extinction_light(state) and s.attack_chest(state) and state.has("Birth Seal", player)),
			LocationData("mantra.exe Scan", 1, lambda state: s.attack_flare_gun(state) and state.has_all({"Magatama Jewel", "torude.exe", "Ox-head & Horse-face Defeated"})),
			LocationData("Sacred Orb (Chamber of Extinction) Chest", 1, lambda state: s.state_extinction_light(state) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player)))),
			LocationData("Centimani Defeated", 1, lambda state: s.state_extinction_light(state) and combat.centimani(state), True),
			LocationData("Chamber of Extinction Grail Tablet", 1, lambda state: s.state_extinction_light(state) and s.state_read_grail(state), True)
		],
		"Chamber of Extinction [Map]": [
			LocationData("Map (Chamber of Extinction) Chest", 1, lambda state: s.state_extinction_light(state) and s.attack_chest_any(state))
		],
		"Chamber of Extinction [Magatama]": [
			LocationData("Ox-head & Horse-face Defeated", 1, lambda state: combat.oxhead_horseface(state), True)
		],
		"Twin Labyrinths [Loop]": [
			LocationData("Ring Location", 1, lambda state: s.glitch_raindrop(state))
		],
		"Twin Labyrinths [Jewel]": [
			LocationData("Ankh Jewel (Twin Labyrinths) Chest", 1, lambda state: state.can_reach("Twin Labyrinths [Lower]", "Region", player) and state.can_reach("Twin Labyrinths [Upper Left]", "Region", player) and s.attack_flare_gun(state) and s.attack_chest(state))
		],
		"Twin Labyrinths [Katana]": [
			LocationData("Katana Location", 1, lambda state: state.has_all({"Peryton Defeated", "Twin Statue"}, player) or s.glitch_catpause(event))
		],
		"Twin Labyrinths [Poison 1]": [
			LocationData("Map (Twin Labyrinths) Chest", 1, lambda state: state.has("Twin Poison Cleared") and s.attack_forward(state)),
			LocationData("Twin Poison Cleared", 1, lambda state: state.has("Twin Statue") or state.can_reach("Twin Labyrinths [Poison 2]", "Region", player), True)
		],
		"Twin Labyrinths [Poison 2]": [],
		"Twin Labyrinths [Upper Left]": [
			LocationData("Ring Location", 1, lambda state: True)
		],
		"Twin Labyrinths [Upper Grail]": [
			LocationData("Twin Labyrinths (Front) Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Twin Labyrinths [Lower]": [
			LocationData("Sacred Orb (Twin Labyrinths) Chest", 1, lambda state: s.attack_chest(state) and (state.has("Zu Defeated", player) or s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has("Holy Grail", player)))),
			LocationData("Zu Defeated", 1, lambda state: combat.zu(state), True),
			LocationData("Peryton Defeated", 1, lambda state: combat.peryton(state), True),
			LocationData("Twin Labyrinths (Back) Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Endless Corridor [1F]": [
			LocationData("Map (Endless Corridor) Chest", 1, lambda state: s.attack_chest_any(state)) #TODO Depends on entrance randomizer - if Skanda or Illusion, also need to account for those
		],
		"Endless Corridor [2F]": [
			LocationData("Key Sword Location", 1, lambda state: attack_chest(state))
		],
		"Endless Corridor [3F Upper]": [
			LocationData("Twin Statue Chest", 1, lambda state: attack_chest_any(state) and (state.has("Holy Grail", player) or glitch_raindrop(state) or (state.has("Key of Eternity", player) and (attack_forward(state) or (state.has("Feather", player) and (attack_flare_gun(state) or attack_earth_spear(state)))))))
		],
		"Endless Corridor [5F]": [
			LocationData("Backbeard & Tai Sui Defeated", 1, lambda state: s.state_literacy(state) and combat.backbeard_tai_sui(state), True)
		],
		"Shrine of the Mother [Main]": [
			LocationData("bounce.exe Chest", 1, lambda state: attack_shuriken(state) or attack_rolling_shuriken(state) or attack_earth_spear(state) or attack_bomb(state) or attack_chakram(state) or attack_caltrops(state) or attack_pistol(state) or (attack_flare_gun(state) and state.has("Removed Shrine Skulls", player))),
			LocationData("Crystal Skull Chest", 1, lambda state: attack_chest(state) and state.has_all({"Life Seal", "Removed Shrine Skulls"}, player)),
			LocationData("Diary Chest", 1, lambda state: attack_chest(state) and state.has_all({"Removed Shrine Skulls", "Talisman", "NPC: Xelpud"}, player)),
			LocationData("Sacred Orb (Shrine of the Mother) Chest", 1, lambda state: attack_chest(state) and state.has_all({"Origin Seal", "Birth Seal", "Life Seal", "Death Seal"}, player)),
			#Normal shrine grail tablet doesn't matter, I think - only true shrine
		],
		"Shrine of the Mother [Seal]": [
			LocationData("Death Seal Chest", 1, lambda state: s.attack_chest(state) and ((state.has_all("Feather", player) and self.s.boss_count(state) >= 8) or (state.has_any({"Feather", "Grapple Claw"}, player) and (s.glitch_raindrop(state) or state.has("Removed Shrine Skulls", player)))))
		],
		"Shrine of the Mother [Map]": [
			LocationData("Map (Shrine of the Mother) Chest", 1, lambda state: s.attack_chest_any(state))
		],
		'Gate of Illusion [Eden]': [
			LocationData("Illusion Unlocked", 1, lambda state: state.has('Fruit of Eden', self.player), True)
		],
		"Gate of Illusion [Upper]": [
			LocationData("Cog of the Soul Chest", 1, lambda state: s.state_literacy(state) and state.can_reach("Gate of Illusion [Pot Room]", "Region", player) and state.can_reach("Gate of Illusion [Middle]", "Region", player) and s.state_lamp(state) and state.has_all({"Feather", "Ba Defeated"}, player) and s.attack_forward(state)),
			LocationData("Mudmen Awakened", 1, lambda state: state.has_all({"Feather", "Cog of the Soul"}, player) and s.attack_forward(state), True),
			LocationData("Ba Defeated", 1, lambda state: s.state_literacy(state) and state.has("Feather", player) and combat.ba(state), True)
		],
		"Gate of Illusion [Middle]": [
			LocationData("Fairy Clothes Chest", 1, lambda state: s.state_key_fairy_access(state) and s.attack_below(state))
		],
		"Gate of Illusion [Grail]": [
			LocationData("Key of Eternity Chest", 1, lambda state: s.attack_chest(state) and state.has("Chi You Defeated", player)),
			LocationData("Gate of Illusion Grail Tablet", lambda state: s.state_read_grail(state), True),
			LocationData("Chi You Defeated", lambda state: (s.glitch_raindrop(state) or (state.can_reach("Mausoleum of the Giants", "Region", player) and state.has("Mini Doll", player) and s.state_literacy(state))) and (state.has("Birth Seal", player) or s.glitch_lamp(state)) and combat.chi_you(state))
		],
		"Gate of Illusion [Dracuet]": [
			LocationData("Map (Gate of Illusion) Chest", 1, lambda state: s.attack_forward(state))
		],
		"Graveyard of the Giants [West]": [
			LocationData("Gauntlet Chest", 1, lambda state: s.attack_chest_any(state) and state.has_all({"Feather", "Life Seal"}, player)),
			LocationData("Map (Graveyard of the Giants) Chest", 1, lambda state: s.attack_chest_any(state)),
			LocationData("mirai.exe Chest", 1, lambda state: s.attack_chest(state) and state.has("Feather", player)),
			LocationData("Silver Shield Location", 1, lambda state: s.attack_below(state))
		],
		"Graveyard of the Giants [Grail]": [
			LocationData("Graveyard of the Giants Grail Tablet", lambda state: s.state_read_grail(state), True)
		],
		"Graveyard of the Giants [East]": [
			LocationData("Bomb Location", 1, lambda state: state.has_all({"Feather", "Kamaitachi Defeated"}, player)),
			LocationData("emusic.exe Scan", 1, lambda state: s.attack_bomb(state) and state.has("torude.exe", player)),
			LocationData("Kamaitachi Defeated", 1, lambda state: state.has("Feather", player) and combat.kamaitachi(state), True)
		],
		"Temple of Moonlight [Upper]": [
			LocationData('Axe Location', 1, lambda state: (s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state))))
			LocationData("Fruit of Eden Chest", 1, lambda state: s.attack_chest_any(state) and state.has("Hand Scanner", player) and state.can_reach("Temple of Moonlight [Lower]", "Region", player) and state.can_reach("Temple of Moonlight [Grapple]", "Region", player) and state.can_reach("Temple of Moonlight [Southeast]", "Region", player))
		],
		"Temple of Moonlight [Grapple]": [
			LocationData("Grapple Claw Chest", 1, lambda state: s.attack_chest(state))
		],
		"Temple of Moonlight [Map]": [
			LocationData("Map (Temple of Moonlight) Chest", 1, lambda state: s.attack_chest_any(state))
		],
		"Temple of Moonlight [Pyramid]": [
			#Not a real chest, so cannot be cursed
			LocationData("Philosopher's Ocarina Chest", 1, lambda state: state.has("Maternity Statue", player) and (state.has("Feather", player) or s.glitch_raindrop(state)))
		],
		"Temple of Moonlight [Southeast]": [
			LocationData("Serpent Staff Chest", 1, lambda state: s.attack_chest(state) and state.has("Anubis Defeated", player)),
			LocationData("Anubis Defeated", 1, lambda state: state.has("Book of the Dead", player) and (state.has("Birth Seal", player) or s.glitch_raindrop(state)) and combat.anubis(state), True)
		],
		"Tower of the Goddess [Lower]": [
			LocationData("Eye of Truth Chest", 1, lambda state: s.attack_chest_any(state) and state.can_reach("Tower of the Goddess [Lamp]", "Region", player) and state.has("Flooded Tower of the Goddess", player)),
			LocationData("Flail Whip Location", 1, lambda state: (s.state_literacy(state) or s.glitch_catpause(state)) and (s.glitch_lamp(state) or state.has('NPC: Philosopher Samaranta', player))),
			LocationData("Map (Tower of the Goddess) Chest", 1, lambda state: s.attack_forward(state)),
			LocationData("Flooded Tower of the Goddess", 1, lambda state: state.has("Flooded Spring in the Sky", player) and s.state_literacy(state) and (s.attack_caltrops(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or state.has_any({"Knife", "Katana"}, player)) and (state.has_any({"Holy Grail", "Scalesphere", "Sacred Orb"}, player)), True)
		],
		"Tower of the Goddess [Grail]": [
			LocationData("Plane Model Chest", 1, lambda state: state.has_all({"Eye of Truth", "Vimana Defeated"}, player) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player))) and state.can_reach("Tower of the Goddess [Spaulder]", "Region", player) and state.can_reach("Tower of the Goddess [Lower]", "Region", player)),
			LocationData("Spaulder Chest", 1, lambda state: s.state_key_fairy_access(state) and s.attack_forward(state) and (state.has_all({"Holy Grail", "mirai.exe"}, player)) or state.has_all({"Feather", "Hermes' Boots"}, player)),
			LocationData("Vimana Defeated", 1, lambda state: state.has("Flooded Tower of the Goddess", player) and combat.vimana(state), True)
		],
		"Tower of Ruin [Southeast]": [
			LocationData("Sacred Orb (Tower of Ruin) Chest", 1, lambda state: s.attack_chest_any(state))
		],
		"Tower of Ruin [Southwest]": [
			LocationData("Ankh Jewel (Tower of Ruin) Chest", 1, lambda state: (state.has("Feather", player) or state.can_reach("Tower of Ruin [Grail]", "Region", player)) and (s.attack_below(state) or s.attack_rolling_shuriken(state) or s.attack_bomb(state) or s.attack_caltrops(state) or (s.attack_earth_spear(state) and s.attack_forward(state)) or ((s.glitch_raindrop(state) or s.glitch_catpause(state)) and (s.attack_forward(state) or s.attack_vertical(state))))),
			LocationData("Earth Spear Location", 1, lambda state: state.has("Feather", player) or s.glitch_catpause(state)),
			LocationData("Thunderbird Defeated", 1, lambda state: combat.thunderbird(state), True)
		],
		"Tower of Ruin [Grail]": [
			LocationData("Tower of Ruin Grail Tablet", 1, lambda state: s.state_read_grail(state))
		],
		"Tower of Ruin [Illusion]": [
			LocationData("Map (Tower of Ruin)", 1, lambda state: s.attack_forward(state))
		],
		"Tower of Ruin [Top]": [
			LocationData("Djed Pillar Chest", 1, lambda state: state.has("Nuwa Defeated", player) and s.attack_chest(state)),
			LocationData("Nuwa Defeated", 1, lambda state: state.has_all({"NPC: Philosopher Alsedana", "Feather", "Death Seal"}, player) and combat.nuwa(state), True)
		],
		"Chamber of Birth [Northeast]": [
			LocationData("Perfume Chest", 1, lambda state: state.has("Mudmen Awakened", player) and s.attack_chest_any(state)),
			LocationData("Vessel Chest", 1, lambda state: state.has("Angel Shield", player) and s.attack_chest(state))
		],
		"Chamber of Birth [Southeast]": [
			LocationData("Woman Statue Chest", 1, lambda state: s.attack_chest_any(state) and state.has_any({"Feather", "Grapple Claw"}, player))
		],
		"Chamber of Birth [West]": [
			LocationData("Map (Chamber of Birth) Chest", 1, lambda state: state.has_any({"Woman Statue", "Maternity Statue"}, player) and s.attack_chest(state))
		],
		"Chamber of Birth [Grail]": [
			LocationData("Dimensional Key Chest", 1, lambda state: state.has_all({"Maternity Statue", "Dragon Bone", "Key of Eternity"}, player) and s.attack_forward(state) and (state.has("Cog of the Soul", player) or s.glitch_raindrop(state))),
			LocationData("Chamber of Birth Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Chamber of Birth [Skanda]": [
			LocationData("Pochette Key Chest", 1, lambda state: state.has("Skanda Defeated", player) and s.attack_chest_any(state)),
			LocationData("Skanda Defeated", 1, lambda state: state.can_reach("Chamber of Birth [Dance]", "Region", player) and state.has("Mudmen Awakened", player) and combat.skanda(state), True)
		],
		"Dimensional Corridor [Grail]": [
			LocationData("Map (Dimensional Corridor) Chest", 1, lambda state: s.attack_chest(state) and state.has("Feather", player)),
			LocationData("Dimensional Corridor Grail Tablet", 1, lambda state: s.state_read_grail(state), True)
		],
		"Dimensional Corridor [Upper]": [
			LocationData("Angel Shield Location", 1, lambda state: state.has("Angel Shield Children Defeated", player) and state.has_any({"Feather", "Left Side Children Defeated"}, player) and (state.has("Dimensional Key", player) or s.glitch_catpause(state)))
			LocationData("Sacred Orb (Dimensional Corridor) Chest", 1, lambda state: state.has_all({"Feather", "Dimensional Key", "Death Seal", "Angel Shield Children Defeated"}, player) and s.attack_chest(state)),
			LocationData("Ankh Jewel (Dimensional Corridor) Chest", 1, lambda state: state.has("Mushussu Defeated", player) and s.attack_chest(state)),
			LocationData("Left Side Children Defeated", 1, lambda state: combat.left_side_children(state), True),
			LocationData("Right Side Children Defeated", 1, lambda state: combat.right_side_children(state), True),
			LocationData("Angel Shield Children Defeated", 1, lambda state: combat.angel_shield_children(state), True),
			LocationData("Ushumgallu Defeated", 1, lambda state: state.has("Dimensional Key", player) and combat.ushumgallu(state)),
			LocationData("Mushussu Defeated", 1, lambda state: state.has_all({"Dimensional Key", "Angel Shield Children Defeated"}, player) and (state.has_all({"Left Side Children Defeated", "Right Side Children Defeated"}, player) or s.glitch_raindrop(state)) and combat.mushussu(state), True)
		],
		"True Shrine of the Mother": [
			LocationData("All Grail Tablets Read", 1, lambda state: state.has_all({"Surface Grail Tablet", "Gate of Guidance Grail Tablet", "Mausoleum of the Giants Grail Tablet", "Temple of the Sun Grail Tablet", "Spring in the Sky Grail Tablet", "Inferno Cavern Grail Tablet", "Chamber of Extinction Grail Tablet", "Twin Labyrinths (Front) Grail Tablet", "Endless Corridor Grail Tablet", "Gate of Illusion Grail Tablet", "Graveyard of the Giants Grail Tablet", "Temple of Moonlight Grail Tablet", "Tower of the Goddess Grail Tablet", "Tower of Ruin Grail Tablet", "Chamber of Birth Grail Tablet", "Twin Labyrinths (Back) Grail Tablet", "Dimensional Corridor Grail Tablet"}, player))
		]
	}

	if include_coin_chests:

	return locations