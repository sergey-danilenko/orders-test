
DROP TRIGGER IF EXISTS trg_category_insert_closure ON categories;
DROP TRIGGER IF EXISTS trg_category_update_closure ON categories;
DROP TRIGGER IF EXISTS trg_category_delete_closure ON categories;

DROP FUNCTION IF EXISTS category_tree_insert();
DROP FUNCTION IF EXISTS category_tree_update();
DROP FUNCTION IF EXISTS category_tree_delete();
