from .FileMod import FileMod
from .Items import item_table
from .Rcd import Rcd

class RcdMod(FileMod):

  STARTING_ITEMS_FLAG = 0x84f

  DEFAULT_PARAMS = {
    "param_index": 0,
    "iterations": 1,
    "item_mod": 0
  }

  OBJECT_TYPES = dict([
      (0x2c, {
          "param_len": 7,
          "item_mod": 11
        },
      ),
      (0x2f, {
          "param_len": 4,
          "param_index": 1
        },
      ),
      (0xb5, {
          "param_len": 5
        },
      ),
      (0xc3, {
          "param_len": 5,
          "param_index": 3,
          "iterations": 2
        },
      )
    ]
  )

  def __init__(self, filename):
    super().__init__(Rcd, filename)

  def place_item_in_location(self, item, item_id, location) -> None:
    for zone in location.zones:
      object_type_params = self.OBJECT_TYPES.get(location.object_type)
      if object_type_params is None:
        continue

      screen = self.file_contents.zones[zone].rooms[location.room].screens[location.screen]
      location_ids = [location.item_id]

      params = self.DEFAULT_PARAMS | object_type_params
      params["objects"] = screen.objects_with_position
      params["object_type"] = location.object_type
      params["item_id"] = item_id

      match params["object_type"]:
        case 0x2c:
          # Endless Corridor Twin Statue Chest Exists Twice
          if location.zones[0] == 8 and location.room == 3 and location.screen == 0 and location.item_id == 59:
            params["iterations"] = 2
        case 0x2f:
          # Endless Corridor Keysword Exists Twice, Once as Regular and Once as Empowered
          if location.zones[0] == 8 and location.room == 2 and location.screen == 1 and location.item_id == 4:
            location_ids.append(7)
        case 0xc3:
          params["objects"] = screen.objects_without_position

      params["original_obtain_flag"] = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
      params["new_obtain_flag"] = item.obtain_flag if item.obtain_flag is not None else location.obtain_flag
      params["obtain_value"] = item.obtain_value if item.obtain_value is not None else location.obtain_value
      for location_id in location_ids:
        params["location_id"] = location_id
        self.place_item(**params)

  def give_starting_items(self, items) -> None:
    flag_counter = 0
    for item_name in items:
      test_op = Rcd.Operation()
      test_op.flag = self.STARTING_ITEMS_FLAG
      test_op.op_value = flag_counter
      test_op.operation = 0

      write_op = Rcd.Operation()
      write_op.flag = self.STARTING_ITEMS_FLAG
      write_op.op_value = 1
      write_op.operation = 1

      item_id = item_table[item_name].game_code
      item_giver = Rcd.ObjectWithPosition()
      item_giver.id = 0xb5
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
    o = enumerate(objects)
    for _ in range(iterations):
      o_index = next((i for i,v in o if v.id == object_type and v.parameters[param_index] == location_id+item_mod and len(v.parameters) < param_len), None)
      location = objects[o_index]

      for test_op in location.test_operations:
        if test_op.flag == original_obtain_flag:
          test_op.flag = new_obtain_flag
      for write_op in location.write_operations:
        if write_op.flag == original_obtain_flag:
          write_op.flag = new_obtain_flag
          if object_type == 0x2c:
            location.write_operations[3].op_value = obtain_value
          elif object_type == 0x2f or 0xb5 or 0xc3:
            write_op.value = obtain_value

      location.parameters[param_index] = item_id+item_mod
      location.parameters.append(1)
      location.parameters_length += 1
      self.file_size += 2
