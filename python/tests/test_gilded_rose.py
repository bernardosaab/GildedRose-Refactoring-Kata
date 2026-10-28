# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

def update_item(name, sell_in, quality):
    """Create an item, run one day of updates, and return the item."""
    item = Item(name, sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    return item

class GildedRoseTest(unittest.TestCase):
    def test_update_does_not_change_name(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)


class NormalItemTest(unittest.TestCase):
    def test_quality_and_sell_in_drop(self):
        item = update_item("+5 Dexterity Vest", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(19, item.quality)

    def test_quality_and_sell_in_drop_twice_as_fast(self):
        # Twice as fast on the sell-by day
        item = update_item("+5 Dexterity Vest", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_quality_drops_twice_as_fast_after_sell_by(self):
        item = update_item("+5 Dexterity Vest", -1, 5)
        self.assertEqual(-2, item.sell_in)
        self.assertEqual(3, item.quality)

    def test_quality_never_negative(self):
        item = update_item("+5 Dexterity Vest", 5, 0)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_quality_never_negative_when_degrading_twice(self):
        item = update_item("+5 Dexterity Vest", 0, 1)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)



class AgedBrieTest(unittest.TestCase):
    def test_quality_increases_for_aged_brie(self):
        item = update_item("Aged Brie", 10, 10)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(11, item.quality)

    def test_quality_never_exceeds_50_for_aged_brie(self):
        item = update_item("Aged Brie", 10, 50)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_increases_twice_as_fast_after_sell_by_for_aged_brie(self):
        item = update_item("Aged Brie", 0, 10)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_quality_increases_twice_as_fast_after_sell_by_for_aged_brie_never_exceeds_50(self):
        item = update_item("Aged Brie", 0, 49)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(50, item.quality)

class SulfurasTest(unittest.TestCase):
    def test_quality_and_sell_in_do_not_change_for_sulfuras(self):
        item = update_item("Sulfuras, Hand of Ragnaros", 10, 80)
        self.assertEqual(10, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_quality_and_sell_in_do_not_change_for_sulfuras_after_sell_by(self):
        item = update_item("Sulfuras, Hand of Ragnaros", 0, 80)
        self.assertEqual(0, item.sell_in)
        self.assertEqual(80, item.quality)

    def test_quality_and_sell_in_do_not_change_for_sulfuras_after_sell_by_negative_sell_in(self):
        item = update_item("Sulfuras, Hand of Ragnaros", -1, 80)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(80, item.quality)

class BackstagePassesTest(unittest.TestCase):
    def test_quality_increases_by_2_when_10_days_or_less_for_backstage_passes(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 10, 10)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_quality_increases_by_3_when_5_days_or_less_for_backstage_passes(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 5, 10)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(13, item.quality)

    def test_quality_drops_to_0_after_concert_for_backstage_passes(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 0, 10)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_quality_increases_by_1_when_more_than_10_days_for_backstage_passes(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 11, 10)
        self.assertEqual(10, item.sell_in)
        self.assertEqual(11, item.quality)

    def test_quality_never_exceeds_50_for_backstage_passes(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 5, 49)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_never_exceeds_50_for_backstage_passes_with_high_quality(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 1, 50)
        self.assertEqual(0, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_increases_by_2_when_10_days_or_less_for_backstage_passes_with_high_quality(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 10, 49)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_increases_by_3_when_5_days_or_less_for_backstage_passes_with_high_quality(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 5, 48)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_increases_by_1_when_more_than_10_days_for_backstage_passes_with_high_quality(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 11, 49)
        self.assertEqual(10, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_quality_drops_to_0_after_concert_for_backstage_passes_with_high_quality(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 0, 50)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_quality_increases_by_2_when_6_days_remaining(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 6, 10)
        self.assertEqual(5, item.sell_in)
        self.assertEqual(12, item.quality)

    def test_quality_increases_by_3_when_1_day_remaining(self):
        item = update_item("Backstage passes to a TAFKAL80ETC concert", 1, 10)
        self.assertEqual(0, item.sell_in)
        self.assertEqual(13, item.quality)

class ConjuredItemTest(unittest.TestCase):

    def test_conjured_item_degrades_twice_as_fast(self):
        item = update_item("Conjured Mana Cake", 5, 10)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(8, item.quality)

    def test_conjured_item_degrades_by_4_on_sell_in_date(self):
        item = update_item("Conjured Mana Cake", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(16, item.quality)

    def test_conjured_item_degrades_by_4_after_sell_in_date(self):
        item = update_item("Conjured Mana Cake", -1, 10)
        self.assertEqual(-2, item.sell_in)
        self.assertEqual(6, item.quality)

    def test_conjured_item_quality_never_negative_degrades_by_4(self):
        item = update_item("Conjured Mana Cake", 0, 3)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_conjured_item_quality_never_negative_degrades_by_2(self):
        item = update_item("Conjured Mana Cake", 5, 1)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_conjured_item_quality_stays_non_negative(self):
        item = update_item("Conjured Mana Cake", 5, 0)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)


if __name__ == '__main__':
    unittest.main()
