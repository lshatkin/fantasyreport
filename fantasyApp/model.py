"""Insta485 model (database) API."""
import sqlite3
import flask
import app


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary."""
    output = {}
    for idx, col in enumerate(cursor.description):
        output[col[0]] = row[idx]
    return output


def query_db(query, args=(), one=False):
    """Query from the database."""
    cur = get_db().execute(query, args)
    r_v = cur.fetchall()
    cur.close()
    return (r_v[0] if r_v else None) if one else r_v


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db = sqlite3.connect(
            insta485.app.config['DATABASE_FILENAME'])
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@insta485.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request."""
    # Assertion needed to avoid style error
    assert error or not error
    if hasattr(flask.g, 'sqlite_db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()
