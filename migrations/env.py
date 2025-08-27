from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Make sure Alembic can import your app's models
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import Base from your models
from backend.database import Base  # Adjust path to your project
from backend.models import item, warehouse,bom,production_order,purchase,uom,uom_conversion,stock_transaction,inventory,wip,sales # This ensures all models are imported

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set target_metadata for 'autogenerate'
target_metadata = Base.metadata

# Allow DATABASE_URL from environment or alembic.ini
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,   # Detect column type changes
        compare_server_default=True , # Detect server defaults
        render_as_batch=True,  
        include_object=lambda obj, name, type_, reflected, compare_to:
        True  # or add logic to ignore certain differences
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True ,
            include_object=lambda obj, name, type_, reflected, compare_to:
            True  # or add logic to ignore certain differences
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
