from .FileMod import FileMod
from .Items import item_table
from .Rcd import Rcd
from .LmFlags import GLOBAL_FLAGS, RCD_OBJECTS, TEST_OPERATIONS, WRITE_OPERATIONS, grail_flag_by_zone
from .Locations import get_locations_by_region
from .rcd.FlagTimer import FlagTimer
from .rcd.InstantItem import InstantItem
from .rcd.Operation import Operation
from .rcd.TextureDrawAnimation import TextureDrawAnimation
from .rcd.LemezaDetector import LemezaDetector
from .rcd.GrailPoint import GrailPoint


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

        if self.options.AncientLaMulaneseLearned:
            self.__create_ancient_lamulanese_timer()

    # RCD Mod Methods

    def __place_item(self, objects, object_type, param_index, param_len, location, location_id, item_id, original_obtain_flag, new_obtain_flag, obtain_value, item_mod, iterations, item):
        for _ in range(iterations):
            location = next((o for _, o in enumerate(objects) if o.id == object_type and o.parameters[param_index] == location_id+item_mod and len(o.parameters) < param_len), None)

            for test_op in location.test_operations:
                if test_op.flag == original_obtain_flag:
                    test_op.flag = new_obtain_flag
            for write_op in location.write_operations:
                if write_op.flag == original_obtain_flag:
                    write_op.flag = new_obtain_flag
                    if object_type in (RCD_OBJECTS["naked_item"], RCD_OBJECTS["instant_item"], RCD_OBJECTS["scan"]):
                        write_op.op_value = obtain_value

            # Destructible Cover customization
            for operation in ["test", "write"]:
                self.__update_operation(operation, objects, [RCD_OBJECTS["hitbox_generator"], RCD_OBJECTS["room_spawner"]], original_obtain_flag, new_obtain_flag)

            # Surface Map customization
            if original_obtain_flag == GLOBAL_FLAGS["surface_map"]:
                self.__fix_surface_map_scan(objects, location, original_obtain_flag)
            
            # Shrine of the Mother Map Crusher customization
            if original_obtain_flag == GLOBAL_FLAGS["shrine_map"]:
                self.__update_operation("write", objects, [RCD_OBJECTS["crusher"]], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

            # Mausoleum Ankh Jewel Trap customization
            if original_obtain_flag == GLOBAL_FLAGS["ankh_jewel_mausoleum"]:
                self.__update_operation("write", objects, [RCD_OBJECTS["moving_texture"]], original_obtain_flag, new_obtain_flag, new_op_value=obtain_value)

            # Yagostr Dais customization
            if original_obtain_flag == GLOBAL_FLAGS["yagostr_found"]:
                self.__update_operation("test", objects, [RCD_OBJECTS["trigger_dais"]], original_obtain_flag, new_obtain_flag)

            # Vimana customization
            if original_obtain_flag == GLOBAL_FLAGS["plane_found"]:
                vimana_objects = self.file_contents.zones[13].rooms[6].screens[1].objects_with_position
                self.__update_operation("test", vimana_objects, [RCD_OBJECTS["vimana"]], original_obtain_flag, new_obtain_flag)

            # Mekuri Master customization
            if original_obtain_flag == GLOBAL_FLAGS["mekuri"]:
                self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"], RCD_OBJECTS["texture_draw_animation"]], original_obtain_flag, new_obtain_flag)

            location.parameters[param_index] = item_id+item_mod
            location.parameters.append(1)
            location.parameters_length += 1
            self.file_size += 2

    def __fix_surface_map_scan(self, objects, location, obtain_flag):
        scan = next(o for _, o in enumerate(objects) if o.id == RCD_OBJECTS["scannable"] and len([t for t in o.test_operations if t.flag == obtain_flag]) > 0)

        surface_scan_flag = GLOBAL_FLAGS["replacement_surface_map_scan"]
        scan.test_operations[0].flag = surface_scan_flag
        scan.write_operations[0].flag = surface_scan_flag
        location.test_operations[0].flag = surface_scan_flag

        self.__add_operation_to_object("write", location, surface_scan_flag, WRITE_OPERATIONS["add"], 1)

    def __give_starting_items(self, items) -> None:
        flag_counter = 0
        starting_room = self.file_contents.zones[1].rooms[2].screens[1]

        for item_name in items:
            item = item_table[item_name]

            item_giver = InstantItem(x=0, y=0, item=item.game_code, width=160, height=120, sound=39)
            test_ops = [Operation.create(GLOBAL_FLAGS["starting_items"], TEST_OPERATIONS["eq"], flag_counter)]
            write_ops = [
                Operation.create(GLOBAL_FLAGS["starting_items"], WRITE_OPERATIONS["add"], 1),
                Operation.create(item.obtain_flag, WRITE_OPERATIONS["add"], item.obtain_value)
            ]
            item_giver.add_ops(test_ops, write_ops)
            item_giver.add_to_screen(self, starting_room)

            flag_counter += 1

    def __rewrite_diary_chest(self) -> None:
        diary_location = next((location for _, location in enumerate(get_locations_by_region(None)["Shrine of the Mother [Main]"]) if location.name == "Shrine of the Mother - Diary Chest"))
        for zone_index in diary_location.zones:
            diary_screen = self.file_contents.zones[zone_index].rooms[diary_location.room].screens[diary_location.screen]
            diary_chest = next((o for _, o in enumerate(diary_screen.objects_with_position)
                if o.id == RCD_OBJECTS["chest"]), None)

            diary_shawn_test = next((test_op for _, test_op in enumerate(diary_chest.test_operations) if test_op.flag == GLOBAL_FLAGS["shrine_shawn"]), None)
            diary_shawn_test.flag = GLOBAL_FLAGS["shrine_dragon_bone"]
            diary_shawn_test.operation = TEST_OPERATIONS["eq"]
            diary_shawn_test.op_value = 1

            self.__add_operation_to_object("test", diary_chest, GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["eq"], 2)

    def __add_diary_chest_timer(self) -> None:
        screen = self.file_contents.zones[9].rooms[2].screens[0]

        flag_timer = FlagTimer()
        test_ops = [
            Operation.create(GLOBAL_FLAGS["talisman_found"], TEST_OPERATIONS["gteq"], 3),
            Operation.create(GLOBAL_FLAGS["shrine_dragon_bone"], TEST_OPERATIONS["gteq"], 1)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["shrine_diary_chest"], WRITE_OPERATIONS["assign"], 2)]
        flag_timer.add_ops(test_ops, write_ops)
        flag_timer.add_to_screen(self, screen)

    def __rewrite_four_guardian_shop_conditions(self, dat_mod):
        msx2_replacement_flag = dat_mod.find_shop_flag("nebur_guardian", 0)
        objects = self.file_contents.zones[1].rooms[2].screens[0].objects_with_position
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=0, new_op_value=3, new_operation=TEST_OPERATIONS["lteq"])
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["xelpud_msx2"], GLOBAL_FLAGS["guardians_killed"], old_op_value=1, new_op_value=4)
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["msx2_found"], msx2_replacement_flag)

    def __rewrite_slushfund_conversation_conditions(self):
        objects = self.file_contents.zones[10].rooms[8].screens[0].objects_with_position
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["slushfund_conversation"], GLOBAL_FLAGS["replacement_slushfund_conversation"])

    def __rewrite_cog_chest(self):
        objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
        self.__update_operation("write", objects, [RCD_OBJECTS["chest"]], GLOBAL_FLAGS["cog_puzzle"], GLOBAL_FLAGS["replacement_cog_puzzle"])

        stray_fairy_door = self.__find_objects_by_operation("write", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["cog_puzzle"], operation=WRITE_OPERATIONS["assign"], op_value=3)[0]
        self.__add_operation_to_object("write", stray_fairy_door, GLOBAL_FLAGS["replacement_cog_puzzle"], WRITE_OPERATIONS["assign"], 3)

    def __rewrite_fishman_alt_shop(self):
        screen = self.file_contents.zones[4].rooms[3].screens[3]
        objects = screen.objects_with_position
        
        # Persist Main Shop after Alt is Opened
        self.__update_operation("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["fishman_shop_puzzle"], GLOBAL_FLAGS["fishman_shop_puzzle"], old_op_value=2, new_operation=TEST_OPERATIONS["gteq"])

        # Relocate Alt Shop
        self.__update_position("test", objects, [RCD_OBJECTS["language_conversation"]], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 76, op_value=3)

        # Relocate Fairy Keyspot trigger
        self.__update_position("test", objects, [RCD_OBJECTS["fairy_keyspot"]], GLOBAL_FLAGS["fishman_shop_puzzle"], 9, 74)

        # Relocate Alt Shop Explosion
        self.__update_position("test", objects, [RCD_OBJECTS["explosion"]], GLOBAL_FLAGS["screen_flag_0d"], 7, 76)

        # Add Alt Shop Door Graphic
        fishman_alt_door = TextureDrawAnimation(x=9, y=76, layer=-1, image_x=260, image_y=0, dx=40, dy=40, animation_frames=1, max_alpha=255)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["mother_state"], TEST_OPERATIONS["neq"], 3),
            Operation.create(GLOBAL_FLAGS["fishman_shop_puzzle"], TEST_OPERATIONS["eq"], 3)
        ]
        fishman_alt_door.add_ops(test_ops, [])
        fishman_alt_door.add_to_screen(self, screen)

    def __clean_up_test_operations(self):
        # Remove Fairy Conversation Requirement from Buer Room Ladder
        buer_objects = self.file_contents.zones[3].rooms[2].screens[1].objects_with_position
        self.__remove_operation("test", buer_objects, [RCD_OBJECTS["hitbox_generator"]], GLOBAL_FLAGS["endless_fairyqueen"])

        # Remove Slushfund Conversation Requirement from Pepper Puzzle
        pepper_puzzle_objects = self.file_contents.zones[0].rooms[0].screens[0].objects_with_position
        self.__remove_operation("test", pepper_puzzle_objects, [RCD_OBJECTS["use_item"]], GLOBAL_FLAGS["slushfund_conversation"])

        # Remove Crucifix Check from Crucifix Puzzle Torches
        crucifix_puzzle_objects = self.file_contents.zones[0].rooms[1].screens[1].objects_with_position
        self.__remove_operation("test", crucifix_puzzle_objects, [RCD_OBJECTS["texture_draw_animation"]], GLOBAL_FLAGS["crucifix_found"])

        # Remove Cog Puzzle Requirement from Mudmen Activation
        mudmen_activation_objects = self.file_contents.zones[10].rooms[0].screens[1].objects_with_position
        self.__remove_operation("test", mudmen_activation_objects, [RCD_OBJECTS["use_item"]], GLOBAL_FLAGS["cog_puzzle"])

        # Remove Plane Missing Requirement from Plane Puzzle
        plane_platform_left_objects = self.file_contents.zones[13].rooms[7].screens[0].objects_with_position
        self.__remove_operation("test", plane_platform_left_objects, [RCD_OBJECTS["counterweight_platform"]], GLOBAL_FLAGS["plane_found"])
        plane_platform_right_objects = self.file_contents.zones[13].rooms[7].screens[2].objects_with_position
        self.__remove_operation("test", plane_platform_right_objects, [RCD_OBJECTS["counterweight_platform"]], GLOBAL_FLAGS["plane_found"])

        # Remove Dracuet Check From Guidance Elevator Block
        guidance_elevator_hibox_objects = self.file_contents.zones[0].rooms[6].screens[0].objects_with_position
        self.__remove_operation("test", guidance_elevator_hibox_objects, [RCD_OBJECTS["hitbox_generator"]], GLOBAL_FLAGS["mulbruk_father"])

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

                                lemeza_detector = LemezaDetector(x=obj.x_pos, y=obj.y_pos-1, width=2, height=3)
                                test_ops = [Operation.create(grail_flag, TEST_OPERATIONS["eq"], 0)]
                                write_ops = [Operation.create(grail_flag, WRITE_OPERATIONS["assign"], 1)]
                                lemeza_detector.add_ops(test_ops, write_ops)
                                lemeza_detector.add_to_screen(self, screen)

    def __create_boss_checkpoints(self) -> None:
        # Amphisbaena
        amphisbaena_screen = self.file_contents.zones[0].rooms[8].screens[1]
        amphisbaena_grail_point = GrailPoint(x=15, y=44, card=41)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["amphisbaena_ankh_puzzle"], TEST_OPERATIONS["eq"], 5),
            Operation.create(GLOBAL_FLAGS["amphisbaena_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        amphisbaena_grail_point.add_ops(test_ops, write_ops)
        amphisbaena_grail_point.add_to_screen(self, amphisbaena_screen)

        # Sakit
        sakit_screen = self.file_contents.zones[2].rooms[8].screens[1]
        sakit_grail_point = GrailPoint(x=45, y=6, card=75)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["sakit_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["sakit_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        sakit_grail_point.add_ops(test_ops, write_ops)
        sakit_grail_point.add_to_screen(self, sakit_screen)

        # Ellmac
        ellmac_screen = self.file_contents.zones[3].rooms[8].screens[0]
        ellmac_grail_point = GrailPoint(x=20, y=16, card=104)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["ellmac_ankh_puzzle"], TEST_OPERATIONS["eq"], 5),
            Operation.create(GLOBAL_FLAGS["ellmac_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        ellmac_grail_point.add_ops(test_ops, write_ops)
        ellmac_grail_point.add_to_screen(self, ellmac_screen)

        # Bahamut
        bahamut_screen = self.file_contents.zones[4].rooms[4].screens[0]
        bahamut_grail_point = GrailPoint(x=19, y=17, card=136)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["bahamut_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["bahamut_room_flooded"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["bahamut_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        bahamut_grail_point.add_ops(test_ops, write_ops)
        bahamut_grail_point.add_to_screen(self, bahamut_screen)

        # Viy
        viy_screen = self.file_contents.zones[5].rooms[8].screens[1]
        viy_grail_point = GrailPoint(x=23, y=28, card=149)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["viy_ankh_puzzle"], TEST_OPERATIONS["eq"], 4),
            Operation.create(GLOBAL_FLAGS["viy_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        viy_grail_point.add_ops(test_ops, write_ops)
        viy_grail_point.add_to_screen(self, viy_screen)

        # Palenque
        palenque_screen = self.file_contents.zones[6].rooms[9].screens[1]
        palenque_grail_point = GrailPoint(x=47, y=20, card=170)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["palenque_ankh_puzzle"], TEST_OPERATIONS["eq"], 3),
            Operation.create(GLOBAL_FLAGS["palenque_screen_mural"], TEST_OPERATIONS["eq"], 3),
            Operation.create(GLOBAL_FLAGS["palenque_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        palenque_grail_point.add_ops(test_ops, write_ops)
        palenque_grail_point.add_to_screen(self, palenque_screen)

        # Baphomet
        baphomet_screen = self.file_contents.zones[7].rooms[4].screens[1]
        baphomet_grail_point = GrailPoint(x=47, y=4, card=188)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["baphomet_ankh_puzzle"], TEST_OPERATIONS["eq"], 2),
            Operation.create(GLOBAL_FLAGS["baphomet_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        baphomet_grail_point.add_ops(test_ops, write_ops)
        baphomet_grail_point.add_to_screen(self, baphomet_screen)

        # Tiamat
        tiamat_screen = self.file_contents.zones[17].rooms[9].screens[0]
        tiamat_grail_point = GrailPoint(x=15, y=4, card=368)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["tiamat_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["tiamat_state"], TEST_OPERATIONS["lt"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        tiamat_grail_point.add_ops(test_ops, write_ops)
        tiamat_grail_point.add_to_screen(self, tiamat_screen)

        # Mother
        mother_screen = self.file_contents.zones[18].rooms[3].screens[1]
        mother_grail_point = GrailPoint(x=33, y=20, card=231)
        test_ops = [
            Operation.create(GLOBAL_FLAGS["mother_ankh_puzzle"], TEST_OPERATIONS["eq"], 1),
            Operation.create(GLOBAL_FLAGS["mother_state"], TEST_OPERATIONS["lteq"], 2),
            Operation.create(GLOBAL_FLAGS["screen_flag_02"], TEST_OPERATIONS["eq"], 0),
            Operation.create(GLOBAL_FLAGS["escape"], TEST_OPERATIONS["eq"], 0)
        ]
        write_ops = [Operation.create(GLOBAL_FLAGS["screen_flag_02"], WRITE_OPERATIONS["assign"], 1)]
        mother_grail_point.add_ops(test_ops, write_ops)
        mother_grail_point.add_to_screen(self, mother_screen)

    def __create_ancient_lamulanese_timer(self):
        screen = self.file_contents.zones[1].rooms[2].screens[1]

        flag_timer = FlagTimer()
        test_ops = [Operation.create(GLOBAL_FLAGS["ancient_lamulanese_learned"], TEST_OPERATIONS["eq"], 0)]
        write_ops = [
            Operation.create(GLOBAL_FLAGS["translation_tablets_read"], WRITE_OPERATIONS["assign"], 3),
            Operation.create(GLOBAL_FLAGS["ancient_lamulanese_learned"], WRITE_OPERATIONS["assign"], 1)
        ]
        flag_timer.add_ops(test_ops, write_ops)
        flag_timer.add_to_screen(self, screen)

    # Utility Methods

    def __op_type(self, op):
        return f"{op}_operations"

    # Search Methods

    def __find_objects_by_operation(self, op_type, objects, object_ids, flag, operation=None, op_value=None):
        return [o for _, o in enumerate(objects) if o.id in object_ids and len([op for op in getattr(o, self.__op_type(op_type)) if self.__op_matches(op, flag, operation, op_value)]) > 0]

    def __find_operation_index(self, ops, flag, operation=None, op_value=None):
        return next(i for i, op in enumerate(ops) if self.__op_matches(op, flag, operation, op_value))

    # Conditionals

    def __op_matches(self, op, flag, operation, op_value):
        return op.flag == flag and (operation is None or op.operation == operation) and (op_value is None or op.op_value == op_value)

    # Write Methods

    def __update_position(self, op_type, objects, object_ids, flag, x_pos, y_pos, operation=None, op_value=None):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, flag, operation, op_value)

        for obj in objs:
            obj.x_pos = x_pos
            obj.y_pos = y_pos

    def __update_operation(self, op_type, objects, object_ids, old_flag, new_flag, old_operation=None, new_operation=None, old_op_value=None, new_op_value=None):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, old_flag, old_operation, old_op_value)

        for obj in objs:
            ops = getattr(obj, self.__op_type(op_type))
            op_index = self.__find_operation_index(ops, old_flag, old_operation, old_op_value)
            
            op = getattr(obj, self.__op_type(op_type))[op_index]
            op.flag = new_flag
            if new_operation is not None:
                op.operation = new_operation
            if new_op_value is not None:
                op.op_value = new_op_value

    def __remove_operation(self, op_type, objects, object_ids, flag):
        objs = self.__find_objects_by_operation(op_type, objects, object_ids, flag)

        for obj in objs:
            ops = getattr(obj, self.__op_type(op_type))
            op_index = self.__find_operation_index(ops, flag)
            
            del ops[op_index]
            op_type_len = self.__op_type(op_type) + "_length"
            old_len = getattr(obj, op_type_len)
            setattr(obj, op_type_len, old_len-1)
            self.file_size -= 4

    def __add_operation_to_object(self, op_type, obj, flag, operation, op_value):
        op = Rcd.Operation()
        op.flag = flag
        op.operation = operation
        op.op_value = op_value

        ops = getattr(obj, self.__op_type(op_type))
        ops.append(op)

        op_type_len = self.__op_type(op_type) + "_length"
        old_len = getattr(obj, op_type_len)
        setattr(obj, op_type_len, old_len+1)
        self.file_size += 4
