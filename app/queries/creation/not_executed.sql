-- plant data sourced from the web
-- include general plant info
-- include watering schedule
-- include fertilization schedule
-- include other important info
CREATE TABLE plant_data (

);

-- tracker for fertilization
CREATE TABLE  fertilization_tracker (
    plant_id REFERENCES plants(plant_id),
    fertilized_date DATE,
    fertilizer_type VARCHAR(100)

    PRIMARY KEY (plant_id)
);

-- tracker for cleaning leaves
CREATE TABLE  clean_tracker (
    plant_id REFERENCES plants(plant_id),
    cleaned_date DATE,
    PRIMARY KEY (plant_id)
);

-- tracker for spraying neem oil
CREATE TABLE  neem_oil_tracker (
    plant_id REFERENCES plants(plant_id),
    neem_oil_date DATE
    PRIMARY KEY (plant_id)
);

-- tracker for re-potting
-- TODO: how to update here and main tracker? want to log pot size with new plant but also update
CREATE TABLE  pot (
    plant_id REFERENCES plants(plant_id),
    pot_date DATE,
    pot_size NUMERIC (4, 2) REFERENCES plants(pot_size)
    PRIMARY KEY (plant_id)
);
