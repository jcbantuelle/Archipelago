GLOBAL_FLAGS = {
  "xmailer": 0x0e3,
  "grail_tablet_guidance": 0x064,
  "grail_tablet_mausoleum": 0x065,
  "grail_tablet_sun": 0x066,
  "grail_tablet_spring": 0x067,
  "grail_tablet_inferno": 0x068,
  "grail_tablet_extinction": 0x069,
  "grail_tablet_twin_front": 0x06a,
  "grail_tablet_endless": 0x06b,
  "grail_tablet_shrine_front": 0x06c,
  "grail_tablet_illusion": 0x06d,
  "grail_tablet_graveyard": 0x06e,
  "grail_tablet_moonlight": 0x06f,
  "grail_tablet_goddess": 0x070,
  "grail_tablet_ruin": 0x071,
  "grail_tablet_birth": 0x072,
  "grail_tablet_twin_back": 0x073,
  "grail_tablet_dimensional": 0x074,
  "grail_tablet_shrine_back": 0x075,
  "mulana_talisman": 0x105,
  "diary_chest_puzzle": 0x212,
  "shrine_dragon_bone": 0x218,
  "shrine_diary_chest": 0x219,
  "shrine_shawn": 0x21b,
  "cant_leave_conversation": 0x2e4,
  "xelpud_talisman": 0x327,
  "grail_tablet_surface": 0x54e,
  "starting_items": 0x84f,
  "diary_found": 0x850,
  "talisman_found": 0x851
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
  "xelpud_xmailer": 364,
  "xelpud_talisman": 369,
  "xelpud_pillar": 370,
  "xelpud_mulana_talisman": 371,
  "xelpud_conversation_tree": 480,
  "xelpud_howling_wind": 1049
}

RCD_OBJECTS = {
  "flag_timer": 0x0b,
  "hitbox_generator": 0x12,
  "lemeza_detector": 0x14,
  "chest": 0x2c,
  "naked_item": 0x2f,
  "scannable": 0x9e,
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
