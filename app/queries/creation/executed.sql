
createdb PlantTracker

-- user plant entries with relevant data
CREATE TABLE plants (
    plant_id SERIAL UNIQUE,
    plant_name VARCHAR(100) NOT NULL,
    adoption_date DATE,
    death_date DATE,
    pot_size NUMERIC(4, 2),
    purchase_location VARCHAR(100),
    puchase_price MONEY,
    PRIMARY KEY (plant_id)
);

-- tracker for moisture readings
CREATE TABLE moisture_tracker (
    plant_id INTEGER,
    moisture_level INTEGER,
    reading_date DATE,
	FOREIGN KEY (plant_id)
    	REFERENCES plants (plant_id)
);
-- tracker for waterings
CREATE TABLE  water_tracker (
    plant_id INTEGER,
    water_date DATE,
    PRIMARY KEY (plant_id),
	FOREIGN KEY (plant_id)
		REFERENCES plants (plant_id)
);

-- tracker for observations like pests, general health, new leaves, etc.
CREATE TABLE  observation_tracker (
    plant_id INTEGER,
    observation_comment TEXT,
    PRIMARY KEY (plant_id),
	FOREIGN KEY (plant_id)
		REFERENCES plants (plant_id)
);

CREATE TABLE users (
    user_id SERIAL UNIQUE,
    name VARCHAR(200),
    PRIMARY KEY (user_id)
)

-- tracker for trimmed leaves
CREATE TABLE  trim_tracker (
    plant_id INTEGER,
    trimmed_date DATE,
	trimmed_quantity INTEGER,
    PRIMARY KEY (plant_id),
	FOREIGN KEY (plant_id)
		REFERENCES plants (plant_id)
);

ALTER TABLE plants ADD COLUMN user_id INTEGER;

ALTER TABLE plants ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users (user_id) MATCH FULL;

INSERT INTO users (name) VALUES ('Amanda');

-- substituted dates for timestamps
-- added event_ids to activity tables and made PK

-- updated FK to drop when plant_id is dropped
ALTER TABLE trim_tracker
DROP CONSTRAINT trim_tracker_plant_id_fkey,
ADD CONSTRAINT trim_tracker_plant_id_fkey
   FOREIGN KEY (plant_id)
   	REFERENCES plants(plant_id)
   	ON DELETE CASCADE;