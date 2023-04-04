from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld, Location, CollectionState
from .Options import is_option_enabled
from .LogicShortcuts import LaMulanaLogicShortcuts
from .CombatLogic import LaMulanaCombatLogic
from .WorldState import LaMulanaWorldState

class LocationData(NamedTuple):
	name: str
	code: Optional[int]
	logic: Callable[[CollectionState, int], bool] = lambda state: True
	is_event: bool = False
	is_cursable: bool = False

def get_locations_by_region(world: MultiWorld, player: int, worldstate: LaMulanaWorldState) -> Dict[str, List[LocationData]]:
	s = LaMulanaLogicShortcuts(world, player)
	combat = LaMulanaCombatLogic(world, player, s)
	
	include_coin_chests = is_option_enabled(world, player, "RandomizeCoinChests")
	include_trap_items = is_option_enabled(world, player, "RandomizeTrapItems")
	include_hell_temple_reward = get_option_value(world, player, "ProvocativeBathingSuit") == 2

	locations = {
		"Surface [Main]": [
			LocationData("Birth Seal Chest", 2359000, lambda state: s.attack_chest(state) and state.has_all({"Origin Seal", "Helmet"}, player) and state.has_any({"Hermes' Boots", "Feather", "Bahamut Defeated"}), is_cursable=True)
			LocationData("deathv.exe Location", 2359001, lambda state: s.attack_forward(state) and (state.has("NPC: Xelpud", player) or s.glitch_raindrop(state))),
			LocationData("Feather Chest", 2359002, lambda state: s.attack_chest(state) and state.has("Argus Defeated", player), is_cursable=True),
			LocationData("Map (Surface) Location", 2359003, lambda state: state.has("Hand Scanner", player)),
			LocationData("Sacred Orb (Surface) Chest", 2359004, lambda state: state.has("Helmet", player) and state.has_any({"Hermes' Boots", "Bahamut Defeated"}, player) and (attack_above(state) or attack_shuriken(state) or attack_chakram(state) or attack_bomb(state) or attack_pistol(state) or (attack_s_above(state) and attack_chest(state)) or (attack_rolling_shuriken(state) and state.has("Bahamut Defeated", player))), is_cursable=True),
			LocationData("Shell Horn Chest", 2359005, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData("Argus Defeated", None, lambda state: state.has("Serpent Staff", player) and combat.argus(state), True),
			LocationData("Surface Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Gate of Guidance [Main]": [
			LocationData("Ankh Jewel (Gate of Guidance) Chest", 2359006, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state), is_cursable=True),
			LocationData("Crucifix Chest", 2359007, lambda state: s.attack_flare_gun(state) and s.attack_chest(state) and state.has("Life Seal", player), is_cursable=True),
			LocationData("Holy Grail Chest", 2359008, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData("Map (Gate of Guidance) Chest", 2359009, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData("Sacred Orb (Gate of Guidance) Chest", 2359010, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("Shuriken Location", 2359011, lambda state: s.attack_chest_any(state)),
			LocationData("Treasures Chest", 2359012, lambda state: s.attack_chest_any(state) and state.has("Pepper", player), is_cursable=True),
			LocationData("Gate of Guidance Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Gate of Guidance [Door]": [
			LocationData("yagostr.exe Chest", 2359013, lambda state: s.attack_chest(state), is_cursable=True)
		],
		"Mausoleum of the Giants": [
			LocationData("Ankh Jewel (Mausoleum of the Giants) Chest", 2359014, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData("Map (Mausoleum of the Giants) Chest", 2359015, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("Rolling Shuriken Location", 2359016, lambda state: s.attack_chest_any(state)),
			LocationData("Sacred Orb (Mausoleum of the Giants) Chest", 2359017, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("Mausoleum of the Giants Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Temple of the Sun [Main]": [
			LocationData("Ankh Jewel (Temple of the Sun) Chest", 2359018, lambda state: attack_chest(state), is_cursable=True),
			LocationData("Knife Location", 2359019, lambda state: attack_shuriken(state) or (attack_chakram(state) and state.has_any({"Feather", "Grapple Claw"}, player)) or attack_bomb(state) or (attack_flare_gun(state) and attack_forward(state) and state.has("Feather", player)) or glitch_catpause(state)),
			LocationData("Sacred Orb (Temple of the Sun) Chest", 2359020, lambda state: attack_chest_any(state), is_cursable=True)
		],
		"Temple of the Sun [Top Entrance]": [
			LocationData("Map (Temple of the Sun) Chest", 2359021, lambda state: s.attack_chest(state) and s.sun_watchtower(state), is_cursable=True),
		],
		"Temple of the Sun [Grail]": [
			LocationData("Temple of the Sun Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Temple of the Sun [West]": [
			LocationData("Isis' Pendant Chest", 2359022, lambda state: state.has("Buer Defeated", player) and s.state_literacy(state) and s.state_mobility(state) and (s.attack_above(state) or s.attack_s_above(state)), is_cursable=True),
			LocationData("Buer Defeated", None, lambda state: combat.buer(state), True)
		],
		"Temple of the Sun [East]": [
			LocationData("Bronze Mirror Chest", 2359023, lambda state: s.bronze_mirror_chest_logic(state), is_cursable=True),
			LocationData("Talisman Location", 2359024, lambda state: state.has("Viy Defeated", player))
		],
		"Spring in the Sky [Main]": [
			LocationData("Caltrops Location", 2359025),
			LocationData("Map (Spring in the Sky) Chest", 2359026, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("Sacred Orb (Spring in the Sky) Chest", 2359027, lambda state: s.attack_chest_any(state) and state.has("Birth Seal", player), is_cursable=True),
			LocationData("Flooded Temple of the Sun", None, lambda state: (s.attack_forward(state) and (s.state_water_swim(state, 3) or state.has('Holy Grail', player))) or (s.attack_vertical(state) and s.state_water_swim(state, 3)), True)
			LocationData("Spring in the Sky Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Spring in the Sky [Upper]": [
			LocationData("Glove Chest", 2359028, lambda state: state.has("Flooded Spring in the Sky", player) and s.attack_chest_any(state), is_cursable=True),
			LocationData("Origin Seal Chest", 2359029, lambda state: state.has_all({"Helmet", "Nuckelavee Defeated"}, player) and (s.attack_forward(state) or (state.has("Feather", player) and s.attack_earth_spear(state))), is_cursable=True),
			LocationData("Scalesphere Chest", 2359030, lambda state: s.attack_chest(state) and state.has("Helmet", player), is_cursable=True),
			LocationData("Nuckelavee Defeated", None, lambda state: state.has("Helmet", player) and combat.nuckelavee(state), True),
			LocationData("Flooded Spring in the Sky", None, lambda state: state.has_all({"Helmet", "Origin Seal"}, player), True)
		],
		"Inferno Cavern [Main]": [
			LocationData("bunplus.exe Location", 2359031, lambda state: s.attack_forward(state)),
			LocationData("Flare Gun Location", 2359032, lambda state: s.attack_forward(state)),
			LocationData("Ice Cape Chest", 2359033, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData("Map (Inferno Cavern) Chest", 2359034, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("Inferno Cavern Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Inferno Cavern [Pazuzu]": [
			LocationData("Chain Whip Location", 2359035, lambda state: state.has("Pazuzu Defeated", player)),
			LocationData("Pazuzu Defeated", None, lambda state: combat.pazuzu(state), True),
		],
		"Chamber of Extinction [Main]": [
			LocationData("Chakram Location", 2359036, lambda state: s.state_extinction_light(state) and (state.has("Centimani Defeated", player) or s.glitch_catpause(state))),
			LocationData("Life Seal Chest", 2359037, lambda state: s.state_extinction_light(state) and s.attack_chest(state) and state.has("Birth Seal", player), is_cursable=True),
			LocationData("mantra.exe Scan", 2359038, lambda state: s.attack_flare_gun(state) and state.has_all({"Magatama Jewel", "torude.exe", "Ox-head & Horse-face Defeated"})),
			LocationData("Sacred Orb (Chamber of Extinction) Chest", 2359039, lambda state: s.state_extinction_light(state) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player))), is_cursable=True),
			LocationData("Centimani Defeated", None, lambda state: s.state_extinction_light(state) and combat.centimani(state), True),
			LocationData("Chamber of Extinction Grail Tablet", None, lambda state: s.state_extinction_light(state) and s.state_read_grail(state), True)
		],
		"Chamber of Extinction [Map]": [
			LocationData("Map (Chamber of Extinction) Chest", 2359040, lambda state: s.state_extinction_light(state) and s.attack_chest_any(state), is_cursable=True)
		],
		"Chamber of Extinction [Magatama]": [
			LocationData("Ox-head & Horse-face Defeated", None, lambda state: combat.oxhead_horseface(state), True)
		],
		"Chamber of Extinction [Ankh Lower]": [
			LocationData("Hell Temple Unlocked", None, lambda state: s.hell_temple_requirements(state), True)
		],
		"Twin Labyrinths [Loop]": [
			LocationData("Ring Location", 2359041, lambda state: s.glitch_raindrop(state) or state.can_reach('Twin Labyrinths [Upper Left]', 'Region', player))
		],
		"Twin Labyrinths [Jewel]": [
			LocationData("Ankh Jewel (Twin Labyrinths) Chest", 2359042, lambda state: state.can_reach("Twin Labyrinths [Lower]", "Region", player) and state.can_reach("Twin Labyrinths [Upper Left]", "Region", player) and s.attack_flare_gun(state) and s.attack_chest(state), is_cursable=True)
		],
		"Twin Labyrinths [Katana]": [
			LocationData("Katana Location", 2359043, lambda state: state.has_all({"Peryton Defeated", "Twin Statue"}, player) or s.glitch_catpause(event))
		],
		"Twin Labyrinths [Poison 1]": [
			LocationData("Map (Twin Labyrinths) Chest", 2359044, lambda state: state.has("Twin Poison Cleared") and s.attack_forward(state), is_cursable=True),
			LocationData("Twin Poison Cleared", None, lambda state: state.has("Twin Statue") or (state.can_reach("Twin Labyrinths [Poison 2]", "Region", player), True) and state.has('Holy Grail', player))
		],
		"Twin Labyrinths [Upper Grail]": [
			LocationData("Twin Labyrinths (Front) Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Twin Labyrinths [Lower]": [
			LocationData("Sacred Orb (Twin Labyrinths) Chest", 2359045, lambda state: s.attack_chest(state) and (state.has("Zu Defeated", player) or s.glitch_raindrop(state) or (s.glitch_lamp(state) and state.has("Holy Grail", player))), is_cursable=True),
			LocationData("Zu Defeated", None, lambda state: combat.zu(state), True),
			LocationData("Peryton Defeated", None, lambda state: combat.peryton(state), True),
			LocationData("Twin Labyrinths (Back) Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Endless Corridor [1F]": [
			LocationData("Map (Endless Corridor) Chest", 2359046, lambda state: s.endless_oneway_open(worldstate) and s.attack_chest_any(state), is_cursable=True) #TODO Depends on entrance randomizer - if Skanda or Illusion, also need to account for those
		],
		"Endless Corridor [2F]": [
			LocationData("Key Sword Location", 2359047, lambda state: s.attack_chest(state))
		],
		"Endless Corridor [3F Upper]": [
			LocationData("Twin Statue Chest", 2359048, lambda state: s.attack_chest_any(state) and (state.has("Holy Grail", player) or s.glitch_raindrop(state) or (state.has("Key of Eternity", player) and (s.attack_forward(state) or (state.has("Feather", player) and (s.attack_flare_gun(state) or s.attack_earth_spear(state)))))), is_cursable=True)
		],
		"Endless Corridor [5F]": [
			LocationData("Backbeard & Tai Sui Defeated", None, lambda state: s.state_literacy(state) and combat.backbeard_tai_sui(state), True)
		],
		"Shrine of the Mother [Main]": [
			LocationData("bounce.exe Chest", 2359049, lambda state: s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state) or (s.attack_flare_gun(state) and state.has("Removed Shrine Skulls", player)), is_cursable=True),
			LocationData("Crystal Skull Chest", 2359050, lambda state: s.attack_chest(state) and state.has_all({"Life Seal", "Removed Shrine Skulls"}, player), is_cursable=True),
			LocationData("Diary Chest", 2359051, lambda state: s.attack_chest(state) and state.has_all({"Removed Shrine Skulls", "Talisman", "NPC: Xelpud"}, player), is_cursable=True),
			LocationData("Sacred Orb (Shrine of the Mother) Chest", 2359052, lambda state: s.attack_chest(state) and state.has_all({"Origin Seal", "Birth Seal", "Life Seal", "Death Seal"}, player), is_cursable=True),
			LocationData("Removed Shrine Skulls", None, lambda state: state.has_all({'Dragon Bone', 'yagostr.exe', 'yagomap.exe', 'Map (Shrine of the Mother)'}, player), True)
			#Normal shrine grail tablet doesn't matter, I think - only true shrine
		],
		"Shrine of the Mother [Seal]": [
			LocationData("Death Seal Chest", 2359053, lambda state: s.attack_chest(state) and ((state.has_all("Feather", player) and self.s.boss_count(state) >= 8) or (state.has_any({"Feather", "Grapple Claw"}, player) and (s.glitch_raindrop(state) or state.has("Removed Shrine Skulls", player)))), is_cursable=True)
		],
		"Shrine of the Mother [Map]": [
			LocationData("Map (Shrine of the Mother) Chest", 2359054, lambda state: s.attack_chest_any(state), is_cursable=True)
		],
		'Gate of Illusion [Eden]': [
			LocationData("Illusion Unlocked", None, lambda state: state.has('Fruit of Eden', self.player), True)
		],
		"Gate of Illusion [Upper]": [
			LocationData("Cog of the Soul Chest", 2359055, lambda state: s.state_literacy(state) and state.can_reach("Gate of Illusion [Pot Room]", "Region", player) and state.can_reach("Gate of Illusion [Middle]", "Region", player) and s.state_lamp(state) and state.has_all({"Feather", "Ba Defeated"}, player) and s.attack_forward(state), is_cursable=True),
			LocationData("Mudmen Awakened", None, lambda state: state.has_all({"Feather", "Cog of the Soul"}, player) and s.attack_forward(state), True),
			LocationData("Ba Defeated", None, lambda state: s.state_literacy(state) and state.has("Feather", player) and combat.ba(state), True)
		],
		"Gate of Illusion [Middle]": [
			LocationData("Fairy Clothes Chest", 2359056, lambda state: s.state_key_fairy_access(state) and s.attack_below(state), is_cursable=True)
		],
		"Gate of Illusion [Grail]": [
			LocationData("Key of Eternity Chest", 2359057, lambda state: s.attack_chest(state) and state.has("Chi You Defeated", player)),
			LocationData("Gate of Illusion Grail Tablet", None, lambda state: s.state_read_grail(state), True),
			LocationData("Chi You Defeated", None, lambda state: (s.glitch_raindrop(state) or (state.can_reach("Mausoleum of the Giants", "Region", player) and state.has("Mini Doll", player) and s.state_literacy(state))) and (state.has("Birth Seal", player) or s.glitch_lamp(state)) and combat.chi_you(state), True)
		],
		"Gate of Illusion [Dracuet]": [
			LocationData("Map (Gate of Illusion) Chest", 2359058, lambda state: s.attack_forward(state), is_cursable=True)
		],
		"Graveyard of the Giants [West]": [
			LocationData("Gauntlet Chest", 2359059, lambda state: s.attack_chest_any(state) and state.has_all({"Feather", "Life Seal"}, player), is_cursable=True),
			LocationData("Map (Graveyard of the Giants) Chest", 2359060, lambda state: s.attack_chest_any(state), is_cursable=True),
			LocationData("mirai.exe Chest", 2359061, lambda state: s.attack_chest(state) and state.has("Feather", player), is_cursable=True),
			LocationData("Silver Shield Location", 2359062, lambda state: s.attack_below(state))
		],
		"Graveyard of the Giants [Grail]": [
			LocationData("Graveyard of the Giants Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Graveyard of the Giants [East]": [
			LocationData("Bomb Location", 2359063, lambda state: state.has_all({"Feather", "Kamaitachi Defeated"}, player)),
			LocationData("emusic.exe Scan", 2359064, lambda state: s.attack_bomb(state) and state.has("torude.exe", player)),
			LocationData("Kamaitachi Defeated", None, lambda state: state.has("Feather", player) and combat.kamaitachi(state), True)
		],
		"Temple of Moonlight [Upper]": [
			LocationData('Axe Location', 2359065, lambda state: (s.state_mobility(state) and s.attack_forward(state)) or (state.has('Grapple Claw', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state))))
			LocationData("Fruit of Eden Chest", 2359066, lambda state: s.attack_chest_any(state) and state.has("Hand Scanner", player) and state.can_reach("Temple of Moonlight [Lower]", "Region", player) and state.can_reach("Temple of Moonlight [Grapple]", "Region", player) and state.can_reach("Temple of Moonlight [Southeast]", "Region", player), is_cursable=True)
		],
		"Temple of Moonlight [Grapple]": [
			LocationData("Grapple Claw Chest", 2359067, lambda state: s.attack_chest(state), is_cursable=True)
		],
		"Temple of Moonlight [Map]": [
			LocationData("Map (Temple of Moonlight) Chest", 2359068, lambda state: s.attack_chest_any(state), is_cursable=True)
		],
		"Temple of Moonlight [Pyramid]": [
			#Not cursable because it's not a real chest
			LocationData("Philosopher's Ocarina Chest", 2359069, lambda state: state.has("Maternity Statue", player) and (state.has("Feather", player) or s.glitch_raindrop(state)))
		],
		"Temple of Moonlight [Southeast]": [
			LocationData("Serpent Staff Chest", 2359070, lambda state: s.attack_chest(state) and state.has("Anubis Defeated", player), is_cursable=True),
			LocationData("Anubis Defeated", None, lambda state: state.has("Book of the Dead", player) and (state.has("Birth Seal", player) or s.glitch_raindrop(state)) and combat.anubis(state), True)
		],
		"Tower of the Goddess [Lower]": [
			LocationData("Eye of Truth Chest", 2359071, lambda state: s.attack_chest_any(state) and state.can_reach("Tower of the Goddess [Lamp]", "Region", player) and state.has("Flooded Tower of the Goddess", player), is_cursable=True),
			LocationData("Flail Whip Location", 2359072, lambda state: (s.state_literacy(state) or s.glitch_catpause(state)) and (s.glitch_lamp(state) or state.has('NPC: Philosopher Samaranta', player))),
			LocationData("Map (Tower of the Goddess) Chest", 2359073, lambda state: s.attack_forward(state), is_cursable=True),
			LocationData("Flooded Tower of the Goddess", None, lambda state: state.has("Flooded Spring in the Sky", player) and s.state_literacy(state) and (s.attack_caltrops(state) or s.attack_earth_spear(state) or s.attack_bomb(state) or state.has_any({"Knife", "Katana"}, player)) and (state.has_any({"Holy Grail", "Scalesphere", "Sacred Orb"}, player)), True)
		],
		"Tower of the Goddess [Grail]": [
			LocationData("Plane Model Chest", 2359074, lambda state: state.has_all({"Eye of Truth", "Vimana Defeated"}, player) and (s.attack_chest(state) or (s.attack_flare_gun(state) and state.has("Feather", player))) and state.can_reach("Tower of the Goddess [Spaulder]", "Region", player) and state.can_reach("Tower of the Goddess [Lower]", "Region", player), is_cursable=True),
			LocationData("Spaulder Chest", 2359075, lambda state: s.state_key_fairy_access(state) and s.attack_forward(state) and (state.has_all({"Holy Grail", "mirai.exe"}, player)) or state.has_all({"Feather", "Hermes' Boots"}, player), is_cursable=True),
			LocationData("Vimana Defeated", None, lambda state: state.has("Flooded Tower of the Goddess", player) and combat.vimana(state), True)
		],
		"Tower of Ruin [Southeast]": [
			LocationData("Sacred Orb (Tower of Ruin) Chest", 2359076, lambda state: s.attack_chest_any(state), is_cursable=True)
		],
		"Tower of Ruin [Southwest]": [
			LocationData("Ankh Jewel (Tower of Ruin) Chest", 2359077, lambda state: (state.has("Feather", player) or state.can_reach("Tower of Ruin [Grail]", "Region", player)) and (s.attack_below(state) or s.attack_rolling_shuriken(state) or s.attack_bomb(state) or s.attack_caltrops(state) or (s.attack_earth_spear(state) and s.attack_forward(state)) or ((s.glitch_raindrop(state) or s.glitch_catpause(state)) and (s.attack_forward(state) or s.attack_vertical(state)))), is_cursable=True),
			LocationData("Earth Spear Location", 2359078, lambda state: state.has("Feather", player) or s.glitch_catpause(state)),
			LocationData("Thunderbird Defeated", None, lambda state: combat.thunderbird(state), True)
		],
		"Tower of Ruin [La-Mulanese]": [
			LocationData("Medicine Statue Open", None, lambda state: s.state_lamp(state) and s.attack_chest(state))
		],
		"Tower of Ruin [Grail]": [
			LocationData("Tower of Ruin Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Tower of Ruin [Illusion]": [
			LocationData("Map (Tower of Ruin)", 2359079, lambda state: s.attack_forward(state), is_cursable=True)
		],
		"Tower of Ruin [Top]": [
			LocationData("Djed Pillar Chest", 2359080, lambda state: state.has("Nuwa Defeated", player) and s.attack_chest(state), is_cursable=True),
			LocationData("Nuwa Defeated", None, lambda state: s.nuwa_access(state) and combat.nuwa(state), True)
		],
		"Chamber of Birth [Northeast]": [
			LocationData("Perfume Chest", 2359081, lambda state: state.has("Mudmen Awakened", player) and s.attack_chest_any(state), is_cursable=True),
			LocationData("Vessel Chest", 2359082, lambda state: state.has("Angel Shield", player) and s.attack_chest(state), is_cursable=True)
		],
		"Chamber of Birth [Southeast]": [
			LocationData("Woman Statue Chest", 2359083, lambda state: s.attack_chest_any(state) and state.has_any({"Feather", "Grapple Claw"}, player), is_cursable=True)
		],
		"Chamber of Birth [West]": [
			LocationData("Map (Chamber of Birth) Chest", 2359084, lambda state: state.has_any({"Woman Statue", "Maternity Statue"}, player) and s.attack_chest(state), is_cursable=True)
		],
		"Chamber of Birth [Grail]": [
			LocationData("Dimensional Key Chest", 2359085, lambda state: state.has_all({"Maternity Statue", "Dragon Bone", "Key of Eternity"}, player) and s.attack_forward(state) and (state.has("Cog of the Soul", player) or s.glitch_raindrop(state)), is_cursable=True),
			LocationData("Chamber of Birth Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Chamber of Birth [Skanda]": [
			LocationData("Pochette Key Chest", 2359086, lambda state: state.has("Skanda Defeated", player) and s.attack_chest_any(state), is_cursable=True),
			LocationData("Skanda Defeated", None, lambda state: state.can_reach("Chamber of Birth [Dance]", "Region", player) and state.has("Mudmen Awakened", player) and combat.skanda(state), True)
		],
		"Dimensional Corridor [Grail]": [
			LocationData("Map (Dimensional Corridor) Chest", 2359087, lambda state: s.attack_chest(state) and state.has("Feather", player), is_cursable=True),
			LocationData("Dimensional Corridor Grail Tablet", None, lambda state: s.state_read_grail(state), True)
		],
		"Dimensional Corridor [Upper]": [
			LocationData("Angel Shield Location", 2359088, lambda state: state.has("Angel Shield Children Defeated", player) and state.has_any({"Feather", "Left Side Children Defeated"}, player) and (state.has("Dimensional Key", player) or s.glitch_catpause(state)))
			LocationData("Sacred Orb (Dimensional Corridor) Chest", 2359089, lambda state: state.has_all({"Feather", "Dimensional Key", "Death Seal", "Angel Shield Children Defeated"}, player) and s.attack_chest(state), is_cursable=True),
			LocationData("Ankh Jewel (Dimensional Corridor) Chest", 2359090, lambda state: state.has("Mushussu Defeated", player) and s.attack_chest(state), is_cursable=True),
			LocationData("Magatama Jewel Chest", 2359091, lambda state: state.has('Tiamat Defeated', player) and s.attack_chest(state), is_cursable=True),
			LocationData("Left Side Children Defeated", None, lambda state: combat.left_side_children(state), True),
			LocationData("Right Side Children Defeated", None, lambda state: combat.right_side_children(state), True),
			LocationData("Angel Shield Children Defeated", None, lambda state: combat.angel_shield_children(state), True),
			LocationData("Ushumgallu Defeated", None, lambda state: state.has("Dimensional Key", player) and combat.ushumgallu(state)),
			LocationData("Mushussu Defeated", None, lambda state: state.has_all({"Dimensional Key", "Angel Shield Children Defeated"}, player) and (state.has_all({"Left Side Children Defeated", "Right Side Children Defeated"}, player) or s.glitch_raindrop(state)) and combat.mushussu(state), True)
		],
		"True Shrine of the Mother": [
			LocationData("All Grail Tablets Read", None, lambda state: state.has_all({"Surface Grail Tablet", "Gate of Guidance Grail Tablet", "Mausoleum of the Giants Grail Tablet", "Temple of the Sun Grail Tablet", "Spring in the Sky Grail Tablet", "Inferno Cavern Grail Tablet", "Chamber of Extinction Grail Tablet", "Twin Labyrinths (Front) Grail Tablet", "Endless Corridor Grail Tablet", "Gate of Illusion Grail Tablet", "Graveyard of the Giants Grail Tablet", "Temple of Moonlight Grail Tablet", "Tower of the Goddess Grail Tablet", "Tower of Ruin Grail Tablet", "Chamber of Birth Grail Tablet", "Twin Labyrinths (Back) Grail Tablet", "Dimensional Corridor Grail Tablet"}, player)),
			LocationData("Mother Defeated", None, lambda state: state.has_all({'All Grail Tablets Read', 'Fairies Unlocked'}, player) and combat.mother(state))
		]
	}

	if include_coin_chests:
		locations['Surface [Main]'].extend([
			LocationData('Surface Waterfall Coin Chest', 2359092, lambda state: s.attack_chest(state), is_cursable=True),
			LocationData('Surface Seal Coin Chest', 2359093, lambda state: s.attack_chest(state) and state.has('Life Seal', player), is_cursable=True)
		])
		locations['Surface [Ruin Path Upper]'] = [
			LocationData('Surface Underground Path Coin Chest', 2359094, lambda state: s.attack_bomb(state), is_cursable=True)
		]
		locations['Mausoleum of the Giants'].extend([
			LocationData('Mausoleum of the Giants Coin Chest', 2359095, lambda state: s.attack_shuriken(state) or s.attack_chakram(state) or s.attack_pistol(state) or (s.attack_main(state) and state.has('Feather', player)), is_cursable=True)
		])
		locations['Temple of the Sun [Main]'].extend([
			#attack fairy logic
			LocationData('Temple of the Sun Pyramid Coin Chest', 2359096, lambda state: s.attack_bomb(state) or (state.has_all({'Bomb', 'Fairies Unlocked'}, player) and s.state_frontside_warp(state)), is_cursable=True)
		])
		locations['Spring in the Sky [Main]'].extend([
			LocationData('Spring in the Sky Coin Chest', 2359097, lambda state: s.attack_forward(state) or (s.attack_vertical(state) and (s.get_health_count(state) >= 3 or state.has_any({'Holy Grail', 'Scalesphere'}, player))), is_cursable=True)
		])
		locations['Inferno Cavern [Main]'].extend([
			LocationData('Inferno Cavern Lava Coin Chest', 2359098, lambda state: s.attack_chest(state) and (s.state_lava_swim(state, 2) if state.has('Holy Grail', player) else s.state_lava_swim(state, 4)), is_cursable=True)
		])
		locations['Inferno Cavern [Spikes]'] = [
			LocationData('Inferno Cavern Echidna\'s Chamber Coin Chest', 2359099, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_earth_spear(state) or s.attack_flare_gun(state) or s.attack_bomb(state) or s.attack_caltrops(state) or s.attack_chakram(state), is_cursable=True)
		]
		locations['Chamber of Extinction [Left Main]'] = [
			LocationData('Chamber of Extinction Coin Chest', 2359100, lambda state: s.attack_chest(state), is_cursable=True)
		]
		locations['Twin Labyrinths [Lower]'].extend([
			LocationData('Twin Labyrinths Witches Coin Chest', 2359101, lambda state: state.has('Peryton Defeated', player) and s.attack_forward(state), is_cursable=True),
			LocationData('Twin Labyrinths Lower Coin Chest', 2359102, lambda state: s.attack_chest_any(state), is_cursable=True)
		])
		locations['Twin Labyrinths [Upper Left]'].extend([
			LocationData('Twin Labyrinths Escape Coin Chest', 2359103, lambda state: state.has('Mother Defeated', player) and s.attack_chest(state), is_cursable=True)
		])
		locations['Endless Corridor [3F Upper]'].extend([
			LocationData('Endless Corridor Coin Chest', 2359104, lambda state: s.attack_main(state), is_cursable=True)
		]),
		locations['Gate of Illusion [Middle]'].extend([
			LocationData('Gate of Illusion Katana Coin Chest', 2359105, lambda state: state.has('Katana', player), is_cursable=True)
		])
		locations['Gate of Illusion [Lower]'] = [
			LocationData('Gate of Illusion Spikes Coin Chest', 2359106, lambda state: s.attack_chest(state), is_cursable=True)
		]
		locations['Graveyard of the Giants [West]'].extend([
			LocationData('Graveyard of the Giants Coin Chest', 2359107, lambda state: state.has('Feather', player) and s.attack_forward(state), is_cursable=True)
		])
		locations['Temple of Moonlight [Eden]'] = [
			LocationData('Temple of Moonlight Coin Chest', 2359108, lambda state: s.attack_bomb(state) or (s.attack_caltrops(state) and state.has_any({'Feather', 'Ring'}, player)) or (state.has('Feather', player) and (s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_pistol(state))), is_cursable=True)
		]
		locations['Tower of the Goddess [Grail]'].extend([
			LocationData('Tower of the Goddess Shield Statue Coin Chest', 2359109, lambda state: state.has_any({'Katana', 'Knife'}, player) or s.attack_caltrops(state) or s.attack_bomb(state) or (s.attack_forward(state) and (s.attack_earth_spear(state) or s.glitch_catpause(state) or s.glitch_raindrop(state))), is_cursable=True)
		])
		locations['Tower of the Goddess [Lower]'].extend([
			LocationData('Tower of the Goddess Fairy Spot Coin Chest', 2359110, lambda state: s.attack_chest_any(state), is_cursable=True)
		])
		locations['Tower of Ruin [Spirits]'] = [
			LocationData('Tower of Ruin Coin Chest', 2359111, lambda state: s.attack_shuriken(state) or s.attack_rolling_shuriken(state) or s.attack_chakram(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_pistol(state), is_cursable=True)
		]
		locations['Chamber of Birth [Northeast]'].extend([
			LocationData('Chamber of Birth Ninja Coin Chest', 2359112, lambda state: s.attack_main(state) or s.attack_shuriken(state) or s.attack_bomb(state) or s.attack_chakram(state) or s.attack_caltrops(state) or s.attack_pistol(state) or (s.state_lamp(state) and (s.attack_earth_spear(state) or s.attack_flare_gun(state) or s.attack_rolling_shuriken(state))), is_cursable=True)
		])
		locations['Chamber of Birth [Southeast]'].extend([
			LocationData('Chamber of Birth Southeast Coin Chest', 2359113, lambda state: s.attack_forward(state), is_cursable=True)
		])
		locations['Chamber of Birth [Dance]'].extend([
			LocationData('Chamber of Birth Dance of Life Coin Chest', 2359114, lambda state: s.attack_forward(state) or s.attack_flare_gun(state), is_cursable=True)
		])
		locations['Dimensional Corridor [Grail]'].extend([
			LocationData('Dimensional Corridor Coin Chest', 2359115, lambda state: s.attack_forward(state) or s.attack_flare_gun(state), is_cursable=True)
		])

	if include_trap_items:
		locations['Inferno Cavern [Main]'].append(
			LocationData('Inferno Cavern Fake Orb', 2359116)
		)
		locations['Twin Labyrinths [Loop]'].append(
			LocationData('Twin Labyrinths Fake Ankh Jewel', 2359117)
		)
		locations['Gate of Illusion [Dracuet]'].append(
			LocationData('Gate of Illusion Exploding Chest', 2359118, lambda state: s.attack_chest(state), is_cursable=True)
		)
		locations['Graveyard of the Giants [West]'].append(
			LocationData('Graveyard of the Giants Trap Chest', 2359119, lambda state: s.attack_chest(state), is_cursable=True)
		)

	if include_hell_temple_reward:
		locations['Hell Temple [Dracuet]'] = [
			LocationData("Hell Temple Final Reward", 2359120)
		]

	return locations