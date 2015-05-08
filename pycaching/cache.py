#!/usr/bin/env python3

import logging
import datetime
from pycaching.errors import ValueError
from pycaching.point import Point
from pycaching.util import Util


def lazy_loaded(func):
    """Decorator providing lazy loading."""

    def wrapper(*args, **kwargs):
        self = args[0]
        assert isinstance(self, Cache)
        try:
            return func(*args, **kwargs)
        except AttributeError:
            logging.debug("Lazy loading: %s", func.__name__)
            self.geocaching.load_cache(self.wp, self)
            return func(*args, **kwargs)

    return wrapper


class Cache(object):

    # generated by Util.get_possible_attributes()
    # TODO: smarter way of keeping attributes up to date
    _possible_attributes = {
        "abandonedbuilding": "Abandoned Structure",
        "available": "Available at All Times",
        "bicycles": "Bicycles",
        "boat": "Boat",
        "campfires": "Campfires",
        "camping": "Camping Available",
        "cliff": "Cliff / Falling Rocks",
        "climbing": "Difficult Climbing",
        "cow": "Watch for Livestock",
        "danger": "Dangerous Area",
        "dangerousanimals": "Dangerous Animals",
        "dogs": "Dogs",
        "fee": "Access or Parking Fee",
        "field_puzzle": "Field Puzzle",
        "firstaid": "Needs Maintenance",
        "flashlight": "Flashlight Required",
        "food": "Food Nearby",
        "frontyard": "Front Yard(Private Residence)",
        "fuel": "Fuel Nearby",
        "geotour": "GeoTour Cache",
        "hike_long": "Long Hike (+10km)",
        "hike_med": "Medium Hike (1km-10km)",
        "hike_short": "Short Hike (Less than 1km)",
        "hiking": "Significant Hike",
        "horses": "Horses",
        "hunting": "Hunting",
        "jeeps": "Off-Road Vehicles",
        "kids": "Recommended for Kids",
        "landf": "Lost And Found Tour",
        "mine": "Abandoned Mines",
        "motorcycles": "Motortcycles",
        "night": "Recommended at Night",
        "nightcache": "Night Cache",
        "onehour": "Takes Less Than an Hour",
        "parking": "Parking Available",
        "parkngrab": "Park and Grab",
        "partnership": "Partnership Cache",
        "phone": "Telephone Nearby",
        "picnic": "Picnic Tables Nearby",
        "poisonoak": "Poisonous Plants",
        "public": "Public Transportation",
        "quads": "Quads",
        "rappelling": "Climbing Gear",
        "restrooms": "Public Restrooms Nearby",
        "rv": "Truck Driver/RV",
        "s-tool": "Special Tool Required",
        "scenic": "Scenic View",
        "scuba": "Scuba Gear",
        "seasonal": "Seasonal Access",
        "skiis": "Cross Country Skis",
        "snowmobiles": "Snowmobiles",
        "snowshoes": "Snowshoes",
        "stealth": "Stealth Required",
        "stroller": "Stroller Accessible",
        "swimming": "May Require Swimming",
        "teamwork": "Teamwork Required",
        "thorn": "Thorns",
        "ticks": "Ticks",
        "touristOK": "Tourist Friendly",
        "treeclimbing": "Tree Climbing",
        "UV": "UV Light Required",
        "wading": "May Require Wading",
        "water": "Drinking Water Nearby",
        "wheelchair": "Wheelchair Accessible",
        "winter": "Available During Winter",
        "wirelessbeacon": "Wireless Beacon"
    }

    _possible_types = {
        # key is cache image url, used for parsing: http://www.geocaching.com/images/WptTypes/[KEY].gif
        "2": "Traditional Cache",
        "3": "Multi-cache",
        "8": "Mystery Cache",
        "__8": "Unknown Cache",  # same as Mystery, key not used
        "5": "Letterbox hybrid",
        "6": "Event Cache",
        "mega": "Mega-Event Cache",
        "giga": "Giga-Event Cache",
        "earthcache": "Earthcache",
        "137": "Earthcache",
        "13": "Cache in Trash out Event",
        "11": "Webcam Cache",
        "4": "Virtual Cache",
        "1858": "Wherigo Cache",
        "10Years_32": "Lost and Found Event Cache",
        "ape_32": "Project Ape Cache",
        "HQ_32": "Groundspeak HQ",
        "1304": "GPS Adventures Exhibit",
        "4738": "Groundspeak Block Party",
        "12": "Locationless (Reverse) Cache",
    }

    _possible_sizes = {
        "micro": "micro",
        "small": "small",
        "regular": "regular",
        "large": "large",
        "not_chosen": "not chosen",
        "virtual": "virtual",
        "other": "other",
    }

    def __init__(self, wp, geocaching, *, name=None, cache_type=None, location=None, state=None,
                 found=None, size=None, difficulty=None, terrain=None, author=None, hidden=None,
                 attributes=None, summary=None, description=None, hint=None, favorites=None, pm_only=None):
        self.wp = wp
        self.geocaching = geocaching
        if name is not None:
            self.name = name
        if cache_type is not None:
            self.cache_type = cache_type
        if location is not None:
            self.location = location
        if state is not None:
            self.state = state
        if found is not None:
            self.found = found
        if size is not None:
            self.size = size
        if difficulty is not None:
            self.difficulty = difficulty
        if terrain is not None:
            self.terrain = terrain
        if author is not None:
            self.author = author
        if hidden is not None:
            self.hidden = hidden
        if attributes is not None:
            self.attributes = attributes
        if summary is not None:
            self.summary = summary
        if description is not None:
            self.description = description
        if hint is not None:
            self.hint = hint
        if favorites is not None:
            self.favorites = favorites
        if pm_only is not None:
            self.pm_only = pm_only

    def __str__(self):
        return self.wp

    def __eq__(self, other):
        return self.wp == other.wp

    @property
    def wp(self):
        return self._wp

    @wp.setter
    def wp(self, wp):
        wp = str(wp).upper().strip()
        if not wp.startswith("GC"):
            raise ValueError("Waypoint '{}' doesn't start with 'GC'.".format(wp))
        self._wp = wp

    @property
    def geocaching(self):
        return self._geocaching

    @geocaching.setter
    def geocaching(self, geocaching):
        if not hasattr(geocaching, "load_cache"):
            raise ValueError("Passed object (type: '{}') doesn't contain 'load_cache' method.".format(type(geocaching)))
        self._geocaching = geocaching

    @property
    @lazy_loaded
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        name = str(name).strip()
        self._name = name

    @property
    @lazy_loaded
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        if type(location) is str:
            location = Point.from_string(location)
        elif type(location) is not Point:
            raise ValueError("Passed object is not Point instance nor string containing coordinates.")
        self._location = location

    @property
    @lazy_loaded
    def cache_type(self):
        return self._cache_type

    @cache_type.setter
    def cache_type(self, cache_type):
        cache_type = cache_type.strip()
        cache_type = cache_type.replace("Geocache", "Cache")
        if cache_type in self._possible_types.values():  # try to search in values
            self._cache_type = cache_type
        elif cache_type in self._possible_types.keys():  # not in values => it must be a key
            self._cache_type = self._possible_types[cache_type]
        else:
            raise ValueError("Cache type '{}' is not possible.".format(cache_type))

    @property
    @lazy_loaded
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = bool(state)

    @property
    @lazy_loaded
    def found(self):
        return self._found

    @found.setter
    def found(self, found):
        self._found = bool(found)

    @property
    @lazy_loaded
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        size = size.strip().lower()
        if size in self._possible_sizes.values():  # try to search in values
            self._size = size
        elif size in self._possible_sizes.keys():  # not in values => it must be a key
            self._size = self._possible_sizes[size]
        else:
            raise ValueError("Size '{}' is not possible.".format(size))

    @property
    @lazy_loaded
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        difficulty = float(difficulty)
        if difficulty < 1 or difficulty > 5 or difficulty * 10 % 5 != 0:  # X.0 or X.5
            raise ValueError("Difficulty must be from 1 to 5 and divisible by 0.5.")
        self._difficulty = difficulty

    @property
    @lazy_loaded
    def terrain(self):
        return self._terrain

    @terrain.setter
    def terrain(self, terrain):
        terrain = float(terrain)
        if terrain < 1 or terrain > 5 or terrain * 10 % 5 != 0:  # X.0 or X.5
            raise ValueError("Terrain must be from 1 to 5 and divisible by 0.5.")
        self._terrain = terrain

    @property
    @lazy_loaded
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        author = str(author).strip()
        self._author = author

    @property
    @lazy_loaded
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        if type(hidden) is str:
            hidden = Util.parse_date(hidden)
        elif type(hidden) is not datetime.date:
            raise ValueError("Passed object is not datetime.date instance nor string containing date.")
        self._hidden = hidden

    @property
    @lazy_loaded
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        if type(attributes) is not dict:
            raise ValueError("Attribues is not dict.")

        self._attributes = {}
        for name, allowed in attributes.items():
            name = name.strip()
            if name in self._possible_attributes:
                self._attributes[name] = allowed
            else:
                logging.warning("Unknown attribute '%s', ignoring.", name)

    @property
    @lazy_loaded
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        summary = str(summary).strip()
        self._summary = summary

    @property
    @lazy_loaded
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        description = str(description).strip()
        self._description = description

    @property
    @lazy_loaded
    def hint(self):
        return self._hint

    @hint.setter
    def hint(self, hint):
        hint = str(hint).strip()
        self._hint = hint

    @property
    @lazy_loaded
    def favorites(self):
        return self._favorites

    @favorites.setter
    def favorites(self, favorites):
        self._favorites = int(favorites)

    @property
    def pm_only(self):
        return self._pm_only

    @pm_only.setter
    def pm_only(self, pm_only):
        self._pm_only = bool(pm_only)

    def inside_area(self, area):
        """Calculate if geocache is inside given area"""
        return area.inside_area(self.location)
