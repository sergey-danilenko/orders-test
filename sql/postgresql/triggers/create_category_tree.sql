-- Insert new Category
CREATE OR REPLACE FUNCTION category_tree_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO category_trees(ancestor_id, descendant_id, depth)
    VALUES (NEW.id, NEW.id, 0);

    IF NEW.parent_id IS NOT NULL THEN
        INSERT INTO category_trees(ancestor_id, descendant_id, depth)
        SELECT ancestor_id, NEW.id, depth + 1
        FROM category_trees
        WHERE descendant_id = NEW.parent_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_category_insert_closure
AFTER INSERT ON categories
FOR EACH ROW
EXECUTE FUNCTION category_tree_insert();

-- Update Parent
CREATE OR REPLACE FUNCTION category_tree_update() RETURNS TRIGGER AS $$
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

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_category_update_closure
AFTER UPDATE OF parent_id ON categories
FOR EACH ROW
EXECUTE FUNCTION category_tree_update();

-- Delete Category
CREATE OR REPLACE FUNCTION category_tree_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE categories
    SET parent_id = OLD.parent_id
    WHERE parent_id = OLD.id;

    DELETE FROM category_trees
    WHERE ancestor_id = OLD.id OR descendant_id = OLD.id;

    INSERT INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT super.ancestor_id, sub.descendant_id, super.depth + sub.depth + 1
    FROM category_trees AS super
    JOIN category_trees AS sub
      ON super.descendant_id = OLD.parent_id
     AND sub.ancestor_id IN (
         SELECT id FROM categories WHERE parent_id = OLD.parent_id
     )
    ON CONFLICT (ancestor_id, descendant_id) DO NOTHING;

    INSERT INTO category_trees (ancestor_id, descendant_id, depth)
    SELECT id, id, 0
    FROM categories
    WHERE parent_id = OLD.parent_id
    ON CONFLICT (ancestor_id, descendant_id) DO NOTHING;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_category_delete_closure
AFTER DELETE ON categories
FOR EACH ROW
EXECUTE FUNCTION category_tree_delete();

