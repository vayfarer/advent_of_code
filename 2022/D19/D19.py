# Advent of Code 2022, Day 19 Part 1
# Michael Chen
# 12/24/2022

import time
import re

class NotEnoughMinerals(Exception):
    """Not enough minerals to buy these bots!"""
    pass

class Blueprint:
    def __init__(self, _id:int, ore_bot:dict, cla_bot:dict, obs_bot:dict, geo_bot:dict):
        """
        Cost parameters are dict format: {ore: NUM, cla: NUM, obs: NUM}.
        :param id: Numerical ID of the blueprint
        :param ore_bot: cost of the ore robot
        :param cla_bot: cost of the clay robot
        :param obs_bot: cost of the obsidian robot
        :param geo_bot: cost of the geode robot
        """

        self.id = _id
        self._bots = {'ore_bot': ore_bot, 'cla_bot': cla_bot, 'obs_bot':obs_bot, 'geo_bot':geo_bot}
        self._ore_bot = ore_bot
        self._cla_bot = cla_bot
        self._obs_bot = obs_bot
        self._geo_bot = geo_bot
        self.set_checks()

    def __str__(self):
        out = f'Blueprint #{self.id}: \nOre bot: {self._ore_bot} \nCla bot: {self._cla_bot} \nObs bot: {self._obs_bot} \nGeo bot: {self._geo_bot}'
        return out

    def next_options(self, bot_qty, resources, no_build, minute, minutes):
        """Returns the options available from this blueprint given ore, cla, and
        obs resources.
        :param: bot_qty: Current number of bots before building more.
        :param: resources: Resources available for building bots.
        {'ore': NUM, 'cla': NUM, 'obs': NUM}
        :param: no_build: Set() of bots (eg. {'ore_bot'}) that are not being considered for build
        options."""

        no_build_bot = {'ore_bot': 0,
                     'cla_bot': 0,
                     'obs_bot': 0,
                     'geo_bot': 0}
        new_options = []
        new_no_build = set()

        bot_list = list(no_build_bot.keys())

        minutes_left = minutes - minute
        if minutes_left <= 4:
            bot_list.remove('ore_bot')
            if minutes_left <= 3:
                bot_list.remove('cla_bot')
                if minutes_left <= 2:
                    bot_list.remove('obs_bot')


        for bot in bot_list:
            bot_range = 0 if bot in no_build or bot_qty[bot] >= self._max_bots[bot] else self.buy_num(resources, bot)
            if bot_range > 0:
                # Add this bot to the no build set because it could have been built.

                new_bot_qty = bot_qty.copy()
                new_bot_qty[bot] += 1

                new_no_build.add(bot)
                new_res = add_resources(bot_qty, self.change(resources, bot, 1))

                new_options.extend([(new_bot_qty, new_res, set())])

        # Always consider building geode bots?
        new_no_build.difference_update({'geo_bot'})

        # add the no_build alternative
        new_res = add_resources(bot_qty, resources)
        new_options.extend([(bot_qty, new_res, new_no_build)])

        return new_options

    def set_checks(self):
        """Sets the times at which the DSF search for most geodes should be
        checked."""
        self._check_minute1 = max(self._bots['ore_bot']['ore'], self._bots['cla_bot']['ore']) + 1
        # The branch should have built an ore or clay bot by this minute.
        self._max_bots = {}
        self._max_bots['ore_bot'] = max([self._bots[bot]['ore'] for bot in self._bots])
        self._max_bots['cla_bot'] = max([self._bots[bot]['cla'] for bot in self._bots])
        self._max_bots['obs_bot'] = max([self._bots[bot]['obs'] for bot in self._bots])
        # No real limit to geobots.
        self._max_bots['geo_bot'] = 32

    def check_minute1(self):
        return self._check_minute1

    def buy_num(self, resources, bot):
        """Returns the number of `bot` (eg. 'ore_bot') that can be bought with
        `resources'."""
        return min([resources[i] // cost for i, cost in self._bots[bot].items() if cost > 0])

    def change(self, resources, bot, qty):
        """Returns the change left over from `resources` after buying `qty` of
        bot`."""
        change = {'ore': 0, 'cla': 0, 'obs': 0, 'geo':0}
        for res, num in resources.items():
            change[res] = num - qty * self._bots[bot][res]
            if change[res] < 0:
                raise NotEnoughMinerals
        return change

def add_resources(bot_qty, resources):
    """Gives new resources """
    new_res = {'ore': resources['ore'] + bot_qty['ore_bot'],
               'cla': resources['cla'] + bot_qty['cla_bot'],
               'obs': resources['obs'] + bot_qty['obs_bot'],
               'geo': resources['geo'] + bot_qty['geo_bot']
               }
    return new_res

def max_geo(blueprint, minutes):
    """Returns the quality level of the blueprint by finding the maximum geodes
    the blueprint can crack via DFS."""
    start_bots = {'ore_bot': 1,
                  'cla_bot': 0,
                  'obs_bot': 0,
                  'geo_bot': 0}
    start_res = {'ore': 0, 'cla': 0, 'obs': 0, 'geo': 0}

    geodes_left = {16: 126, 15: 110, 14: 95, 13: 81, 12: 68, 11: 56,
                   10: 55, 9: 45, 8: 36, 7: 28, 6: 21, 5:15, 4:10, 3:6, 2: 3, 1: 1, 0: 0}
    check_minute1 = blueprint.check_minute1()

    def dfs(bot_qty:dict, resources:dict, no_build, max_geo:int=0, minute:int=0):
        """DFS traversal of blueprint builds"""
        minute += 1

        minutes_left = minutes - minute
        # Checks if the maximum number of geodes possible from this branch beats
        # the current maximum.
        if minutes_left < 17 and geodes_left[minutes_left] + resources['geo'] + bot_qty['geo_bot']*(minutes_left + 1) < max_geo:
            return max_geo

        # reached end of dfs.
        if minute == minutes:
            geo = resources['geo'] + bot_qty['geo_bot']
            return max(max_geo, geo)

        options = blueprint.next_options(bot_qty, resources, no_build, minute, minutes)

        for new_bot_qty, new_resources, no_build in options:

            if minute == check_minute1 and new_bot_qty['ore_bot'] < 2 and new_bot_qty['cla_bot'] < 1:
                # If the branch did not build a clay or ore bot, discontinue.
                continue
            else:
                max_geo = max(max_geo, dfs(new_bot_qty, new_resources, no_build, max_geo, minute))

        return max_geo

    return dfs(start_bots, start_res, set())

if __name__ == "__main__":

    blueprints = []
    time_limit = 24

    with open('input.txt') as f:
        line = f.readline().strip()
        while line:
            _id, ore_ore, cla_ore, obs_ore, obs_cla, geo_ore, geo_obs = re.findall(r'\d+', line)
            _id = int(_id)
            ore_bot = {'ore':int(ore_ore), 'cla':0, 'obs':0, 'geo':0}
            cla_bot = {'ore':int(cla_ore), 'cla':0, 'obs':0, 'geo':0}
            obs_bot = {'ore':int(obs_ore), 'cla':int(obs_cla), 'obs':0, 'geo':0}
            geo_bot = {'ore':int(geo_ore), 'cla':0, 'obs':int(geo_obs), 'geo':0}
            blueprints.append(Blueprint(_id, ore_bot, cla_bot, obs_bot, geo_bot))

            line = f.readline().strip()

    sum_ql = 0
    # tic = time.perf_counter()
    for bp in blueprints:
        sum_ql += bp.id * max_geo(bp, time_limit)
    # print(time.perf_counter() - tic)

    print(f'Part 1: Total blueprint quality is {sum_ql}.')

    time_limit = 32
    geo_product = 1
    tic = time.perf_counter()
    for bp in blueprints[0:3]:
        geo_product *= max_geo(bp, time_limit)
    print(time.perf_counter() - tic)

    print(f'Part 2: Blueprint product is {geo_product}.')

