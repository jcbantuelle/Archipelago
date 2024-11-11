GLOBAL_FLAGS = {
  "talisman_found": 0xa4,
  "crucifix_found": 0xab,
  "surface_map": 0xd1,
  "shrine_map": 0xda,
  "xmailer": 0xe3,
  "grail_tablet_guidance": 0x64,
  "grail_tablet_mausoleum": 0x65,
  "grail_tablet_sun": 0x66,
  "grail_tablet_spring": 0x67,
  "grail_tablet_inferno": 0x68,
  "grail_tablet_extinction": 0x69,
  "grail_tablet_twin_front": 0x6a,
  "grail_tablet_endless": 0x6b,
  "grail_tablet_shrine_front": 0x6c,
  "grail_tablet_illusion": 0x6d,
  "grail_tablet_graveyard": 0x6e,
  "grail_tablet_moonlight": 0x6f,
  "grail_tablet_goddess": 0x70,
  "grail_tablet_ruin": 0x71,
  "grail_tablet_birth": 0x72,
  "grail_tablet_twin_back": 0x73,
  "grail_tablet_dimensional": 0x74,
  "grail_tablet_shrine_back": 0x75,
  "ankh_jewel_mausoleum": 0x8f,
  "yagostr_found": 0xe5,
  "guardians_killed": 0x102,
  "diary_found": 0x104,
  "mulana_talisman": 0x105,
  "endless_fairyqueen": 0x1f5,
  "diary_chest_puzzle": 0x212,
  "shrine_dragon_bone": 0x218,
  "shrine_diary_chest": 0x219,
  "shrine_shawn": 0x21b,
  "xelpud_msx2": 0x21d,
  "slushfund_conversation": 0x228,
  "cog_puzzle": 0x23a,
  "cant_leave_conversation": 0x2e4,
  "msx2_found": 0x2e6,
  "xelpud_talisman": 0x327,
  "grail_tablet_surface": 0x54e,
  "starting_items": 0x84f,
  "replacement_surface_map_scan": 0x85f,
  "replacement_slushfund_conversation": 0x860,
  "rcd_filler_items": 0xc18,
  "dat_filler_items": 0xe0c
}

HEADERS = {
  "break": 0x000a,
  "flag": 0x0040,
  "flag2": 0x0041,
  "item": 0x0042,
  "pose": 0x0046,
  "mantra": 0x0047,
  "color": 0x004a,
  "item_name": 0x004d,
  "data": 0x004e,
  "anime": 0x004f
}

CARDS = {
  "slushfund_give_pepper": 245,
  "slushfund_give_anchor": 247,
  "xelpud_xmailer": 364,
  "xelpud_talisman": 369,
  "xelpud_pillar": 370,
  "xelpud_mulana_talisman": 371,
  "xelpud_conversation_tree": 480,
  "nebur_guardian": 490,
  "xelpud_howling_wind": 1049
}

RCD_OBJECTS = {
  "trigger_dais": 0x8,
  "moving_texture": 0xa,
  "flag_timer": 0xb,
  "room_spawner": 0xe,
  "crusher": 0x11,
  "hitbox_generator": 0x12,
  "lemeza_detector": 0x14,
  "chest": 0x2c,
  "naked_item": 0x2f,
  "texture_draw_animation": 0x93,
  "use_item": 0x9c,
  "scannable": 0x9e,
  "language_conversation": 0xa0,
  "instant_item": 0xb5,
  "scan": 0xc3
}

TEST_OPERATIONS = {
  "eq": 0,
  "lteq": 1,
  "gteq": 2
}

WRITE_OPERATIONS = {
  "assign": 0,
  "add": 1
}

def grail_flag_by_zone(zone, frontside):
  match zone:
    case 0:
      return GLOBAL_FLAGS["grail_tablet_guidance"]
    case 1:
      return GLOBAL_FLAGS["grail_tablet_surface"]
    case 2:
      return GLOBAL_FLAGS["grail_tablet_mausoleum"]
    case 3:
      return GLOBAL_FLAGS["grail_tablet_sun"]
    case 4:
      return GLOBAL_FLAGS["grail_tablet_spring"]
    case 5:
      return GLOBAL_FLAGS["grail_tablet_inferno"]
    case 6:
      return GLOBAL_FLAGS["grail_tablet_extinction"]
    case 7:
      if frontside:
        return GLOBAL_FLAGS["grail_tablet_twin_front"]
      else:
        return GLOBAL_FLAGS["grail_tablet_twin_back"]
    case 8:
      return GLOBAL_FLAGS["grail_tablet_endless"]
    case 9:
      return GLOBAL_FLAGS["grail_tablet_shrine_front"]
    case 10:
      return GLOBAL_FLAGS["grail_tablet_illusion"]
    case 11:
      return GLOBAL_FLAGS["grail_tablet_graveyard"]
    case 12:
      return GLOBAL_FLAGS["grail_tablet_moonlight"]
    case 13:
      return GLOBAL_FLAGS["grail_tablet_goddess"]
    case 14:
      return GLOBAL_FLAGS["grail_tablet_ruin"]
    case 15|16:
      return GLOBAL_FLAGS["grail_tablet_birth"]
    case 17:
      return GLOBAL_FLAGS["grail_tablet_dimensional"]
    case 18:
      return GLOBAL_FLAGS["grail_tablet_shrine_back"]
    case _:
      return 0xacf
