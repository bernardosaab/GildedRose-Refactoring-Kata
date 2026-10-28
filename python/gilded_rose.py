# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured"

MIN_QUALITY = 0
MAX_QUALITY = 50

BACKSTAGE_DOUBLE_BONUS_THRESHOLD = 11
BACKSTAGE_TRIPLE_BONUS_THRESHOLD = 6


class ItemUpdater:
    """Shared quality adjustment helpers for item updaters."""

    def _increase_quality(self, item, amount=1):
        if item.quality < MAX_QUALITY:
            item.quality = min(MAX_QUALITY, item.quality + amount)

    def _decrease_quality(self, item, amount=1):
        if item.quality > MIN_QUALITY:
            item.quality = max(MIN_QUALITY, item.quality - amount)


class NormalItemUpdater(ItemUpdater):
    """Updates normal items, with a configurable degradation rate."""

    def __init__(self, degrade_rate=1):
        self.degrade_rate = degrade_rate

    def update(self, item):
        self._decrease_quality(item, self.degrade_rate)
        item.sell_in -= 1

        if item.sell_in < 0:
            self._decrease_quality(item, self.degrade_rate)


class AgedBrieUpdater(ItemUpdater):
    def update(self, item):
        self._increase_quality(item)
        item.sell_in -= 1

        if item.sell_in < 0:
            self._increase_quality(item)


class BackstagePassUpdater(ItemUpdater):
    def update(self, item):
        self._increase_quality(item)

        if item.sell_in < BACKSTAGE_DOUBLE_BONUS_THRESHOLD:
            self._increase_quality(item)

        if item.sell_in < BACKSTAGE_TRIPLE_BONUS_THRESHOLD:
            self._increase_quality(item)

        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = MIN_QUALITY


class ConjuredItemUpdater(NormalItemUpdater):
    """Conjured items degrade twice as fast as normal items."""

    def __init__(self):
        super().__init__(degrade_rate=2)


class SulfurasUpdater(ItemUpdater):
    def update(self, item):
        # Sulfuras never changes.
        pass


# Updaters are stateless, so one shared instance of each is enough.
UPDATERS = {
    AGED_BRIE: AgedBrieUpdater(),
    SULFURAS: SulfurasUpdater(),
    BACKSTAGE_PASSES: BackstagePassUpdater(),
}

CONJURED_UPDATER = ConjuredItemUpdater()
NORMAL_UPDATER = NormalItemUpdater()


def get_updater(item):
    """Select by Conjured prefix, exact-name registration, or normal item fallback."""
    if item.name.startswith(CONJURED):
        return CONJURED_UPDATER

    return UPDATERS.get(item.name, NORMAL_UPDATER)


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            get_updater(item).update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
