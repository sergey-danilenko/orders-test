
CREATE TRIGGER trg_category_delete_closure
AFTER DELETE ON categories
FOR EACH ROW
BEGIN
    UPDATE categories
    SET parent_id = OLD.parent_id
    WHERE parent_id = OLD.id;

    DELETE FROM category_trees
    WHERE ancestor_id = OLD.id OR descendant_id = OLD.id;

    INSERT OR IGNORE INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT super.ancestor_id, sub.descendant_id, super.depth + sub.depth + 1
    FROM category_trees AS super
    JOIN category_trees AS sub
      ON super.descendant_id = OLD.parent_id
     AND sub.ancestor_id IN (
         SELECT id FROM categories WHERE parent_id = OLD.parent_id
     );

    INSERT OR IGNORE INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT id, id, 0
    FROM categories
    WHERE parent_id = OLD.parent_id;
END;
