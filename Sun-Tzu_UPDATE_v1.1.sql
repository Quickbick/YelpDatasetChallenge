-- QUESTION 5) UPDATE statements file:
-- Sun-Tzu team.

-- Maybe this should go at the top actually..?
-- DROP TABLE IF EXISTS BusinessAggregates;

-- Create a temporary table to store aggregated data
CREATE TEMP TABLE BusinessAggregates AS
SELECT
    b.id AS BusinessID,
    COALESCE(SUM(c.count), 0) AS numCheckins,
    COUNT(r.id) AS reviewCount,
    -- OLD UNROUNDED: COALESCE(AVG(r.star_rating), 0) AS reviewrating
    COALESCE(ROUND(AVG(r.star_rating), 1), 0) AS reviewrating -- Now, I'm trying to round to 1 decimal places like they did in the example photos.
FROM
    Business b
LEFT JOIN Checkins c ON b.id = c.business
LEFT JOIN Rating ra ON b.id = ra.business
LEFT JOIN Reviews r ON ra.review = r.id
GROUP BY
    b.id;

-- Update the Business table with aggregated data
UPDATE Business
SET
    num_checkins = bagg.numCheckins,
    num_reviews = bagg.reviewCount,
    review_rating = bagg.reviewrating
FROM
    BusinessAggregates bagg
WHERE
    Business.id = bagg.BusinessID;

-- Drop the temporary table
DROP TABLE IF EXISTS BusinessAggregates;








-- OLD, didn't work my bad:
/*

UPDATE Business -- Calculate + Update num_checkins attribute for each business:
SET num_checkins = (
    SELECT SUM(count) 
    FROM Checkins
    WHERE Checkins.business = Business.id
);

UPDATE Business -- Calculate + Update num_reviews attribute for each business:
SET num_reviews = (
    SELECT COUNT(*) 
    FROM Reviews
    WHERE Reviews.id = Business.id
),
review_rating = ( -- Calculate + Update review_rating attribute for each business:
    SELECT AVG(star_rating)
    FROM Reviews
    WHERE Reviews.id = Business.id
);

*/