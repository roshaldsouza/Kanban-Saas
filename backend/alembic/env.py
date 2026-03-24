from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# So Alembic can find your app/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.core.database import Base
from app.core.config import settings
from app.users.models import User  # noqa: F401
from app.core.database import Base
from app.core.config import settings

# Alembic Config object — gives access to alembic.ini values
config = context.config

# Override sqlalchemy.url from your .env via pydantic settings
# Alembic uses a sync driver, so we strip +asyncpg from the URL
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL.replace("+asyncpg", "")
)

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is what Alembic diffs to generate migrations
# It must see all your models — you'll import them here later
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without a live DB connection.
    Useful for generating raw SQL scripts.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations with a live DB connection.
    This is what actually executes when you run:
        alembic upgrade head
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# Alembic calls whichever mode is appropriate
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()