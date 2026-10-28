# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured"


class ItemUpdater:
    """Shared quality adjustment helpers for item updaters."""

    def _increase_quality(self, item):
        if item.quality < 50:
            item.quality = item.quality + 1

    def _decrease_quality(self, item):
        if item.quality > 0:
            item.quality = item.quality - 1


class NormalItemUpdater(ItemUpdater):
    def update(self, item):
        self._decrease_quality(item)
        item.sell_in -= 1

        if item.sell_in < 0:
            self._decrease_quality(item)


class AgedBrieUpdater(ItemUpdater):
    def update(self, item):
        self._increase_quality(item)
        item.sell_in -= 1

        if item.sell_in < 0:
            self._increase_quality(item)


class BackstagePassUpdater(ItemUpdater):
    def update(self, item):
        self._increase_quality(item)

        if item.sell_in < 11:
            self._increase_quality(item)

        if item.sell_in < 6:
            self._increase_quality(item)

        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = 0


class ConjuredItemUpdater(ItemUpdater):
    def update(self, item):
        self._decrease_quality(item)
        self._decrease_quality(item)
        item.sell_in -= 1

        if item.sell_in < 0:
            self._decrease_quality(item)
            self._decrease_quality(item)


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
    """Select the updater that handles this item."""
    if item.name.startswith(CONJURED):
        return CONJURED_UPDATER

    return UPDATERS.get(item.name, NORMAL_UPDATER)


class GildedRose(object):
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
