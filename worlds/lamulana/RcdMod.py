from .FileMod import FileMod
from .Items import item_table
from .Rcd import Rcd
from .LmFlags import GLOBAL_FLAGS, RCD_OBJECTS, TEST_OPERATIONS, WRITE_OPERATIONS, grail_flag_by_zone
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

  def __init__(self, filename):
    super().__init__(Rcd, filename)
    self.filler_flags = 0xc18

  def place_item_in_location(self, item, item_id, location) -> None:
    for zone in location.zones:
      object_type_params = self.RCD_OBJECT_PARAMS.get(location.object_type)
      if object_type_params is None:
        continue

      screen = self.file_contents.zones[zone].rooms[location.room].screens[location.screen]
      location_ids = [location.item_id]

      params = self.DEFAULT_PARAMS | object_type_params
      params["objects"] = screen.objects_with_position
      params["object_type"] = location.object_type
      params["item_id"] = item_id

      if params["object_type"] == RCD_OBJECTS["chest"]:
        # Endless Corridor Twin Statue Chest Exists Twice
        if location.zones[0] == 8 and location.room == 3 and location.screen == 0 and location.item_id == 59:
          params["iterations"] = 2
      elif params["object_type"] == RCD_OBJECTS["naked_item"]:
        # Endless Corridor Keysword Exists Twice, Once as Regular and Once as Empowered
        if location.zones[0] == 8 and location.room == 2 and location.screen == 1 and location.item_id == 4:
          location_ids.append(7)
      elif params["object_type"] == RCD_OBJECTS["scan"]:
        params["objects"] = screen.objects_without_position

      params["original_obtain_flag"] = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
      if item.obtain_flag is not None:
        params["new_obtain_flag"] = item.obtain_flag
      else:
        params["new_obtain_flag"] = self.filler_flags
        self.filler_flags += 1
      params["obtain_value"] = item.obtain_value if item.obtain_value is not None else location.obtain_value
      for location_id in location_ids:
        params["location_id"] = location_id
        self.place_item(**params)

  def create_grail_autoscans(self) -> None:
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

  def rewrite_diary_chest(self) -> None:
    diary_location = next((location for _, location in enumerate(get_locations_by_region(None, None, None)["Shrine of the Mother [Main]"]) if location.name == "Shrine of the Mother - Diary Chest"), None)
    for zone_index in diary_location.zones:
      diary_screen = self.file_contents.zones[zone_index].rooms[diary_location.room].screens[diary_location.screen]
      diary_chest = next((o for _,o in enumerate(diary_screen.objects_with_position)
        if o.id == RCD_OBJECTS["chest"]), None)

      diary_shawn_test = next((test_op for _, test_op in enumerate(diary_chest.test_operations) if test_op.flag == GLOBAL_FLAGS["shrine_shawn"]), None)
      diary_shawn_test.flag = GLOBAL_FLAGS["shrine_dragon_bone"]
      diary_shawn_test.operation = TEST_OPERATIONS["eq"]
      diary_shawn_test.op_value = 1

      self.add_test_to_object(diary_chest, GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["eq"], 2)

  def add_diary_chest_timer(self) -> None:
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

  def give_starting_items(self, items) -> None:
    flag_counter = 0
    for item_name in items:
      test_op = Rcd.Operation()
      test_op.flag = GLOBAL_FLAGS["starting_items"]
      test_op.operation = TEST_OPERATIONS["eq"]
      test_op.op_value = flag_counter

      write_op = Rcd.Operation()
      write_op.flag = GLOBAL_FLAGS["starting_items"]
      write_op.operation = WRITE_OPERATIONS["add"]
      write_op.op_value = 1

      item_id = item_table[item_name].game_code
      item_giver = Rcd.ObjectWithPosition()
      item_giver.id = RCD_OBJECTS["instant_item"]
      item_giver.test_operations_length = 1
      item_giver.write_operations_length = 1
      item_giver.parameters_length = 4
      item_giver.x_pos = 0
      item_giver.y_pos = 0
      item_giver.test_operations = [test_op]
      item_giver.write_operations = [write_op]
      item_giver.parameters = [item_id,160,120,39]
      starting_room = self.file_contents.zones[1].rooms[2].screens[1]
      starting_room.objects_with_position.append(item_giver)
      starting_room.objects_length += 1
      self.file_size += 24
      flag_counter += 1

  def place_item(self, objects, object_type, param_index, param_len, location_id, item_id, original_obtain_flag, new_obtain_flag, obtain_value, item_mod, iterations):
    for _ in range(iterations):
      location = next((o for _,o in enumerate(objects) if o.id == object_type and o.parameters[param_index] == location_id+item_mod and len(o.parameters) < param_len), None)

      for test_op in location.test_operations:
        if test_op.flag == original_obtain_flag:
          test_op.flag = new_obtain_flag
      for write_op in location.write_operations:
        if write_op.flag == original_obtain_flag:
          write_op.flag = new_obtain_flag
          if object_type == RCD_OBJECTS["chest"]:
            location.write_operations[3].op_value = obtain_value
          elif object_type == RCD_OBJECTS["naked_item"] or RCD_OBJECTS["instant_item"] or RCD_OBJECTS["scan"]:
            write_op.value = obtain_value

      location.parameters[param_index] = item_id+item_mod
      location.parameters.append(1)
      location.parameters_length += 1
      self.file_size += 2

  def add_test_to_object(self, rcd_object, flag, operation, value):
    test_op = Rcd.Operation()
    test_op.flag = flag
    test_op.operation = operation
    test_op.op_value = value

    rcd_object.test_operations.append(test_op)
    rcd_object.test_operations_length += 1
    self.file_size += 4
