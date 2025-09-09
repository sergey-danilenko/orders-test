CREATE TRIGGER trg_category_insert_closure
AFTER INSERT ON categories
FOR EACH ROW
BEGIN
    INSERT INTO category_trees (ancestor_id, descendant_id, depth)
    VALUES (NEW.id, NEW.id, 0);

    INSERT INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT ancestor_id, NEW.id, depth + 1
    FROM category_trees
    WHERE descendant_id = NEW.parent_id;
END;