import toml

class LocalConfig:

  def __init__(self, multiworld, player):
    self.configurations = {
      "server_url": "<get_from_host>",
      "password": "<get_from_host_or_leave_as_empty_quotes>",
      "log_file_name": "lamulanamw.txt",
      "local_player_id": player,
      "players": [{"id": player_id, "name": multiworld.player_name[player_id]} for player_id in multiworld.player_ids],
      "item_mapping": []
    }

  def add_item(self, location):
    self.configurations["item_mapping"].append(
      {
        "flag": location.obtain_flag,
        "location_id": location.address,
        "player_id": location.item.player,
        "obtain_value": location.obtain_value
      }
    )

  def write_file(self):
    return toml.dumps(self.configurations)
