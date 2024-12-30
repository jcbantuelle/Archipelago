GLOBAL_FLAGS = {
    "screen_flag_02": 0x02,
    "screen_flag_0d": 0x0d,
    "talisman_found": 0xa4,
    "crucifix_found": 0xab,
    "plane_found": 0xb4,
    "surface_map": 0xd1,
    "shrine_map": 0xda,
    "xmailer": 0xe3,
    "mekuri": 0xf1,
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
    "amphisbaena_state": 0xf6,
    "sakit_state": 0xf7,
    "ellmac_state": 0xf8,
    "bahamut_state": 0xf9,
    "viy_state": 0xfa,
    "palenque_state": 0xfb,
    "baphomet_state": 0xfc,
    "tiamat_state": 0xfd,
    "mother_state": 0xfe,
    "guardians_killed": 0x102,
    "diary_found": 0x104,
    "mulana_talisman": 0x105,
    "amphisbaena_ankh_puzzle": 0x133,
    "sakit_ankh_puzzle": 0x164,
    "ellmac_ankh_puzzle": 0x178,
    "fishman_shop_puzzle": 0x197,
    "bahamut_room_flooded": 0x199,
    "bahamut_ankh_puzzle": 0x19f,
    "viy_ankh_puzzle": 0x1b4,
    "palenque_ankh_puzzle": 0x1c3,
    "palenque_screen_mural": 0x1ca,
    "baphomet_ankh_puzzle": 0x1e0,
    "endless_fairyqueen": 0x1f5,
    "diary_chest_puzzle": 0x212,
    "shrine_dragon_bone": 0x218,
    "shrine_diary_chest": 0x219,
    "shrine_shawn": 0x21b,
    "xelpud_msx2": 0x21d,
    "slushfund_conversation": 0x228,
    "cog_puzzle": 0x23a,
    "cant_leave_conversation": 0x2e4,
    "translation_tablets_read": 0x2e5,
    "msx2_found": 0x2e6,
    "ancient_lamulanese_learned": 0x2ea,
    "tiamat_ankh_puzzle": 0x2ed,
    "mother_ankh_puzzle": 0x2e0,
    "xelpud_talisman": 0x327,
    "mulbruk_father": 0x34c,
    "escape": 0x382,
    "grail_tablet_surface": 0x54e,
    "starting_items": 0x84f,
    "replacement_surface_map_scan": 0x85f,
    "replacement_slushfund_conversation": 0x860,
    "replacement_cog_puzzle": 0x861,
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
    "counterweight_platform": 0x33,
    "chest": 0x2c,
    "naked_item": 0x2f,
    "vimana": 0x71,
    "texture_draw_animation": 0x93,
    "use_item": 0x9c,
    "scannable": 0x9e,
    "grail_point": 0x9f,
    "language_conversation": 0xa0,
    "fairy_keyspot": 0xa7,
    "explosion": 0xb4,
    "instant_item": 0xb5,
    "scan": 0xc3
}

TEST_OPERATIONS = {
    "eq": 0x0,
    "lteq": 0x1,
    "gteq": 0x2,
    "andnz": 0x3,
    "ornz": 0x4,
    "xornz": 0x5,
    "zero": 0x6,
    "neq": 0x40,
    "gt": 0x41,
    "lt": 0x42,
    "andz": 0x43,
    "orz": 0x44,
    "xorz": 0x45,
    "nz": 0x46
}

WRITE_OPERATIONS = {
    "assign": 0x0,
    "add": 0x1,
    "sub": 0x2,
    "mult": 0x3,
    "div": 0x4,
    "and": 0x5,
    "or": 0x6,
    "xor": 0x7
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
