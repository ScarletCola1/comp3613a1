import logging
import threading
import time
from contextlib import contextmanager

from sqlalchemy import inspect
from sqlalchemy.exc import DBAPIError, OperationalError, ProgrammingError
from sqlmodel import SQLModel, Session, create_engine

from app.config import get_settings

logger = logging.getLogger(__name__)

_schema_lock = threading.Lock()


def sqlalchemy_uri(uri: str) -> str:
    """Accept Render's postgres:// URLs in the sync SQLAlchemy engine."""
    if uri.startswith("postgres://"):
        return "postgresql+psycopg2://" + uri[len("postgres://") :]
    if uri.startswith("postgresql://"):
        return "postgresql+psycopg2://" + uri[len("postgresql://") :]
    return uri


engine = create_engine(
    sqlalchemy_uri(get_settings().database_uri),
    echo=get_settings().env.lower()
    in ["dev", "development", "test", "testing", "staging"],
    pool_size=get_settings().db_pool_size,
    max_overflow=get_settings().db_additional_overflow,
    pool_timeout=get_settings().db_pool_timeout,
    pool_recycle=get_settings().db_pool_recycle,
)


def create_db_and_tables() -> None:
    # Ensure model modules are imported so tables are registered on metadata.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _migrate_review_booking_index()


def _migrate_review_booking_index() -> None:
    """Allow multiple reviews per booking in databases with the old unique index."""
    if engine.dialect.name != "sqlite":
        return

    from app.models.review import Review

    inspector = inspect(engine)
    if not inspector.has_table(Review.__tablename__):
        return

    booking_index = next(
        (
            index
            for index in Review.__table__.indexes
            if [column.name for column in index.columns] == ["booking_id"]
            and not index.unique
        ),
        None,
    )
    if booking_index is None:
        return

    stale_unique_indexes = [
        index
        for index in inspector.get_indexes(Review.__tablename__)
        if index.get("unique")
        and index.get("column_names") == ["booking_id"]
        and index.get("name") == booking_index.name
    ]
    if not stale_unique_indexes:
        return

    with engine.begin() as connection:
        quote = connection.dialect.identifier_preparer.quote
        for index in stale_unique_indexes:
            name = index.get("name")
            if name is None:
                raise RuntimeError("Cannot migrate an unnamed review booking index.")
            connection.exec_driver_sql(f"DROP INDEX {quote(name)}")
        booking_index.create(connection, checkfirst=True)
    logger.info("Migrated review booking index to allow multiple reviews per booking")


def drop_all() -> None:
    SQLModel.metadata.drop_all(bind=engine)


def is_db_not_ready_error(exc: BaseException) -> bool:
    """True when Postgres is unreachable or the schema/tables are missing."""
    if isinstance(exc, OperationalError):
        return True
    if isinstance(exc, ProgrammingError):
        return True
    if isinstance(exc, DBAPIError) and getattr(exc, "connection_invalidated", False):
        return True

    text = str(exc).lower()
    markers = (
        "does not exist",
        "undefinedtable",
        "undefined table",
        "no such table",
        "relation ",
        "could not connect",
        "connection refused",
        "connection timed out",
        "server closed the connection",
        "the database system is starting up",
        "remaining connection slots",
        "too many connections",
        "ssl connection has been closed",
    )
    return any(m in text for m in markers)


def ensure_db_and_tables(
    *,
    retries: int = 8,
    delay_seconds: float = 2.0,
) -> None:
    """Create tables, retrying while the prod DB is still coming up."""
    last: BaseException | None = None
    for attempt in range(1, retries + 1):
        try:
            with _schema_lock:
                create_db_and_tables()
            if attempt > 1:
                logger.info("Database schema ready after %s attempt(s)", attempt)
            return
        except Exception as exc:  # noqa: BLE001 — first-boot resilience
            last = exc
            if not is_db_not_ready_error(exc) or attempt >= retries:
                raise
            logger.warning(
                "Database not ready (attempt %s/%s): %s",
                attempt,
                retries,
                exc,
            )
            time.sleep(delay_seconds * attempt)
    if last is not None:
        raise last


def recover_if_uninitialized(exc: BaseException) -> bool:
    """If *exc* looks like a missing schema, create tables and return True."""
    if not is_db_not_ready_error(exc):
        return False
    logger.warning("Uninitialized database detected; creating tables: %s", exc)
    ensure_db_and_tables()
    return True


def _session_generator():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()


def get_session():
    yield from _session_generator()


@contextmanager
def get_cli_session():
    yield from _session_generator()
