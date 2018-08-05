from save_to_db.core.exceptions import ItemsNotTheSame
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase



class TestMergeItems(TestBase):
    """ Contains tests for merging items in a list that refer to the same item.
    """
    
    ModelGeneralOne = None
    ModelGeneralTwo = None
    
    
    def test_bulk_item_compress(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            allow_merge_items = True
            getters = [['f_integer', 'f_float'], ['parent_x_1']]
        
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            allow_merge_items = True
            getters = [['f_integer', 'f_float'], ['parent_x_1']]
        
        # simple merge ---------------------------------------------------------
        def gen_items_simple():
            bulk = ItemGeneralOne.Bulk()
            for f_integer in range(2):
                for f_float in range(2):
                    for _ in range(2):
                        bulk.gen(f_integer=f_integer,
                                 f_float=f_float)
            return bulk
        
        # --- no exception ---
        simple = gen_items_simple()
        
        # still items must be merged
        simple[0](f_string='Zero')
        simple[1](f_text='One')
        
        simple.process()

        expected = [
            {'f_float': 0.0, 'f_integer': 0,
             'f_string': 'Zero', 'f_text': 'One'},  # merged different fields
            {'f_float': 1.0, 'f_integer': 0},
            {'f_float': 0.0, 'f_integer': 1},
            {'f_float': 1.0, 'f_integer': 1},
        ]
        self.assertEqual(simple.to_dict()['bulk'], expected)
        
        # --- cannot merge ---
        simple = gen_items_simple()
        simple[0](f_string='Zero')
        simple[1](f_string='One')
        with self.assertRaises(ItemsNotTheSame):
            simple.process()
        
        # merge with related items ---------------------------------------------
        def gen_items_with_parent():
            bulk = ItemGeneralOne.Bulk()
            parents = [
                ItemGeneralTwo(f_integer=0, f_float=0, f_string='Zero'),
                ItemGeneralTwo(f_integer=0, f_float=0, f_text='One'),
            ]
            
            for i in range(2):
                for _ in range(2):
                    bulk.gen(parent_x_1=parents[i])
                    
            # this items won't be merged (two objects, although the same)
            bulk.gen(parent_x_1=ItemGeneralTwo(f_integer=1, f_float=1))
            bulk.gen(parent_x_1=ItemGeneralTwo(f_integer=1, f_float=1))
                    
            return bulk
        
        # --- no exception ---
        with_parent = gen_items_with_parent()
        
        # still items must be merged
        with_parent[0](f_string='Zero')
        with_parent[1](f_text='One')
        
        with_parent.process()
        
        expected = [
            # two items merged
            {
                'f_string': 'Zero',
                'f_text': 'One',
                 'parent_x_1': {
                    'f_float': 0.0,
                     'f_integer': 0,
                     'f_string': 'Zero'
                 }
            },
            # but parent was not merged (should be merged in later versions)
            {'parent_x_1': {'f_float': 0.0, 'f_integer': 0, 'f_text': 'One'}},
            {'parent_x_1': {'f_float': 1.0, 'f_integer': 1}},
            {'parent_x_1': {'f_float': 1.0, 'f_integer': 1}}
        ]
        self.assertEqual(with_parent.to_dict()['bulk'], expected)
        
        # last two items are still different objects
        # (should be merged in later versions)
        with_parent_as_list = with_parent.as_list()
        self.assertEqual(with_parent_as_list[-1].to_dict(),
                         with_parent_as_list[-2].to_dict())
        self.assertIsNot(with_parent_as_list[-1], with_parent_as_list[-2])

        # --- cannot merge ---
        with_parent = gen_items_with_parent()
        with_parent[0](f_string='Zero')
        with_parent[1](f_string='One')
        with self.assertRaises(ItemsNotTheSame):
            with_parent.process()
            
    
    def test_allow_merge_setting(self):
        
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            allow_merge_items = True
            getters = [['f_integer', 'f_float'], ['parent_x_1']]
        
        # default `allow_merge_items` is False
        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            getters = [['f_integer', 'f_float'], ['parent_x_1']]
            
        
        def gen_items(bulk):
            for f_integer in range(2):
                for f_float in range(2):
                    for _ in range(2):
                        bulk.gen(f_integer=f_integer,
                                 f_float=f_float)
            return bulk
        
        # not overwritten ------------------------------------------------------
        bulk = ItemGeneralOne.Bulk()
        gen_items(bulk)
        bulk_len = len(bulk)
        bulk.process()
        self.assertLess(len(bulk), bulk_len)  # items were merged
        
        bulk = ItemGeneralTwo.Bulk()
        gen_items(bulk)
        bulk_len = len(bulk)
        bulk.process()
        self.assertEqual(len(bulk), bulk_len)  # items were not merged
        
        # overwritten ----------------------------------------------------------
        bulk = ItemGeneralOne.Bulk()
        bulk.allow_merge_items = False
        gen_items(bulk)
        bulk_len = len(bulk)
        bulk.process()
        self.assertEqual(len(bulk), bulk_len)  # items were not merged
        
        bulk = ItemGeneralTwo.Bulk()
        bulk.allow_merge_items = True
        gen_items(bulk)
        bulk_len = len(bulk)
        bulk.process()
        self.assertLess(len(bulk), bulk_len)  # items were merged
    
    
    