from .database import db

def upgrade():
    # Add the category_id column to the Todo table
    with db.engine.connect() as connection:
        connection.execute("""
            ALTER TABLE todo
            ADD COLUMN category_id INTEGER,
            ADD CONSTRAINT fk_category_id
            FOREIGN KEY (category_id)
            REFERENCES category (id);
        """)

def downgrade():
    # Remove the category_id column from the Todo table
    with db.engine.connect() as connection:
        connection.execute("""
            ALTER TABLE todo
            DROP COLUMN category_id;
        """)