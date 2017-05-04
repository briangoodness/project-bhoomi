
-- run SQL statements, post-loading of region MultiPolygons into database

-- After loading all rows; run SQL statement to convert the 'geom' column back to Geometry datatype, from text/hex format
ALTER TABLE maps_cell_prediction ALTER COLUMN geom TYPE Geometry(POLYGON);
SELECT UpdateGeometrySRID('maps_cell_prediction', 'geom', 4326);

-- Add 'id' COLUMN
ALTER TABLE maps_cell_prediction ADD COLUMN id SERIAL PRIMARY KEY;

-- For testing: add wealth indices
UPDATE maps_cell_prediction SET predicted_wealth_idx=2.2 where MOD(id, 3) = 0;
UPDATE maps_cell_prediction SET predicted_wealth_idx=0.6 where MOD(id, 3) = 1;
