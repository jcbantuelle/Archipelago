from typing import Dict, Union, List
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, OptionList

starting_location_ids = {
	'surface': 0
	'guidance': 1
	'mausoleum': 2
	'sun': 3
	'spring': 4
	'inferno': 5,
	'extinction': 6,
	'twin (front)': 7
	'endless': 8,
	'illusion': 9
	'graveyard': 10,
	'moonlight': 11,
	'goddess': 12,
	'ruin': 13,
	'birth': 14,
	'twin (back)': 15,
	'gate of time (surface)': 16
}

starting_weapon_ids = {
	'leather whip': 0
	'knife': 1
	'key sword': 2
	'axe': 3
	'katana': 4
	'shuriken': 5
	'rolling shuriken': 6
	'earth spear': 7
	'flare gun': 8
	'bomb': 9
	'chakram': 10
	'caltrops': 11
	'pistol': 12
}

class RandomizeShops(Toggle):
	"If on, randomizes all shop items. If off, unique shop items are still randomized"
	display_name = "Randomize all shop items"

class RandomizeNPCs(Toggle):
	"Randomizes all NPCs and shop locations"
	display_name = "Randomize NPC/shop doors"

class RandomizeCoinChests(Toggle):
	"Randomizes all coin chests"
	display_name = "Randomize coin chests"

class RandomizeTrapItems(Toggle):
	"Randomizes the 4 trap items and locations"
	display_name = "Randomize Trap Items"

class RandomizeSeals(Toggle):
	"Individually randomizes which seal is required to break each wall seal"
	display_name = "Randomize seals"

class ProvocativeBathingSuit(Choice):
	"In Item Pool: The provocative bathing suit is in the item pool, but Hell Temple is not required. Hell Temple: The final reward for beating Hell Temple may be required"
	display_name = "Hell Temple Reward"
	option_off: 0
	option_in_item_pool = 1
	option_hell_temple = 2
	alias_true: 1

class RandomizeCursedChests(Toggle):
	"If on, 4 random chests will be cursed instead of the 4 vanilla cursed chests"
	display_name = "Randomize Cursed Chests"

class RandomizeDracuetsShop(Toggle):
	"Randomize Dracuet's shop in Hell Temple. If NPC rando is on, includes the Hell Temple shop in the randomized NPC pool"
	display_name = "Randomize Dracuet's Shop"

class StartingLocation(Choice):
	"Set or randomize your starting location"
	display_name = "Starting Location"
	option_surface = starting_location_ids['surface']
	option_gate_of_guidance = starting_location_ids['guidance']
	option_mausoleum_of_the_giants = starting_location_ids['mausoleum']
	option_temple_of_the_sun = starting_location_ids['sun']
	option_spring_in_the_sky = starting_location_ids['spring']
	option_inferno_cavern = starting_location_ids['inferno']
	option_chamber_of_extinction = starting_location_ids['extinction']
	option_twin_labs_front = starting_location_ids['twin (front)']
	option_endless_corridor = starting_location_ids['endless']
	option_gate_of_illusion = starting_location_ids['illusion']
	option_graveyard_of_the_giants = starting_location_ids['graveyard']
	option_temple_of_moonlight = starting_location_ids['moonlight']
	option_tower_of_the_goddess = starting_location_ids['goddess']
	option_tower_of_ruin = starting_location_ids['ruin']
	option_chamber_of_birth = starting_location_ids['birth']
	option_twin_labs_back = starting_location_ids['twin (back)']
	option_gate_of_time_surface = starting_location_ids['gate of time (surface)']

class StartingWeapon(Choice):
	"Set or randomize your starting weapon"
	display_name = "Starting Weapon"
	option_leather_whip = starting_weapon_ids['leather whip']
	option_knife = starting_weapon_ids['knife']
	option_key_sword = starting_weapon_ids['key sword']
	option_axe = starting_weapon_ids['axe']
	option_katana = starting_weapon_ids['katana']
	option_shuriken = starting_weapon_ids['shuriken']
	option_rolling_shuriken = starting_weapon_ids['rolling shuriken']
	option_earth_spear = starting_weapon_ids['earth spear']
	option_flare_gun = starting_weapon_ids['flare gun']
	option_bomb = starting_weapon_ids['bomb']
	option_chakram = starting_weapon_ids['chakram']
	option_caltrops = starting_weapon_ids['caltrops']
	option_pistol = starting_weapon_ids['pistol']

class StartWithHolyGrail(DefaultOnToggle):
	"Starting with the Holy Grail is generally recommended"
	display_name = "Start with the Holy Grail"

class StartWithMirai(DefaultOnToggle):
	"Start with mirai.exe for backside warping"
	display_name = "Start with mirai.exe"

class StartWithHandScanner(Toggle):
	"Start with the hand scanner"
	display_name: "Start with the Hand Scanner"

class StartWithReader(Toggle):
	"Start with the reader software"
	display_name: "Start with Reader"

class StartWithHermesBoots(Toggle):
	"Start with boots to go fast right away"
	display_name = "Start with Hermes' Boots"

class RandomizeTransitions(Choice):
	"Randomizes transitions between areas. \"On\" does not include one-way transitions, whereas \"Full\" includes one-way transitions"
	display_name = "Randomize Transitions"
	option_off = 0
	option_on = 1
	option_full = 2

class RandomizeBacksideDoors(Choice):
	"Randomizes the backside doors, without including non-boss doors (Extinction-Gate of Time and Dimensional-Endless Corridor). \"Full\" adds these non-boss transitions to the entrance pool"
	display_name = "Randomize Backside Doors"
	option_off = 0
	option_boss_doors_only = 1
	option_full = 2

class RequireIceCape(DefaultOnToggle):
	"Requires the ice cape for swimming through lava. If off, you may instead need enough health to survive the swim"
	display_name = "Require Ice Cape for Lava"

class RequireFlareGun(DefaultOnToggle):
	"Logically requires the flare gun to do anything in the Chamber of Extinction"
	display_name = "Require Flare Gun for Chamber of Extinction"

class RequireKeyFairyCombo(DefaultOnToggle):
	"Requires the software combination miracle + mekuri to summon key fairies. If off, you may need to grind for key fairies"
	display_name = "Key Fairies expect miracle + mekuri"

class AutoScanGrailTablets(DefaultOnToggle):
	"Quality of life - walking past a grail tablet scans it automatically. Otherwise, Hand Scanner and reader.exe are required to warp back to it."
	display_name = "Automatically Scan Grail Tablets"

class AlternateMotherAnkh(DefaultOnToggle):
	"Quality of life - If on, skips the mantra sequence to empower the key sword by adding a 9th ankh jewel. Mother's ankh will be like other bosses' and cannot be activated by an empowered key sword."
	display_name = "Alternate Mother Ankh"

class HardCombatLogic(Toggle):
	"If on, combat logic for bosses and room guardians is minimal - would it be theoretically possible to defeat this boss with these items at 32 HP?"
	display_name = "Hard Combat Logic"

#Add note about what happens when you set startingweapon to a main weapon and this is on - maybe overrides it and gives a random subweapon?
class SubweaponOnly(Toggle):
	"If on, removes all main weapons from the item pool, and all subweapon ammo in shops is free."
	display_name = "Subweapon Only Mode"

class RaindropsInLogic(Toggle):
	"Glitch logic - raindropping may be expected with Hermes' Boots and Grapple Claw"
	display_name = "Raindrops In Logic"

class CatPausingInLogic(Toggle):
	"Glitch logic - cat pausing may be expected without any items"
	display_name = "Cat Pausing In Logic"

class LampGlitchInLogic(Toggle):
	"Glitch Logic - using the lamp of time to pass through certain walls may be required"
	display_name = "Lamp Glitch In Logic"

lamulana_options = {
	"RandomizeShops": RandomizedShops,
	"RandomizeNPCs": RandomizeNPCs,
	"RandomizeCoinChests": RandomizeCoinChests,
	"RandomizeTrapItems": RandomizeTrapItems,
	"ProvocativeBathingSuit": ProvocativeBathingSuit,
	"RandomizeCursedChests": RandomizeCursedChests,
	"RandomizeDracuetsShop": RandomizeDracuetsShop,
	"RandomizeSeals": RandomizeSeals,
	"StartingLocation": StartingLocation,
	"StartingWeapon": StartingWeapon,
	"StartWithHolyGrail": StartWithHolyGrail,
	"StartWithMirai": StartWithMirai,
	"StartWithHandScanner": StartWithHandScanner,
	"StartWithReader": StartWithReader,
	"StartWithHermesBoots": StartWithHermesBoots,
	"RandomizeTransitions": RandomizeTransitions,
	"RandomizeBacksideDoors": RandomizeBacksideDoors,
	"RequireIceCape": RequireIceCape,
	"RequireFlareGun": RequireFlareGun,
	"RequireKeyFairyCombo": RequireKeyFairyCombo,
	"AlternateMotherAnkh": AlternateMotherAnkh,
	"HardCombatLogic": HardCombatLogic,
	"SubweaponOnly": SubweaponOnly,
	"RaindropsInLogic": RaindropsInLogic,
	"CatPausingInLogic": CatPausingInLogic,
	"LampGlitchInLogic": LampGlitchInLogic
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
	return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
	option = getattr(world, name, None)
	if option == None:
		return 0
	return option[player].value