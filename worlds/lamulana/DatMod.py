from .FileMod import FileMod
from .Dat import Dat
from .LmFlags import GLOBAL_FLAGS, HEADERS, CARDS

class DatMod(FileMod):

  def __init__(self, filename, local_config):
    super().__init__(Dat, filename, local_config)
    self.filler_flags = 0xe0c

  def place_item_in_location(self, item, item_id, location) -> None:
    params = {
      "item_id": item_id,
      "location": location,
      "item": item
    }
    params["original_obtain_flag"] = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
    if item_id == 38 or item_id == 83 or item_id == 69 or item.obtain_flag is None:
      params["new_obtain_flag"] = self.filler_flags
      self.filler_flags += 1
    else:
      params["new_obtain_flag"] = item.obtain_flag

    params["obtain_value"] = item.obtain_value if item.obtain_value is not None else location.obtain_value

    for card_index in location.cards:
      params["entries"] = self.file_contents.cards[card_index].contents.entries

      if location.slot is None:
        self.place_conversation_item(**params)
        if card_index == CARDS["xelpud_xmailer"]:
          self.update_xelpud_xmailer_flag(params["new_obtain_flag"])
      else:
        self.place_shop_item(**params)
    self.local_config.add_item(params)

  def place_conversation_item(self, entries, item_id, location, item, original_obtain_flag, new_obtain_flag, obtain_value):
    item_index = next((i for i,v in enumerate(entries) if v.header == HEADERS["item"] and v.contents.value == location.item_id), None)
    entries[item_index].contents.value = item_id

    flag_index = next((i for i,v in enumerate(entries) if v.header == HEADERS["flag"] and v.contents.address == original_obtain_flag), None)
    entries[flag_index].contents.address = new_obtain_flag
    entries[flag_index].contents.value = obtain_value

  def place_shop_item(self, entries, item_id, location, item, original_obtain_flag, new_obtain_flag, obtain_value):
    # Override Other Player Item to Map if in a Shop to prevent quantity from selling out
    if item_id == 83:
      item_id = 70
    data_indices = [i for i,v in enumerate(entries) if v.header == HEADERS["data"]]
    entries[data_indices[0]].contents.values[location.slot] = item_id
    item_cost = item.cost if item.cost is not None else 10
    entries[data_indices[1]].contents.values[location.slot] = item_cost
    entries[data_indices[2]].contents.values[location.slot] = item.quantity
    entries[data_indices[3]].contents.values[location.slot] = new_obtain_flag
    if obtain_value > 1:
      entries[data_indices[6]].contents.values[location.slot] = new_obtain_flag

  def rewrite_xelpud_flag_checks(self) -> None:
    card = self.card("xelpud_conversation_tree")

    entries_to_remove = [
      CARDS["xelpud_howling_wind"],
      CARDS["xelpud_xmailer"],
      CARDS["xelpud_pillar"],
      CARDS["xelpud_mulana_talisman"]
    ]
    for entry_value in entries_to_remove:
      self.remove_data_entry_by_value(card, entry_value)

    data_values_to_add = [
      [GLOBAL_FLAGS["diary_found"], 1, CARDS["xelpud_mulana_talisman"], 0],
      [GLOBAL_FLAGS["talisman_found"], 2, CARDS["xelpud_pillar"], 0],
      [GLOBAL_FLAGS["talisman_found"], 1, CARDS["xelpud_talisman"], 0],
      [GLOBAL_FLAGS["xmailer"], 0, CARDS["xelpud_xmailer"], 0]
    ]
    for data_values in data_values_to_add:
      self.add_data_entry(card, data_values)

  def update_xelpud_xmailer_flag(self, new_flag):
    card = self.card("xelpud_conversation_tree")
    entries = card.contents.entries

    for entry in entries:
      if entry.header == HEADERS["data"] and entry.contents.values[0] == GLOBAL_FLAGS["xmailer"]:
        entry.contents.values[0] = new_flag
        break

  def rewrite_xelpud_mulana_talisman_conversation(self) -> None:
    card = self.card("xelpud_mulana_talisman")
    entries = card.contents.entries

    talisman_flag_entries = [(i, entry) for i, entry in enumerate(entries)
      if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["mulana_talisman"]
    ]
    for _, flag_entry in talisman_flag_entries:
      flag_entry.contents.address = GLOBAL_FLAGS["diary_found"]
      flag_entry.contents.value = 2

    insert_index = max([i for i,_ in talisman_flag_entries])
    self.add_flag_entry(card, insert_index, GLOBAL_FLAGS["mulana_talisman"], 2)

    diary_puzzle_index = next((i for i, entry in enumerate(entries)
      if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["diary_chest_puzzle"]
    ), None)
    self.remove_flag_entry(card, diary_puzzle_index)

  def rewrite_xelpud_talisman_conversation(self) -> None:
    card = self.card("xelpud_talisman")
    entries = card.contents.entries

    insert_index = max([i for i,entry in enumerate(entries)
      if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["cant_leave_conversation"]
    ])

    self.add_flag_entry(card, insert_index, GLOBAL_FLAGS["talisman_found"], 2)
    self.add_flag_entry(card, insert_index, GLOBAL_FLAGS["xelpud_talisman"], 1)

  def rewrite_xelpud_pillar_conversation(self) -> None:
    card = self.card("xelpud_pillar")
    entries = card.contents.entries

    diary_chest_flag_index = next((i for i,entry in enumerate(entries)
      if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["shrine_diary_chest"]
    ), None)
  
    self.remove_flag_entry(card, diary_chest_flag_index)

    insert_index = max([i for i,entry in enumerate(entries)
      if entry.header == HEADERS["flag"] and entry.contents.address == GLOBAL_FLAGS["cant_leave_conversation"]
    ])
  
    self.add_flag_entry(card, insert_index, GLOBAL_FLAGS["talisman_found"], 3)

  def card(self, card_name):
    card_index = CARDS[card_name]
    return self.file_contents.cards[card_index]

  def remove_data_entry_by_value(self, card, value):
    entries = card.contents.entries
    entry_index = next((i for i,v in enumerate(entries) if v.header == HEADERS["data"] and v.contents.values[2] == value), None)
    next_index_to_delete = entry_index + 2

    size = 6 + (entries[entry_index].contents.num_values * 2)
    # Final Entry doesn't have a break after it
    if entry_index == (len(entries) - 1):
      size -= 2
      next_index_to_delete -= 1

    del entries[entry_index:next_index_to_delete]
    self.file_size -= size
    card.len_contents -= size

  def add_data_entry(self, card, data_values):
    entries = card.contents.entries
    break_entry = Dat.Entry()
    break_entry.header = HEADERS["break"]
    break_entry.contents = Dat.Noop()
    break_entry.contents.no_value = bytearray()

    data = Dat.Data()
    data.num_values = len(data_values)
    data.values = data_values

    data_entry = Dat.Entry()
    data_entry.header = HEADERS["data"]
    data_entry.contents = data

    entries.append(break_entry)
    entries.append(data_entry)

    file_mod = (6 + (data.num_values * 2))
    self.file_size += file_mod
    card.len_contents += file_mod

  def add_flag_entry(self, card, index, address, value):
    entries = card.contents.entries
    flag = Dat.Flag()
    flag.address = address
    flag.value = value

    flag_entry = Dat.Entry()
    flag_entry.header = HEADERS["flag"]
    flag_entry.contents = flag

    entries.insert(index, flag_entry)

    self.file_size += 6
    card.len_contents += 6

  def remove_flag_entry(self, card, index):
    entries = card.contents.entries
    if index is not None:
      del entries[index]
      self.file_size -= 6
      card.len_contents -= 6
