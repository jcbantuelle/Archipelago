from .FileMod import FileMod
from .Items import item_table
from .Rcd import Rcd
from .LmFlags import GLOBAL_FLAGS, RCD_OBJECTS, TEST_OPERATIONS, WRITE_OPERATIONS, CARDS, grail_flag_by_zone
from .Locations import get_locations_by_region

class RcdMod(FileMod):

  DEFAULT_PARAMS = {
    "param_index": 0,
    "iterations": 1,
    "item_mod": 0
  }

  RCD_OBJECT_PARAMS = dict([
      (RCD_OBJECTS["chest"], {
          "param_len": 7,
          "item_mod": 11
        },
      ),
      (RCD_OBJECTS["naked_item"], {
          "param_len": 4,
          "param_index": 1
        },
      ),
      (RCD_OBJECTS["instant_item"], {
          "param_len": 5
        },
      ),
      (RCD_OBJECTS["scan"], {
          "param_len": 5,
          "param_index": 3,
          "iterations": 2
        },
      )
    ]
  )

  def __init__(self, filename, local_config, options, start_inventory):
    super().__init__(Rcd, filename, local_config, options, GLOBAL_FLAGS["rcd_filler_items"])
    self.start_inventory = start_inventory

  def place_item_in_location(self, item, item_id, location) -> None:
    object_type_params = self.RCD_OBJECT_PARAMS.get(location.object_type)
    if object_type_params is None:
      return

    params = self.DEFAULT_PARAMS | object_type_params
    params["object_type"] = location.object_type
    params["item_id"] = item_id
    params["location"] = location
    params["item"] = item
    super().set_params(params)

    location_ids = [location.item_id]

    for zone in location.zones:
      screen = self.file_contents.zones[zone].rooms[location.room].screens[location.screen]
      params["objects"] = screen.objects_with_position

      if params["object_type"] == RCD_OBJECTS["chest"]:
        # Endless Corridor Twin Statue Chest Exists Twice
        if location.zones[0] == 8 and location.room == 3 and location.screen == 0 and location.item_id == item_table["Twin Statue"].game_code:
          params["iterations"] = 2
      elif params["object_type"] == RCD_OBJECTS["naked_item"]:
        # Endless Corridor Keysword Exists Twice, Once as Regular and Once as Empowered
        if location.zones[0] == 8 and location.room == 2 and location.screen == 1 and location.item_id == item_table["Key Sword"].game_code:
          location_ids.append(7)
      elif params["object_type"] == RCD_OBJECTS["scan"]:
        params["objects"] = screen.objects_without_position

      for location_id in location_ids:
        params["location_id"] = location_id
        self.__place_item(**params)

  def apply_mods(self, dat_mod):
    self.__give_starting_items(self.start_inventory)
    self.__rewrite_diary_chest()
    self.__add_diary_chest_timer()
    self.__rewrite_slushfund_conversation_conditions()
    self.__rewrite_four_guardian_shop_conditions(dat_mod)
    self.__rewrite_cog_chest()
    self.__rewrite_fishman_alt_shop()
    self.__clean_up_test_operations()

    if self.options.AutoScanGrailTablets:
      self.__create_grail_autoscans()

    if self.options.BossCheckpoints:
      self.__create_boss_checkpoints()

  # RCD Mod Methods

  def __place_item(self, objects, object_type, param_index, param_len, location, location_id, item_id, original_obtain_flag, new_obtain_flag, obtain_value, item_mod, iterations, item):
    for _ in range(iterations):
      location = next((o for _,o in enumerate(objects) if o.id == object_type and o.parameters[param_index] == location_id+item_mod and len(o.parameters) < param_len), None)

      for test_op in location.test_operations:
        if test_op.flag == original_obtain_flag:
          test_op.flag = new_obtain_flag
      for write_op in location.write_operations:
        if write_op.flag == original_obtain_flag:
          write_op.flag = new_obtain_flag
          if object_type == RCD_OBJECTS["naked_item"] or RCD_OBJECTS["instant_item"] or RCD_OBJECTS["scan"]:
            write_op.op_value = obtain_value

      self.__update_destructible_cover(objects, original_obtain_flag, new_obtain_flag)

      if original_obtain_flag == GLOBAL_FLAGS["surface_map"]:
        self.__fix_surface_map_scan(objects, location, original_obtain_flag)
      
      # Shrine of the Mother Map Crusher customization
      if original_obtain_flag == GLOBAL_FLAGS["shrine_map"]:
        self.__update_operation("write_operations", objects, RCD_OBJECTS["crusher"], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

      # Mausoleum Ankh Jewel Trap customization
      if original_obtain_flag == GLOBAL_FLAGS["ankh_jewel_mausoleum"]:
        self.__update_operation("write_operations", objects, RCD_OBJECTS["moving_texture"], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

      # Yagostr Dais customization
      if original_obtain_flag == GLOBAL_FLAGS["yagostr_found"]:
        self.__update_operation("test_operations", objects, RCD_OBJECTS["trigger_dais"], original_obtain_flag, new_obtain_flag)

      # Vimana customization
      if original_obtain_flag == GLOBAL_FLAGS["plane_found"]:
        vimana_objects = self.file_contents.zones[13].rooms[6].screens[1].objects_with_position
        self.__update_operation("test_operations", vimana_objects, RCD_OBJECTS["vimana"], original_obtain_flag, new_obtain_flag)

      location.parameters[param_index] = item_id+item_mod
      location.parameters.append(1)
      location.parameters_length += 1
      self.file_size += 2

  def __update_destructible_cover(self, objects, original_obtain_flag, new_obtain_flag):
    covers = [o for _, o in enumerate(objects) if o.id == RCD_OBJECTS["hitbox_generator"] or o.id == RCD_OBJECTS["room_spawner"] and len([t for t in o.test_operations if t.flag == original_obtain_flag]) > 0]
    for cover in covers:
      if cover is not None:
        for cover_test_op in cover.test_operations:
          if cover_test_op.flag == original_obtain_flag:
            cover_test_op.flag = new_obtain_flag
        for cover_write_op in cover.write_operations:
          if cover_write_op.flag == original_obtain_flag:
            cover_write_op.flag = new_obtain_flag

  def __fix_surface_map_scan(self, objects, location, obtain_flag):
    scan = next(o for _, o in enumerate(objects) if o.id == RCD_OBJECTS["scannable"] and len([t for t in o.test_operations if t.flag == obtain_flag]) > 0)
    surface_scan_flag = GLOBAL_FLAGS["replacement_surface_map_scan"]
    scan.test_operations[0].flag = surface_scan_flag
    scan.write_operations[0].flag = surface_scan_flag
    location.test_operations[0].flag = surface_scan_flag
    write_op_scan = Rcd.Operation()
    write_op_scan.flag = surface_scan_flag
    write_op_scan.operation = WRITE_OPERATIONS["add"]
    write_op_scan.op_value = 1
    location.write_operations.append(write_op_scan)
    location.write_operations_length += 1
    self.file_size += 4

  def __give_starting_items(self, items) -> None:
    flag_counter = 0
    for item_name in items:
      item = item_table[item_name]
      test_op = Rcd.Operation()
      test_op.flag = GLOBAL_FLAGS["starting_items"]
      test_op.operation = TEST_OPERATIONS["eq"]
      test_op.op_value = flag_counter

      write_op_given = Rcd.Operation()
      write_op_given.flag = GLOBAL_FLAGS["starting_items"]
      write_op_given.operation = WRITE_OPERATIONS["add"]
      write_op_given.op_value = 1

      write_op_item_flag = Rcd.Operation()
      write_op_item_flag.flag = item.obtain_flag
      write_op_item_flag.operation = WRITE_OPERATIONS["add"]
      write_op_item_flag.op_value = item.obtain_value

      item_id = item.game_code
      item_giver = Rcd.ObjectWithPosition()
      item_giver.id = RCD_OBJECTS["instant_item"]
      item_giver.test_operations_length = 1
      item_giver.write_operations_length = 2
      item_giver.parameters_length = 4
      item_giver.x_pos = 0
      item_giver.y_pos = 0
      item_giver.test_operations = [test_op]
      item_giver.write_operations = [write_op_given, write_op_item_flag]
      item_giver.parameters = [item_id,160,120,39]
      starting_room = self.file_contents.zones[1].rooms[2].screens[1]
      starting_room.objects_with_position.append(item_giver)
      starting_room.objects_length += 1
      self.file_size += 28
      flag_counter += 1

  def __rewrite_diary_chest(self) -> None:
    diary_location = next((location for _, location in enumerate(get_locations_by_region(None, None, None)["Shrine of the Mother [Main]"]) if location.name == "Shrine of the Mother - Diary Chest"), None)
    for zone_index in diary_location.zones:
      diary_screen = self.file_contents.zones[zone_index].rooms[diary_location.room].screens[diary_location.screen]
      diary_chest = next((o for _,o in enumerate(diary_screen.objects_with_position)
        if o.id == RCD_OBJECTS["chest"]), None)

      diary_shawn_test = next((test_op for _, test_op in enumerate(diary_chest.test_operations) if test_op.flag == GLOBAL_FLAGS["shrine_shawn"]), None)
      diary_shawn_test.flag = GLOBAL_FLAGS["shrine_dragon_bone"]
      diary_shawn_test.operation = TEST_OPERATIONS["eq"]
      diary_shawn_test.op_value = 1

      self.__add_operation_to_object("test_operations", diary_chest, GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["eq"], 2)

  def __add_diary_chest_timer(self) -> None:
    screen = self.file_contents.zones[9].rooms[2].screens[0]
  
    talisman_found_test = Rcd.Operation()
    talisman_found_test.flag = GLOBAL_FLAGS["talisman_found"]
    talisman_found_test.operation = TEST_OPERATIONS["gteq"]
    talisman_found_test.op_value = 3

    shrine_dragon_bone_test = Rcd.Operation()
    shrine_dragon_bone_test.flag = GLOBAL_FLAGS["shrine_dragon_bone"]
    shrine_dragon_bone_test.operation = TEST_OPERATIONS["gteq"]
    shrine_dragon_bone_test.op_value = 1

    write_op = Rcd.Operation()
    write_op.flag = GLOBAL_FLAGS["shrine_diary_chest"]
    write_op.operation = WRITE_OPERATIONS["assign"]
    write_op.op_value = 2

    flag_timer = Rcd.ObjectWithoutPosition()
    flag_timer.id = RCD_OBJECTS["flag_timer"]
    flag_timer.test_operations_length = 2
    flag_timer.write_operations_length = 1
    flag_timer.parameters_length = 2
    flag_timer.test_operations = [talisman_found_test, shrine_dragon_bone_test]
    flag_timer.write_operations = [write_op]
    flag_timer.parameters = [0,0]
    
    screen.objects_without_position.append(flag_timer)
    screen.objects_length += 1
    screen.objects_without_position_length += 1
    self.file_size += 20

  def __rewrite_four_guardian_shop_conditions(self, dat_mod):
    msx2_replacement_flag = dat_mod.find_shop_flag("nebur_guardian", 0)
    objects = self.file_contents.zones[1].rooms[2].screens[0].objects_with_position
    self.__update_operation("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=0, new_op_value=3, new_operation=TEST_OPERATIONS["lteq"])
    self.__update_operation("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=1, new_op_value=4)
    self.__update_operation("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["msx2_found"], msx2_replacement_flag)

  def __rewrite_slushfund_conversation_conditions(self):
    objects = self.file_contents.zones[10].rooms[8].screens[0].objects_with_position
    self.__update_operation("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["slushfund_conversation"], GLOBAL_FLAGS["replacement_slushfund_conversation"])

  def __rewrite_cog_chest(self):
    objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
    self.__update_operation("write_operations", objects, RCD_OBJECTS["chest"], GLOBAL_FLAGS["cog_puzzle"], GLOBAL_FLAGS["replacement_cog_puzzle"])

    stray_fairy_door = self.__find_objects_by_operation("write_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["cog_puzzle"], operation=WRITE_OPERATIONS["assign"], op_value=3)[0]
    self.__add_operation_to_object("write_operations", stray_fairy_door, GLOBAL_FLAGS["replacement_cog_puzzle"], WRITE_OPERATIONS["assign"], 3)

  def __rewrite_fishman_alt_shop(self):
    screen = self.file_contents.zones[4].rooms[3].screens[3]
    objects = screen.objects_with_position
    
    # Persist Main Shop after Alt is Opened
    self.__update_operation("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["fishman_shop_puzzle"], GLOBAL_FLAGS["fishman_shop_puzzle"], old_op_value=2, new_operation=TEST_OPERATIONS["gteq"])

    # Relocate Alt Shop
    self.__update_position("test_operations", objects, RCD_OBJECTS["language_conversation"], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 76, op_value=3)

    # Relocate Fairy Keyspot trigger
    self.__update_position("test_operations", objects, RCD_OBJECTS["fairy_keyspot"], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 74)

    # Relocate Alt Shop Explosion
    self.__update_position("test_operations", objects, RCD_OBJECTS["explosion"], GLOBAL_FLAGS["screen_flag_0d"], 7, 76)

    # Add Alt Shop Door Graphic
    test_op_mother = Rcd.Operation()
    test_op_mother.flag = GLOBAL_FLAGS["mother_state"]
    test_op_mother.operation = TEST_OPERATIONS["neq"]
    test_op_mother.op_value = 3

    test_op_fishman_shop_puzzle = Rcd.Operation()
    test_op_fishman_shop_puzzle.flag = GLOBAL_FLAGS["fishman_shop_puzzle"]
    test_op_fishman_shop_puzzle.operation = TEST_OPERATIONS["eq"]
    test_op_fishman_shop_puzzle.op_value = 3

    fishman_alt_door = Rcd.ObjectWithPosition()
    fishman_alt_door.id = RCD_OBJECTS["texture_draw_animation"]
    fishman_alt_door.test_operations_length = 2
    fishman_alt_door.write_operations_length = 0
    fishman_alt_door.parameters_length = 24
    fishman_alt_door.x_pos = 9
    fishman_alt_door.y_pos = 76
    fishman_alt_door.test_operations = [test_op_mother, test_op_fishman_shop_puzzle]
    fishman_alt_door.write_operations = []
    
    fishman_alt_door.parameters = [
      -1, # 0 Layer
      0,  # 1 Image File
      260, # 2 Imagex
      0, # 3 Imagey
      40, # 4 dx
      40, # 5 dy
      0, # 6 animation
      1, # 7 Animation Frames
      0, # 8 Pause Frames
      0, # 9 Repeat Count (<1 is forever)
      0, # 10 Hittile to fill with
      0, # 11 Entry Effect
      0, # 12 Exit Effect
      0, # 13 Cycle Colors t/f
      0, # 14 Alpha/frame
      255, # 15 Max Alpha
      0, # 16 R/frame
      0, # 17 Max R
      0, # 18 G/frame
      0, # 19 Max G
      0, # 20 B/frame
      0, # 21 Max B
      0, # 22 blend. 0=Normal 1=add 2= ... 14=
      0, # 23 not0?
    ]
    objects.append(fishman_alt_door)
    screen.objects_length += 1
    
    self.file_size += 64 # 2 Ops (4*2=8) + Object (8) + 24 Params (2*24=48) = 8+8+48 = 64

  def __clean_up_test_operations(self):
    # Remove Fairy Conversation Requirement from Buer Room Ladder
    buer_objects = self.file_contents.zones[3].rooms[2].screens[1].objects_with_position
    self.__remove_operation("test_operations", buer_objects, RCD_OBJECTS["hitbox_generator"], GLOBAL_FLAGS["endless_fairyqueen"])

		# Remove Slushfund Conversation Requirement from Pepper Puzzle
    pepper_puzzle_objects = self.file_contents.zones[0].rooms[0].screens[0].objects_with_position
    self.__remove_operation("test_operations", pepper_puzzle_objects, RCD_OBJECTS["use_item"], GLOBAL_FLAGS["slushfund_conversation"])

    # Remove Crucifix Check from Crucifix Puzzle Torches
    crucifix_puzzle_objects = self.file_contents.zones[0].rooms[1].screens[1].objects_with_position
    self.__remove_operation("test_operations", crucifix_puzzle_objects, RCD_OBJECTS["texture_draw_animation"], GLOBAL_FLAGS["crucifix_found"])

    # Remove Cog Puzzle Requirement from Mudmen Activation
    mudmen_activation_objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
    self.__remove_operation("test_operations", mudmen_activation_objects, RCD_OBJECTS["use_item"], GLOBAL_FLAGS["cog_puzzle"])

    # Remove Plane Missing Requirement from Plane Puzzle
    plane_platform_left_objects = self.file_contents.zones[13].rooms[7].screens[0].objects_with_position
    self.__remove_operation("test_operations", plane_platform_left_objects, RCD_OBJECTS["counterweight_platform"], GLOBAL_FLAGS["plane_found"])
    plane_platform_right_objects = self.file_contents.zones[13].rooms[7].screens[2].objects_with_position
    self.__remove_operation("test_operations", plane_platform_right_objects, RCD_OBJECTS["counterweight_platform"], GLOBAL_FLAGS["plane_found"])


  def __create_grail_autoscans(self) -> None:
    for zone in self.file_contents.zones:
      for room in zone.rooms:
        for screen in room.screens:
          for obj in screen.objects_with_position:
            if obj.id == RCD_OBJECTS["scannable"]:
              language_block = obj.parameters[0]
              frontside = language_block == 41 or language_block == 75 or language_block == 104 or language_block == 136 or language_block == 149 or language_block == 170 or language_block == 188 or language_block == 221 or (language_block == 231 and zone.zone_index == 9)
              backside = language_block == 250 or language_block == 275 or language_block == 291 or language_block == 305 or language_block == 323 or language_block == 339 or language_block == 206 or language_block == 358 or (language_block == 231 and zone.zone_index != 9)

              if frontside or backside:
                grail_flag = grail_flag_by_zone(zone.zone_index, frontside)

                test_op = self.__generate_op(grail_flag, 0, TEST_OPERATIONS["eq"])
                write_op = self.__generate_op(grail_flag, 1, WRITE_OPERATIONS["assign"])

                params = [0,0,0,0,2,3]
                lemeza_detector = self.__generate_object_with_position(RCD_OBJECTS["lemeza_detector"], obj.x_pos, obj.y_pos - 1, [test_op], [write_op], params)

                screen.objects_with_position.append(lemeza_detector)
                screen.objects_length += 1

                self.file_size += 28

  def __create_boss_checkpoints(self) -> None:
    # Amphisbaena
    amphisbaena_screen = self.file_contents.zones[0].rooms[8].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["amphisbaena_ankh_puzzle"], 5, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["amphisbaena_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [41, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 15, 44, test_ops, write_ops, params)

    amphisbaena_screen.objects_with_position.append(autosave)
    amphisbaena_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Sakit
    sakit_screen = self.file_contents.zones[2].rooms[8].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["sakit_ankh_puzzle"], 1, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["sakit_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [75, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 45, 6, test_ops, write_ops, params)

    sakit_screen.objects_with_position.append(autosave)
    sakit_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Ellmac
    ellmac_screen = self.file_contents.zones[3].rooms[8].screens[0]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["ellmac_ankh_puzzle"], 5, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["ellmac_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [104, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 20, 16, test_ops, write_ops, params)

    ellmac_screen.objects_with_position.append(autosave)
    ellmac_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Bahamut
    bahamut_screen = self.file_contents.zones[4].rooms[4].screens[0]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["bahamut_ankh_puzzle"], 1, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["bahamut_room_flooded"], 1, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["bahamut_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [136, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 19, 17, test_ops, write_ops, params)

    bahamut_screen.objects_with_position.append(autosave)
    bahamut_screen.objects_length += 1

    self.file_size += 50 # 6 Ops (4*6=24) + Object (8) + 9 Params (2*9=18) = 24+8+18 = 50

    # Viy
    viy_screen = self.file_contents.zones[5].rooms[8].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["viy_ankh_puzzle"], 4, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["viy_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [149, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 23, 28, test_ops, write_ops, params)

    viy_screen.objects_with_position.append(autosave)
    viy_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Palenque
    palenque_screen = self.file_contents.zones[6].rooms[9].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["palenque_ankh_puzzle"], 3, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["palenque_screen_mural"], 3, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["palenque_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [170, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 47, 20, test_ops, write_ops, params)

    palenque_screen.objects_with_position.append(autosave)
    palenque_screen.objects_length += 1

    self.file_size += 50 # 6 Ops (4*6=24) + Object (8) + 9 Params (2*9=18) = 24+8+18 = 50

    # Baphomet
    baphomet_screen = self.file_contents.zones[7].rooms[4].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["baphomet_ankh_puzzle"], 2, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["baphomet_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [188, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 47, 4, test_ops, write_ops, params)

    baphomet_screen.objects_with_position.append(autosave)
    baphomet_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Tiamat
    tiamat_screen = self.file_contents.zones[17].rooms[9].screens[0]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["tiamat_ankh_puzzle"], 1, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["tiamat_state"], 2, TEST_OPERATIONS["lt"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [368, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 15, 4, test_ops, write_ops, params)

    tiamat_screen.objects_with_position.append(autosave)
    tiamat_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

    # Mother
    mother_screen = self.file_contents.zones[18].rooms[3].screens[1]

    test_ops = [
      self.__generate_op(GLOBAL_FLAGS["mother_ankh_puzzle"], 1, TEST_OPERATIONS["gteq"]),
      self.__generate_op(GLOBAL_FLAGS["mother_state"], 2, TEST_OPERATIONS["lteq"]),
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 0, TEST_OPERATIONS["eq"]),
      self.__generate_op(GLOBAL_FLAGS["escape"], 0, TEST_OPERATIONS["eq"])
    ]

    write_ops = [
      self.__generate_op(GLOBAL_FLAGS["screen_flag_02"], 1, WRITE_OPERATIONS["assign"])
    ]

    params = [231, 0, 0, 1, 1, 1, 1, 506, 280]
    autosave = self.__generate_object_with_position(RCD_OBJECTS["grail_point"], 33, 20, test_ops, write_ops, params)

    mother_screen.objects_with_position.append(autosave)
    mother_screen.objects_length += 1

    self.file_size += 46 # 5 Ops (4*5=20) + Object (8) + 9 Params (2*9=18) = 20+8+18 = 46

  # Utility Methods

  # Generate methods

  def __generate_op(self, flag, op_value, op_type):
    op = Rcd.Operation()
    op.flag = flag
    op.op_value = op_value
    op.operation = op_type
    return op

  def __generate_object_with_position(self, object_id, x_pos, y_pos, test_ops, write_ops, params):
    obj_with_pos = Rcd.ObjectWithPosition()
    obj_with_pos.id = object_id
    obj_with_pos.test_operations = test_ops
    obj_with_pos.test_operations_length = len(test_ops)

    obj_with_pos.write_operations = write_ops
    obj_with_pos.write_operations_length = len(write_ops)

    obj_with_pos.parameters = params
    obj_with_pos.parameters_length = len(params)

    obj_with_pos.x_pos = x_pos
    obj_with_pos.y_pos = y_pos

    return obj_with_pos

  # Search Methods

  def __find_objects_by_operation(self, op_type, objects, object_id, flag, operation=None, op_value=None):
    return [o for _, o in enumerate(objects) if o.id == object_id and len([op for op in getattr(o, op_type) if self.__op_matches(op, flag, operation, op_value)]) > 0]

  def __find_operation_index(self, ops, flag, operation=None, op_value=None):
    return next(i for i,op in enumerate(ops) if self.__op_matches(op, flag, operation, op_value))

  # Conditionals

  def __op_matches(self, op, flag, operation, op_value):
    return op.flag == flag and (operation is None or op.operation == operation) and (op_value is None or op.op_value == op_value)

  # Write Methods

  def __update_position(self, op_type, objects, object_id, flag, x_pos, y_pos, operation=None, op_value=None):
    objs = self.__find_objects_by_operation(op_type, objects, object_id, flag, operation, op_value)

    for obj in objs:
      obj.x_pos = x_pos
      obj.y_pos = y_pos

  def __update_operation(self, op_type, objects, object_id, old_flag, new_flag, old_operation=None, new_operation=None, old_op_value=None, new_op_value=None):
    objs = self.__find_objects_by_operation(op_type, objects, object_id, old_flag, old_operation, old_op_value)

    for obj in objs:
      ops = getattr(obj, op_type)
      op_index = self.__find_operation_index(ops, old_flag, old_operation, old_op_value)
      
      op = getattr(obj, op_type)[op_index]
      op.flag = new_flag
      if new_operation is not None:
        op.operation = new_operation
      if new_op_value is not None:
        op.op_value = new_op_value

  def __remove_operation(self, op_type, objects, object_id, flag):
    objs = self.__find_objects_by_operation(op_type, objects, object_id, flag)

    for obj in objs:
      ops = getattr(obj, op_type)
      op_index = self.__find_operation_index(ops, flag)
      
      del ops[op_index]
      op_type_len = op_type + "_length"
      old_len = getattr(obj, op_type_len)
      setattr(obj, op_type_len, old_len-1)
      self.file_size -= 4

  def __add_operation_to_object(self, op_type, obj, flag, operation, op_value):
    op = Rcd.Operation()
    op.flag = flag
    op.operation = operation
    op.op_value = op_value

    ops = getattr(obj, op_type)
    ops.append(op)

    op_type_len = op_type + "_length"
    old_len = getattr(obj, op_type_len)
    setattr(obj, op_type_len, old_len+1)
    self.file_size += 4
