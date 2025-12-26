CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT, -- PII: SENSITIVE
    role TEXT   -- 'vip', 'staff', 'guest'
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    type TEXT, -- 'standard', 'vip'
    price DECIMAL(10,2),
    purchase_date DATETIME
);
