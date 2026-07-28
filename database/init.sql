CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL DEFAULT 'Other',
    severity VARCHAR(20) NOT NULL DEFAULT 'Medium',
    status VARCHAR(30) NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL
);


CREATE TABLE IF NOT EXISTS ai_analyses (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER NOT NULL
        REFERENCES incidents(id)
        ON DELETE CASCADE,
    analysis TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_incidents_status
ON incidents(status);

CREATE INDEX IF NOT EXISTS idx_incidents_created
ON incidents(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ai_incident
ON ai_analyses(incident_id);