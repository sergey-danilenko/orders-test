CREATE TABLE categories (
    id SERIAL NOT NULL,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER,
    create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__categories PRIMARY KEY (id),
    CONSTRAINT fk__categories__parent_id__categories FOREIGN KEY(parent_id) REFERENCES categories (id) ON DELETE SET NULL,
    CONSTRAINT uq__categories__parent_name UNIQUE (parent_id, name)
);

CREATE INDEX ix__categories_name ON categories (name);

CREATE INDEX ix__categories_parent_id ON categories (parent_id);

CREATE TABLE clients (
    id SERIAL NOT NULL,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__clients PRIMARY KEY (id),
    CONSTRAINT uq__clients__name UNIQUE (name)
);

CREATE TABLE category_trees (
    ancestor_id INTEGER NOT NULL,
    descendant_id INTEGER NOT NULL,
    depth INTEGER NOT NULL,
    CONSTRAINT pk__category_trees PRIMARY KEY (ancestor_id, descendant_id),
    CONSTRAINT fk__category_trees__ancestor_id__categories FOREIGN KEY(ancestor_id) REFERENCES categories (id) ON DELETE CASCADE,
    CONSTRAINT fk__category_trees__descendant_id__categories FOREIGN KEY(descendant_id) REFERENCES categories (id) ON DELETE CASCADE
);

CREATE INDEX ix__cc_ancestor ON category_trees (ancestor_id);

CREATE INDEX ix__cc_descendant ON category_trees (descendant_id);

CREATE TABLE orders (
    id SERIAL NOT NULL,
    client_id INTEGER NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__orders PRIMARY KEY (id),
    CONSTRAINT fk__orders__client_id__clients FOREIGN KEY(client_id) REFERENCES clients (id) ON DELETE RESTRICT
);

CREATE INDEX ix__orders_client_id ON orders (client_id);

CREATE INDEX ix__orders_create_date ON orders (create_date);

CREATE TABLE products (
    id SERIAL NOT NULL,
    name VARCHAR(100) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    category_id INTEGER NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    CONSTRAINT pk__products PRIMARY KEY (id),
    CONSTRAINT fk__products__category_id__categories FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE RESTRICT,
    CONSTRAINT uq__products_category_name_model UNIQUE (category_id, name)
);

CREATE INDEX ix__products_category_id ON products (category_id);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    CONSTRAINT pk__order_items PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk__order_items__order_id__orders FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE,
    CONSTRAINT fk__order_items__product_id__products FOREIGN KEY(product_id) REFERENCES products (id) ON DELETE RESTRICT
);

CREATE INDEX ix__order_items_product ON order_items (product_id);

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
EXECUTE FUNCTION category_tree_delete();;
