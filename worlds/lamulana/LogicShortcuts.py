from BaseClasses import MultiWorld, CollectionState
from .Options import is_option_enabled, get_option_value, starting_weapon_ids, starting_location_ids

class LaMulanaLogicShortcuts:
	player: int

	flag_autoscan: bool
	flag_ice_cape_lava: bool
	flag_flare_gun_extinction: bool
	flag_subweapon_only: bool
	starting_location: str
	is_frontside_start: bool

	def __init__(self, world: MultiWorld, player: int):
		self.player = player
		self.flag_autoscan = is_option_enabled(world, player, "AutoScanGrailTablets")
		self.flag_ice_cape_lava = is_option_enabled(world, player, "RequireIceCape")
		self.flag_flare_gun_extinction = is_option_enabled(world, player, "RequireFlareGun")
		self.flag_key_fairy_combo_required = is_option_enabled(world, player, "RequireKeyFairyCombo")
		self.flag_subweapon_only = is_option_enabled(world, player, "SubweaponOnly")
		self.flag_pistol_start = get_option_value(world, player, "StartingWeapon") == starting_weapon_ids['pistol']
		self.flag_raindrop = is_option_enabled(world, player, "RaindropsInLogic")
		self.flag_catpause = is_option_enabled(world, player, "CatPausingInLogic")
		self.flag_lamp_glitch = is_option_enabled(world, player, "LampGlitchInLogic")
		
		starting_location_names = {y: x for x, y in starting_location_ids.items()}
		self.starting_location = starting_location_names.[get_option_value(world, player, "StartingLocation")]
		self.is_frontside_start = self.starting_location in {'surface', 'guidance', 'mausoleum', 'sun', 'spring', 'inferno', 'extinction', 'twin (front)', 'endless'}


	#Could add +1 if revive combo was on, but that would turn move.exe and randc.exe into progression
	def get_health_count(self, state: CollectionState) -> bool:
		return state.count("Sacred Orb", self.player)

	def attack_whip(self, state: CollectionState) -> bool:
		return state.has_any({"Leather Whip", "Chain Whip", "Flail Whip"}, self.player)

	def attack_empowered_key_sword(self, state: CollectionState) -> bool:
		return state.has_all({"Key Sword", "Recited All Mantras"}, self.player)

	def attack_shuriken(self, state: CollectionState) -> bool:
		return state.has_all({"Shuriken", "Shuriken Ammo"}, self.player)

	def attack_ring_shuriken(self, state: CollectionState) -> bool:
		return state.has_all({"Shuriken", "Shuriken Ammo", "Ring"}, self.player)

	def attack_rolling_shuriken(self, state: CollectionState) -> bool:
		return state.has_all({"Rolling Shuriken", "Rolling Shuriken Ammo"}, self.player)

	def attack_earth_spear(self, state: CollectionState) -> bool:
		return state.has_all({"Earth Spear", "Earth Spear Ammo"}, self.player)

	def attack_flare_gun(self, state: CollectionState) -> bool:
		return state.has_all({"Flare Gun", "Flare Gun Ammo"}, self.player)

	def attack_ring_flare_gun(self, state: CollectionState) -> bool:
		return state.has_all({"Flare Gun", "Flare Gun Ammo", "Ring"}, self.player)

	def attack_bomb(self, state: CollectionState) -> bool:
		return state.has_all({"Bomb", "Bomb Ammo"}, self.player)

	def attack_chakram(self, state: CollectionState) -> bool:
		return state.has_all({"Chakram", "Chakram Ammo"}, self.player)

	def attack_ring_chakram(self, state: CollectionState) -> bool:
		return state.has_all({"Chakram", "Chakram Ammo", "Ring"}, self.player)

	def attack_caltrops(self, state: CollectionState) -> bool:
		return state.has_all({"Caltrops", "Caltrops Ammo"}, self.player)

	def attack_pistol(self, state: CollectionState) -> bool:
		return state.has_all({"Pistol", "Pistol Ammo"}, self.player) and (self.flag_subweapon_only or self.flag_pistol_start or self.state_fairy_access(state))

	def attack_main(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or state.has_any({"Knife", "Katana", "Axe", "Key Sword"}, self.player)

	def attack_above(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or state.has("Axe", self.player)

	def attack_below(self, state: CollectionState) -> bool:
		return state.has_any({"Axe", "Knife", "Katana"}, self.player)

	def attack_far(self, state: CollectionState) -> bool:
		return self.attack_whip(state) or self.has_any({"Key Sword", "Axe"}, self.player)

	def attack_vertical(self, state: CollectionState) -> bool:
		return state.has_all({"Flare Gun", "Flare Gun Ammo", "Earth Spear", "Earth Spear Ammo"}, self.player)

	def attack_4(self, state: CollectionState) -> bool:
		return self.attack_5(state) or state.has("Chain Whip", self.player)

	def attack_5(self, state: CollectionState) -> bool:
		return state.has_any({"Flail Whip", "Katana", "Axe"}, self.player) or self.attack_empowered_key_sword(state)

	def attack_dps(self, state: CollectionState) -> bool:
		return state.has_any({"Chain Whip", "Flail Whip"}, self.player) or self.attack_empowered_key_sword(state) or (state.has("Gauntlet", self.player) and state.has_any({"Axe", "Katana"}, self.player))

	def attack_forward(self, state: CollectionState) -> bool:
		return self.attack_main(state) or self.attack_s_straight(state) or self.attack_rolling_shuriken(state) or self.attack_bomb(state) or self.attack_caltrops(state)

	def attack_s_straight(self, state: CollectionState) -> bool:
		return self.attack_shuriken(state) or self.attack_chakram(state) or self.attack_pistol(state)

	def attack_s_above(self, state: CollectionState) -> bool:
		return self.attack_flare_gun(state) or self.attack_caltrops(state)

	def attack_chest(self, state: CollectionState) -> bool:
		return self.attack_forward(state) or self.attack_earth_spear(state)

	def attack_chest_any(self, state: CollectionState) -> bool:
		return self.attack_chest(state) or self.attack_flare_gun(state)

	def attack_subweapon(self, state: CollectionState) -> bool:
		return self.attack_shuriken(state) or self.attack_rolling_shuriken(state) or self.attack_earth_spear(state) or self.attack_flare_gun(state) or self.attack_bomb(state) or self.attack_chakram(state) or self.attack_caltrops(state) or self.attack_pistol(state)

	def state_literacy(self, state: CollectionState) -> bool:
		return state.has_all({"Hand Scanner", "reader.exe"}, self.player)

	def state_mobility(self, state: CollectionState) -> bool:
		return state.has_any({"Hermes' Boots", "Feather"}, self.player)

	def state_lamp(self, state: CollectionState) -> bool:
		return state.has_all({"Lamp of Time", "Lamp Recharge"}, self.player)

	def state_extinction_light(self, state: CollectionState) -> bool:
		return attack_flare_gun(state) or not self.flag_flare_gun_extinction

	def state_lava_swim(self, state: CollectionState, amount: int) -> bool:
		if self.flag_ice_cape_lava:
			return self.has("Ice Cape", self.player)
		return self.has("Ice Cape", self.player) or self.get_health_count(state) >= amount

	def state_shield(self, state: CollectionState) -> bool:
		return state.has_any({"Silver Shield", "Angel Shield"}, self.player)

	def state_key_fairy_access(self, state: CollectionState) -> bool:
		return state.has('Fairies Unlocked') and (state.has_all({"miracle.exe", "mekuri.exe"}, self.player) or not flag_key_fairy_combo_required)

	def state_read_grail(self, state: CollectionState) -> bool:
		return self.flag_autoscan or state.has_all({"Hand Scanner", "reader.exe"}, self.player)

	def state_frontside_warp(self, state: CollectionState) -> bool:
		return state.has("Holy Grail", self.player) and self.state_read_grail(state) and (state.has("mirai.exe", self.player) or self.is_frontside_start)

	def state_backside_warp(self, state: CollectionState) -> bool:
		return state.has("Holy Grail", self.player) and self.state_read_grail(state) and (state.has("mirai.exe", self.player) or not self.is_frontside_start)

""" Combos in logic would turn them into progression items
	def combo_revive(self, state: CollectionState) -> bool:
		return state.has_all({"move.exe", "randc.exe"}, self.player)

	def combo_whip(self, state: CollectionState) -> bool:
		return state.has_all({"move.exe", "lamulana.exe"}, self.player)

	def combo_nonwhip(self, state: CollectionState) -> bool:
		return state.has_all({"randc.exe", "mekuri.exe"}, self.player)

	def combo_iframes(self, state: CollectionState) -> bool:
		return state.has_all({"move.exe", "deathv.exe"}, self.player)
"""
	#Only relevant if NPC rando is on
	def combo_dev_npcs(self, state: CollectionState) -> bool:
		return state.has_all({"miracle.exe", "mirai.exe"}, self.player)

	def glitch_raindrop(self, state: CollectionState) -> bool:
		return self.flag_raindrop and state.has_all({"Hermes' Boots", "Grapple Claw"}, self.player)

	def glitch_catpause(self, state:CollectionState = None) -> bool:
		return self.flag_catpause

	def glitch_lamp(self, state: CollectionState) -> bool:
		return self.flag_lamp_glitch and self.state_lamp(state)

	def guardian_count(self, state: CollectionState) -> bool:
		counter = 0
		for boss in ['Amphisbaena Defeated', 'Sakit Defeated', 'Ellmac Defeated', 'Bahamut Defeated', 'Viy Defeated', 'Palenque Defeated', 'Baphomet Defeated', 'Tiamat Defeated']:
			if state.has(boss, self.player):
				counter += 1
		return counter
