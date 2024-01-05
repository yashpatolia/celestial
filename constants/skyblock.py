SLAYER_LEVEL = {
    'zombie': {
        0: 0,
        1: 5,
        2: 25,
        3: 200,
        4: 1000,
        5: 5000,
        6: 20000,
        7: 100000,
        8: 400000,
        9: 1000000
    },
    'spider': {
        0: 0,
        1: 5,
        2: 25,
        3: 200,
        4: 1000,
        5: 5000,
        6: 20000,
        7: 100000,
        8: 400000,
        9: 1000000
    },
    'wolf': {
        0: 0,
        1: 10,
        2: 30,
        3: 250,
        4: 1500,
        5: 5000,
        6: 20000,
        7: 100000,
        8: 400000,
        9: 1000000
    },
    'enderman': {
        0: 0,
        1: 10,
        2: 30,
        3: 250,
        4: 1500,
        5: 5000,
        6: 20000,
        7: 100000,
        8: 400000,
        9: 1000000
    }
}

SLAYER_TEMPLATE = {
    'zombie': {'xp': 0, 'level': 0, 'name': 'Revenant'},
    'spider': {'xp': 0, 'level': 0, 'name': 'Tarantula'},
    'wolf': {'xp': 0, 'level': 0, 'name': 'Sven'},
    'enderman': {'xp': 0, 'level': 0, 'name': 'Voidgloom'}
}

MILESTONE_TABLE = {
    'rock': {'Rock': 0,
             'Common Rock': 2500,
             'Uncommon Rock': 7500,
             'Rare Rock': 20000,
             'Epic Rock': 100000,
             'Legendary Rock': 250000},
    'dolphin': {'Dolphin': 0,
                'Common Dolphin': 250,
                'Uncommon Dolphin': 1000,
                'Rare Dolphin': 2500,
                'Epic Dolphin': 5000,
                'Legendary Dolphin': 10000}
}

COOP_UPGRADES_TEMPLATE = {
    'minion_slots': {'name': 'Minion Slots', 'level': 0, 'max_level': 5},
    'island_size': {'name': 'Island Size', 'level': 0, 'max_level': 10},
    'coins_allowance': {'name': 'Coins Allowance', 'level': 0, 'max_level': 5},
    'coop_slots': {'name': 'Coop Slots', 'level': 0, 'max_level': 3},
    'guests_count': {'name': 'Guests Count', 'level': 0, 'max_level': 5}
}

DUNGEON_XP_TABLE = {0: 0, 1: 50, 2: 125, 3: 235, 4: 395, 5: 625, 6: 955, 7: 1425, 8: 2095, 9: 3045, 10: 4385, 11: 6275,
                    12: 8940, 13: 12700, 14: 17960, 15: 25340, 16: 35640, 17: 50040, 18: 70040, 19: 97640, 20: 135640,
                    21: 188140, 22: 259640, 23: 356640, 24: 488640, 25: 668640, 26: 911640, 27: 1239640, 28: 1684640,
                    29: 2284640, 30: 3084640, 31: 4149640, 32: 5559640, 33: 7459640, 34: 9959640, 35: 13259640,
                    36: 17559640, 37: 23159640, 38: 30359640, 39: 39559640, 40: 51559640, 41: 66559640, 42: 85559640,
                    43: 109559640, 44: 139559640, 45: 177559640, 46: 225559640, 47: 285559640, 48: 360559640,
                    49: 453559640, 50: 569809640}

DUNGEON_INDIVIDUAL_XP_TABLE = {0: 0, 1: 50, 2: 75, 3: 110, 4: 160, 5: 230, 6: 330, 7: 470, 8: 670, 9: 950, 10: 1340,
                               11: 1890, 12: 2665, 13: 3760, 14: 5260, 15: 7380, 16: 10300, 17: 14400, 18: 20000,
                               19: 27600, 20: 38000, 21: 52500, 22: 71500, 23: 97000, 24: 132000, 25: 180000,
                               26: 243000,
                               27: 328000, 28: 445000, 29: 600000, 30: 800000, 31: 1065000, 32: 1410000, 33: 1900000,
                               34: 2500000, 35: 3300000, 36: 4300000, 37: 5600000, 38: 7200000, 39: 9200000,
                               40: 12000000, 41: 15000000, 42: 19000000, 43: 24000000, 44: 30000000, 45: 38000000,
                               46: 48000000, 47: 60000000, 48: 75000000, 49: 93000000, 50: 116250000}

DUNGEON_FLOOR_INFO_TEMPLATE = {
    '0': {'name': 'Entrance', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '1': {'name': 'Floor 1', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '2': {'name': 'Floor 2', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '3': {'name': 'Floor 3', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '4': {'name': 'Floor 4', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '5': {'name': 'Floor 5', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '6': {'name': 'Floor 6', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '7': {'name': 'Floor 7', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0}
}

DUNGEON_MASTER_FLOOR_INFO_TEMPLATE = {
    '1': {'name': 'Master 1', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '2': {'name': 'Master 2', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '3': {'name': 'Master 3', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '4': {'name': 'Master 4', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '5': {'name': 'Master 5', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0},
    '6': {'name': 'Master 6', 'best_score': 0, 'fastest_time_s': 0, 'fastest_time_s_plus': 0, 'completions': 0}
}

DUNGEON_CLASS_XP_TEMPLATE = {
    'mage': 0,
    'archer': 0,
    'tank': 0,
    'healer': 0,
    'berserk': 0
}

BLACKLISTED_SKILLS = ['experience_skill_carpentry', 'experience_skill_runecrafting']

SKILL_XP_TABLE = {0: 0, 1: 50, 2: 175, 3: 375, 4: 675, 5: 1175, 6: 1925, 7: 2925, 8: 4425, 9: 6425, 10: 9925, 11: 14925,
                  12: 22425, 13: 32425, 14: 47425, 15: 67425, 16: 97425, 17: 147425, 18: 222425, 19: 322425, 20: 522425,
                  21: 822425, 22: 1222425, 23: 1722425, 24: 2322425, 25: 3022425, 26: 3822425, 27: 4722425, 28: 5722425,
                  29: 6822425, 30: 8022425, 31: 9322425, 32: 10722425, 33: 12222425, 34: 13822425, 35: 15522425,
                  36: 17322425, 37: 19222425, 38: 21222425, 39: 23322425, 40: 25522425, 41: 27822425, 42: 30222425,
                  43: 32722425, 44: 35322425, 45: 38072425, 46: 40972425, 47: 44072425, 48: 47472425, 49: 51172425,
                  50: 55172425, 51: 59472425, 52: 64072425, 53: 68972425, 54: 74172425, 55: 79672425, 56: 85472425,
                  57: 91572425, 58: 97972425, 59: 104672425, 60: 111672425}

SKILL_INDIVIDUAL_XP_TABLE = {0: 0, 1: 50, 2: 125, 3: 200, 4: 300, 5: 500, 6: 750, 7: 1000, 8: 1500, 9: 2000, 10: 3500,
                             11: 5000, 12: 7500, 13: 10000, 14: 15000, 15: 20000, 16: 30000, 17: 50000, 18: 75000,
                             19: 100000, 20: 200000, 21: 300000, 22: 400000, 23: 500000, 24: 600000, 25: 700000,
                             26: 800000, 27: 900000, 28: 1000000, 29: 1100000, 30: 1200000, 31: 1300000, 32: 1400000,
                             33: 1500000, 34: 1600000, 35: 1700000, 36: 1800000, 37: 1900000, 38: 2000000, 39: 2100000,
                             40: 2200000, 41: 2300000, 42: 2400000, 43: 2500000, 44: 2600000, 45: 2750000, 46: 2900000,
                             47: 3100000, 48: 3400000, 49: 3700000, 50: 4000000, 51: 4300000, 52: 4600000, 53: 4900000,
                             54: 5200000, 55: 5500000, 56: 5800000, 57: 6100000, 58: 6400000, 59: 6700000, 60: 7000000}

RUNECRAFTING_XP_TABLE = {0: 0, 1: 50, 2: 150, 3: 275, 4: 435, 5: 635, 6: 885, 7: 1200, 8: 1600, 9: 2100, 10: 2725,
                         11: 3510, 12: 4510, 13: 5760, 14: 7325, 15: 9325, 16: 11825, 17: 14950, 18: 18950, 19: 23950,
                         20: 30200, 21: 38050, 22: 47850, 23: 60100, 24: 75400, 25: 94500}

RUNECRAFTING_INDIVIDUAL_XP_TABLE = {0: 0, 1: 50, 2: 100, 3: 125, 4: 160, 5: 200, 6: 250, 7: 315, 8: 400, 9: 500,
                                    10: 625, 11: 785, 12: 1000, 13: 1250, 14: 1565, 15: 2000, 16: 2500, 17: 3125,
                                    18: 4000, 19: 5000, 20: 6250, 21: 7850, 22: 9800, 23: 12250, 24: 15300, 25: 19100}

SKILLS_TEMPLATE = {
    'experience_skill_combat': {'xp': 0, 'max_level': 60},
    'experience_skill_mining': {'xp': 0, 'max_level': 60},
    'experience_skill_farming': {'xp': 0, 'max_level': 60},
    'experience_skill_fishing': {'xp': 0, 'max_level': 50},
    'experience_skill_foraging': {'xp': 0, 'max_level': 50},
    'experience_skill_taming': {'xp': 0, 'max_level': 50},
    'experience_skill_alchemy': {'xp': 0, 'max_level': 50},
    'experience_skill_enchanting': {'xp': 0, 'max_level': 60},
    'experience_skill_runecrafting': {'xp': 0, 'max_level': 25},
    'experience_skill_carpentry': {'xp': 0, 'max_level': 50}
}

JACOBS_MEDALS_TEMPLATE = {
    'bronze': 0,
    'silver': 0,
    'gold': 0
}

JACOBS_UPGRADES_TEMPLATE = {
    'double_drops': {'level': 0, 'max_level': 15},
    'farming_level_cap': {'level': 0, 'max_level': 10}
}

JACOBS_INFO_TEMPLATE = {
    'POTATO_ITEM': {'name': 'Potato', 'gold_status': False, 'highscore': 0},
    'CARROT_ITEM': {'name': 'Carrot', 'gold_status': False, 'highscore': 0},
    'NETHER_STALK': {'name': 'Nether Wart', 'gold_status': False, 'highscore': 0},
    'SUGAR_CANE': {'name': 'Sugarcane', 'gold_status': False, 'highscore': 0},
    'MUSHROOM_COLLECTION': {'name': 'Mushroom', 'gold_status': False, 'highscore': 0},
    'PUMPKIN': {'name': 'Pumpkin', 'gold_status': False, 'highscore': 0},
    'MELON': {'name': 'Melon', 'gold_status': False, 'highscore': 0},
    'INK_SACK': {'name': 'Cocoa Beans', 'gold_status': False, 'highscore': 0},
    'WHEAT': {'name': 'Wheat', 'gold_status': False, 'highscore': 0},
    'CACTUS': {'name': 'Cactus', 'gold_status': False, 'highscore': 0}
}

SKILL_WEIGHT_VALUES = {
    'experience_skill_combat': {'exponent': 1.15797687265, 'divider': 275862},
    'experience_skill_mining': {'exponent': 1.18207448, 'divider': 259634},
    'experience_skill_farming': {'exponent': 1.217848139, 'divider': 220689},
    'experience_skill_fishing': {'exponent': 1.406418, 'divider': 88274},
    'experience_skill_foraging': {'exponent': 1.232826, 'divider': 259634},
    'experience_skill_taming': {'exponent': 1.14744, 'divider': 441379},
    'experience_skill_alchemy': {'exponent': 1.0, 'divider': 1103448},
    'experience_skill_enchanting': {'exponent': 0.96976583, 'divider': 882758}
}

SLAYER_WEIGHT_VALUES = {
    'zombie': {'divider': 2208, 'modifier': 0.15},
    'spider': {'divider': 2118, 'modifier': 0.08},
    'wolf': {'divider': 1962, 'modifier': 0.015},
    'enderman': {'divider': 1430, 'modifier': 0.017}
}

DUNGEON_WEIGHT_VALUES = {
    'catacomb': 0.0002149604615,
    'healer': 0.0000045254834,
    'mage': 0.0000045254834,
    'berserk': 0.0000045254834,
    'tank': 0.0000045254834,
    'archer': 0.0000045254834
}