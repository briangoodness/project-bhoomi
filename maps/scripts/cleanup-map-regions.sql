
-- run SQL statements, post-loading of region MultiPolygons into database

-- After loading all rows; run SQL statement to convert the 'geom' column back to Geometry datatype, from text/hex format
ALTER TABLE maps_region ALTER COLUMN geom TYPE Geometry(MultiPOLYGON);
SELECT UpdateGeometrySRID('maps_region', 'geom', 4326);

-- Add 'id' COLUMN
ALTER TABLE maps_region ADD COLUMN id SERIAL PRIMARY KEY;

-- For testing: add wealth indices, wealth deciles
UPDATE maps_region SET wealth_decile=95 where MOD(id, 3) = 0;
UPDATE maps_region SET wealth_decile=80 where MOD(id, 3) = 2;
UPDATE maps_region SET predicted_wealth_idx=2.2 where MOD(id, 3) = 0;
UPDATE maps_region SET predicted_wealth_idx=0.6 where MOD(id, 3) = 1;
