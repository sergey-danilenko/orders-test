
CREATE TRIGGER trg_category_update_closure
AFTER UPDATE OF parent_id ON categories
FOR EACH ROW
BEGIN
    DELETE FROM category_trees
    WHERE descendant_id IN (
        SELECT descendant_id
        FROM category_trees
        WHERE ancestor_id = OLD.id
    )
    AND ancestor_id NOT IN (
        SELECT descendant_id
        FROM category_trees
        WHERE ancestor_id = OLD.id
    )
    AND descendant_id != ancestor_id;

    INSERT INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT super.ancestor_id, sub.descendant_id, super.depth + sub.depth + 1
    FROM category_trees AS super
    JOIN category_trees AS sub
        ON super.descendant_id = NEW.parent_id
      AND sub.ancestor_id = NEW.id;
END;
