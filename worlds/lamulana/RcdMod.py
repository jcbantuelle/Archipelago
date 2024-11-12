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
    self.__clean_up_test_operations()

    if self.options.AutoScanGrailTablets:
      self.__create_grail_autoscans()

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
          if object_type == RCD_OBJECTS["chest"]:
            location.write_operations[0].op_value = obtain_value
            location.write_operations[3].op_value = obtain_value
          elif object_type == RCD_OBJECTS["naked_item"] or RCD_OBJECTS["instant_item"] or RCD_OBJECTS["scan"]:
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

                test_op = Rcd.Operation()
                test_op.flag = grail_flag
                test_op.operation = TEST_OPERATIONS["eq"]
                test_op.op_value = 0

                write_op = Rcd.Operation()
                write_op.flag = grail_flag
                write_op.operation = WRITE_OPERATIONS["assign"]
                write_op.op_value = 1

                lemeza_detector = Rcd.ObjectWithPosition()
                lemeza_detector.id = RCD_OBJECTS["lemeza_detector"]
                lemeza_detector.test_operations_length = 1
                lemeza_detector.write_operations_length = 1
                lemeza_detector.parameters_length = 6
                lemeza_detector.x_pos = obj.x_pos
                lemeza_detector.y_pos = obj.y_pos - 1
                lemeza_detector.test_operations = [test_op]
                lemeza_detector.write_operations = [write_op]
                lemeza_detector.parameters = [0,0,0,0,2,3]

                screen.objects_with_position.append(lemeza_detector)
                screen.objects_length += 1

                self.file_size += 28

  # Utility Methods

  # Search Methods

  def __find_objects_by_operation(self, op_type, objects, object_id, flag, operation=None, op_value=None):
    return [o for _, o in enumerate(objects) if o.id == object_id and len([op for op in getattr(o, op_type) if self.__op_matches(op, flag, operation, op_value)]) > 0]

  def __find_operation_index(self, ops, flag, operation=None, op_value=None):
    return next(i for i,op in enumerate(ops) if self.__op_matches(op, flag, operation, op_value))

  # Conditionals

  def __op_matches(self, op, flag, operation, op_value):
    return op.flag == flag and (operation is None or op.operation == operation) and (op_value is None or op.op_value == op_value)

  # Write Methods

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
