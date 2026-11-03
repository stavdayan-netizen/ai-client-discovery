-- Initial schema (architecture.md section 3.2).
-- Timestamps: UTC ISO-8601 text. IDs: opaque text. JSON columns are validated with json_valid.
-- This file runs inside a transaction opened by the migration runner.

CREATE TABLE leads (
  id           TEXT PRIMARY KEY,
  company_name TEXT NOT NULL CHECK (length(trim(company_name)) > 0),
  contact_name TEXT,
  email        TEXT NOT NULL CHECK (length(trim(email)) > 0),
  phone        TEXT NOT NULL CHECK (length(trim(phone)) > 0),
  status       TEXT NOT NULL DEFAULT 'חדש'
               CHECK (status IN ('חדש', 'ממתין למילוי', 'התקבל', 'בבדיקה', 'הושלם')),
  created_at   TEXT NOT NULL,
  updated_at   TEXT NOT NULL
);

CREATE TABLE lead_status_history (
  id          TEXT PRIMARY KEY,
  lead_id     TEXT NOT NULL REFERENCES leads (id),
  from_status TEXT CHECK (from_status IS NULL
                          OR from_status IN ('חדש', 'ממתין למילוי', 'התקבל', 'בבדיקה', 'הושלם')),
  to_status   TEXT NOT NULL
              CHECK (to_status IN ('חדש', 'ממתין למילוי', 'התקבל', 'בבדיקה', 'הושלם')),
  changed_at  TEXT NOT NULL,
  changed_by  TEXT NOT NULL,
  reason      TEXT
);
CREATE INDEX idx_status_history_lead ON lead_status_history (lead_id, changed_at);

CREATE TABLE template_versions (
  id             TEXT PRIMARY KEY,
  version_number INTEGER NOT NULL UNIQUE CHECK (version_number >= 1),
  state          TEXT NOT NULL CHECK (state IN ('draft', 'published')),
  intro_text     TEXT NOT NULL,
  title_pattern  TEXT NOT NULL,
  definition     TEXT NOT NULL CHECK (json_valid(definition)),
  created_at     TEXT NOT NULL,
  published_at   TEXT,
  CHECK ((state = 'published') = (published_at IS NOT NULL))
);
-- At most one draft at a time.
CREATE UNIQUE INDEX one_draft_template ON template_versions (state) WHERE state = 'draft';
-- Published versions are immutable.
CREATE TRIGGER template_versions_no_update
BEFORE UPDATE ON template_versions
WHEN OLD.state = 'published'
BEGIN
  SELECT RAISE(ABORT, 'published template versions are immutable');
END;
CREATE TRIGGER template_versions_no_delete
BEFORE DELETE ON template_versions
WHEN OLD.state = 'published'
BEGIN
  SELECT RAISE(ABORT, 'published template versions are immutable');
END;

CREATE TABLE questionnaire_instances (
  id                   TEXT PRIMARY KEY,
  lead_id              TEXT NOT NULL REFERENCES leads (id),
  template_version_id  TEXT NOT NULL REFERENCES template_versions (id),
  definition_snapshot  TEXT NOT NULL CHECK (json_valid(definition_snapshot)),
  state                TEXT NOT NULL DEFAULT 'active' CHECK (state IN ('active', 'void')),
  phase                TEXT NOT NULL DEFAULT 'base'
                       CHECK (phase IN ('base', 'followups', 'submitted')),
  token_hash           TEXT NOT NULL UNIQUE,
  link_revoked_at      TEXT,
  link_expires_at      TEXT,
  sent_at              TEXT,
  first_opened_at      TEXT,
  first_answer_at      TEXT,
  last_activity_at     TEXT,
  base_completed_at    TEXT,
  submitted_at         TEXT,
  created_at           TEXT NOT NULL,
  -- Only a final submission sets submitted_at, and it always moves the phase to 'submitted'.
  CHECK ((phase = 'submitted') = (submitted_at IS NOT NULL))
);
-- One active questionnaire per lead.
CREATE UNIQUE INDEX one_active_instance_per_lead
  ON questionnaire_instances (lead_id) WHERE state = 'active';

CREATE TABLE answers (
  instance_id    TEXT NOT NULL REFERENCES questionnaire_instances (id),
  question_id    TEXT NOT NULL,
  value          TEXT CHECK (value IS NULL OR json_valid(value)),
  marked_unknown INTEGER NOT NULL DEFAULT 0 CHECK (marked_unknown IN (0, 1)),
  version        INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
  last_change_id TEXT,
  updated_at     TEXT NOT NULL,
  PRIMARY KEY (instance_id, question_id),
  -- "Unknown" marker on a date or contact group never coexists with an actual value.
  CHECK (marked_unknown = 0 OR value IS NULL)
);

CREATE TABLE ai_analysis_runs (
  id               TEXT PRIMARY KEY,
  instance_id      TEXT NOT NULL REFERENCES questionnaire_instances (id),
  kind             TEXT NOT NULL CHECK (kind IN ('follow_ups', 'analysis')),
  provider         TEXT NOT NULL,
  model            TEXT,
  is_simulated     INTEGER NOT NULL CHECK (is_simulated IN (0, 1)),
  prompt_version   TEXT NOT NULL,
  input_hash       TEXT NOT NULL,
  status           TEXT NOT NULL CHECK (status IN ('pending', 'succeeded', 'failed')),
  output           TEXT CHECK (output IS NULL OR json_valid(output)),
  error            TEXT,
  created_at       TEXT NOT NULL,
  lease_expires_at TEXT,
  completed_at     TEXT,
  CHECK (status <> 'pending' OR lease_expires_at IS NOT NULL)
);
-- At most one live (pending) or successful run per instance and kind.
CREATE UNIQUE INDEX one_live_or_successful_run
  ON ai_analysis_runs (instance_id, kind) WHERE status IN ('pending', 'succeeded');

CREATE TABLE follow_up_questions (
  id                  TEXT PRIMARY KEY,
  instance_id         TEXT NOT NULL REFERENCES questionnaire_instances (id),
  ai_run_id           TEXT NOT NULL REFERENCES ai_analysis_runs (id),
  ordinal             INTEGER NOT NULL CHECK (ordinal BETWEEN 1 AND 5),
  text                TEXT NOT NULL CHECK (length(trim(text)) > 0),
  rationale           TEXT NOT NULL,
  source_question_ids TEXT NOT NULL CHECK (json_valid(source_question_ids)),
  status              TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending', 'answered', 'skipped')),
  answer_text         TEXT,
  answered_at         TEXT,
  UNIQUE (instance_id, ordinal)
);

CREATE TABLE fill_sessions (
  id                TEXT PRIMARY KEY,
  instance_id       TEXT NOT NULL REFERENCES questionnaire_instances (id),
  started_at        TEXT NOT NULL,
  last_heartbeat_at TEXT NOT NULL,
  ended_at          TEXT,
  end_reason        TEXT CHECK (end_reason IS NULL OR end_reason IN
                      ('explicit_save', 'idle', 'hidden', 'submitted', 'unknown')),
  active_seconds    INTEGER NOT NULL DEFAULT 0 CHECK (active_seconds >= 0)
);
CREATE INDEX idx_fill_sessions_instance ON fill_sessions (instance_id, started_at);

CREATE TABLE progress_events (
  id             TEXT PRIMARY KEY,
  instance_id    TEXT NOT NULL REFERENCES questionnaire_instances (id),
  session_id     TEXT REFERENCES fill_sessions (id),
  type           TEXT NOT NULL CHECK (length(type) > 0),
  completion_pct REAL CHECK (completion_pct IS NULL OR completion_pct BETWEEN 0 AND 100),
  at             TEXT NOT NULL,
  meta           TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(meta))
);
CREATE INDEX idx_progress_events_instance ON progress_events (instance_id, at);

CREATE TABLE contacts (
  id                 TEXT PRIMARY KEY,
  lead_id            TEXT NOT NULL REFERENCES leads (id),
  name               TEXT NOT NULL CHECK (length(trim(name)) > 0),
  role               TEXT,
  responsibility     TEXT,
  phone              TEXT,
  email              TEXT,
  origin             TEXT NOT NULL CHECK (origin IN ('extracted', 'manual')),
  is_sponsor         INTEGER NOT NULL DEFAULT 0 CHECK (is_sponsor IN (0, 1)),
  source_instance_id TEXT REFERENCES questionnaire_instances (id),
  source_question_id TEXT,
  dedupe_key         TEXT NOT NULL,
  created_at         TEXT NOT NULL,
  updated_at         TEXT NOT NULL,
  removed_at         TEXT,
  -- A removed (soft-deleted) contact keeps its key, so extraction never re-creates it.
  UNIQUE (lead_id, dedupe_key)
);

CREATE TABLE internal_notes (
  id           TEXT PRIMARY KEY,
  lead_id      TEXT NOT NULL REFERENCES leads (id),
  instance_id  TEXT REFERENCES questionnaire_instances (id),
  question_id  TEXT,
  follow_up_id TEXT REFERENCES follow_up_questions (id),
  author_label TEXT NOT NULL CHECK (length(trim(author_label)) > 0),
  body         TEXT NOT NULL CHECK (length(trim(body)) > 0),
  created_at   TEXT NOT NULL
);
CREATE INDEX idx_internal_notes_lead ON internal_notes (lead_id, created_at);

-- Append-only tables: notes and status history are never edited or deleted.
CREATE TRIGGER internal_notes_no_update BEFORE UPDATE ON internal_notes
BEGIN SELECT RAISE(ABORT, 'internal_notes is append-only'); END;
CREATE TRIGGER internal_notes_no_delete BEFORE DELETE ON internal_notes
BEGIN SELECT RAISE(ABORT, 'internal_notes is append-only'); END;
CREATE TRIGGER lead_status_history_no_update BEFORE UPDATE ON lead_status_history
BEGIN SELECT RAISE(ABORT, 'lead_status_history is append-only'); END;
CREATE TRIGGER lead_status_history_no_delete BEFORE DELETE ON lead_status_history
BEGIN SELECT RAISE(ABORT, 'lead_status_history is append-only'); END;
