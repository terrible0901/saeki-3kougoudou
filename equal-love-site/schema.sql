PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    edition TEXT NOT NULL,
    release_date TEXT NOT NULL,
    image TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    nickname TEXT NOT NULL CHECK(length(nickname) BETWEEN 1 AND 30),
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    review_title TEXT NOT NULL CHECK(length(review_title) BETWEEN 1 AND 60),
    comment TEXT NOT NULL CHECK(length(comment) BETWEEN 10 AND 800),
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT,
    is_sample INTEGER NOT NULL DEFAULT 0,
    seed_key TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_reviews_album_id ON reviews(album_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_reviews_seed_key
ON reviews(seed_key)
WHERE seed_key IS NOT NULL;
