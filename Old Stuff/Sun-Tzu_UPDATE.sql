-- QUESTION 5) UPDATE statements file:
-- Sun-Tzu team.

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
