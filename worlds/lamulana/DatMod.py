from .FileMod import FileMod
from .Dat import Dat

class DatMod(FileMod):

  CARDS = {
    "xelpud_xmailer": 364,
    "xelpud_talisman": 369,
    "xelpud_pillar": 370,
    "xelpud_mulana_talisman": 371,
    "xelpud_conversation_tree": 480,
    "xelpud_howling_wind": 1049
  }

  def __init__(self, filename):
    super().__init__(Dat, filename)

  def place_item_in_location(self, item, item_id, location) -> None:
    for card_index in location.cards:
      card = self.file_contents.cards[card_index]
      entries = card.contents.entries
      if location.slot is None:
        e = enumerate(entries)
        entry_index = next((i for i,v in e if v.header == 0x0042 and v.contents.value == location.item_id), None)
        entries[entry_index].contents.value = item_id

        original_obtain_flag = location.original_obtain_flag if location.original_obtain_flag is not None else location.obtain_flag
        obtain_flag = item.obtain_flag if item.obtain_flag is not None else location.obtain_flag
        obtain_value = item.obtain_value if item.obtain_value is not None else location.obtain_value

        e = enumerate(entries)
        entry_index = next((i for i,v in e if v.header == 0x0040 and v.contents.address == original_obtain_flag), None)
        entries[entry_index].contents.address = obtain_flag
        entries[entry_index].contents.value = obtain_value
      else:
        e = enumerate(entries)
        data_indices = [i for i,v in e if v.header == 0x004e]
        entries[data_indices[0]].contents.values[location.slot] = item_id
        if item.cost is not None:
          entries[data_indices[1]].contents.values[location.slot] = item.cost
        entries[data_indices[2]].contents.values[location.slot] = item.quantity
        entries[data_indices[3]].contents.values[location.slot] = location.obtain_flag
        if location.obtain_value > 1:
          entries[data_indices[6]].contents.values[location.slot] = location.obtain_flag

  def rewrite_xelpud_flag_checks(self) -> None:
    card = self.card("xelpud_conversation_tree")

    entries_to_remove = [
      self.CARDS["xelpud_howling_wind"],
      self.CARDS["xelpud_xmailer"],
      self.CARDS["xelpud_pillar"],
      self.CARDS["xelpud_mulana_talisman"]
    ]
    for entry_value in entries_to_remove:
      self.remove_data_entry_by_value(card, entry_value)

    entries_to_add = [
      [0xaed, 1, self.CARDS["xelpud_mulana_talisman"], 0],
      [0xaec, 2, self.CARDS["xelpud_pillar"], 0],
      [0xaec, 1, self.CARDS["xelpud_talisman"], 0],
      [0xad0, 0, self.CARDS["xelpud_xmailer"], 0]
    ]
    for entry in entries_to_add:
      self.add_data_entry(card, entry)

  def rewrite_xelpud_mulana_talisman_conversation(self) -> None:
    card = self.card("xelpud_mulana_talisman")
    entries = card.contents.entries

    talisman_flag_entries = [(i, entry) for i, entry in enumerate(entries)
      if entry.header == 0x0040 and entry.contents.address == 0x105
    ]
    for _, flag_entry in talisman_flag_entries:
      flag_entry.contents.address = 0xaed
      flag_entry.contents.value = 2
    
    flag = Dat.Flag()
    flag.address = 0x105
    flag.value = 2

    flag_entry = Dat.Entry()
    flag_entry.header = 0x0040
    flag_entry.contents = flag

    max_index = max([i for i,_ in talisman_flag_entries])
    insert_index = max([i for i,_ in talisman_flag_entries])
    entries.insert(insert_index, flag_entry)

    diary_puzzle_index = next((i for i, entry in enumerate(entries)
      if entry.header == 0x0040 and entry.contents.address == 0x212
    ), None)
    if diary_puzzle_index is not None:
      del entries[diary_puzzle_index]

  def card(self, card_name):
    card_index = self.CARDS[card_name]
    return self.file_contents.cards[card_index]

  def remove_data_entry_by_value(self, card, value):
    entries = card.contents.entries

    e = enumerate(entries)
    entry_index = next((i for i,v in e if v.header == 0x004e and v.contents.values[2] == value), None)
    next_index_to_delete = entry_index + 2

    size = 6 + (entries[entry_index].contents.num_values * 2)
    # Final Entry doesn't have a break after it
    if entry_index == (len(entries) - 1):
      size -= 2
      next_index_to_delete -= 1

    del entries[entry_index:next_index_to_delete]
    self.file_size -= size

  def add_data_entry(self, card, values):
    break_entry = Dat.Entry()
    break_entry.header = 0x000a
    break_entry.contents = Dat.Noop()
    break_entry.contents.no_value = bytearray()

    data = Dat.Data()
    data.num_values = len(values)
    data.values = values

    data_entry = Dat.Entry()
    data_entry.header = 0x004e
    data_entry.contents = data

    card.contents.entries.append(break_entry)
    card.contents.entries.append(data_entry)

    self.file_size += (6 + (data.num_values * 2))
