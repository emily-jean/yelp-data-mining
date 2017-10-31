
-- get count of restaurants by state
SELECT business.state,
  COUNT(*) AS "Number of Restaurants per State"
  FROM business
  INNER JOIN category on business.id = category.business_id
  WHERE category.category = "Restaurants"
  GROUP BY business.state;


-- get count of restraurants by city
SELECT business.state, business.city,
  COUNT(*) AS "Number of Restaurants per City"
  FROM business
  INNER JOIN category on business.id = category.business_id
  WHERE category.category = "Restaurants"
  GROUP BY business.state, business.city;


--  all of the restaurants in Pittsburgh (2089)
select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category
  from business
  inner join category on business.id = category.business_id
  where business.city = "Pittsburgh"
  and category.category = "Restaurants"
  GROUP BY business.id, category.category
  ORDER BY business.name;

-- gets all Italian restuarants in Pittsburgh
select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category from business
  inner join category on business.id = category.business_id
  where business.city = "Pittsburgh"
  and category.category = "Italian";
-- Other categories: Chinese, Middle Easter, American, Thai, American (new)


-- query to get all categories for a restaurant (i.e. Restaurants, Mexican)
select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category
  from business
  inner join category on business.id = category.business_id
  where business.id = "-AtzcXIwEP6yO7rM9CM9ww"
  GROUP BY business.id, category.category
  ORDER BY category.category;

-- top 50 most reviews restaurants
select business.id, business.name, business.city, business.state, business.review_count, business.stars
  from business
  inner join category on business.id = category.business_id
  where category.category = "Restaurants"
  order by business.review_count desc
  limit 50;

-- get all of the restaurants in Pittsburgh
select business.id, business.name, business.neighborhood, business.latitude, business.longitude, business.review_count
  from business
  inner join category on business.id = category.business_id
  where business.city = 'Pittsburgh'
  and category.category = 'Restaurants'
  group by business.id
  order by business.neighborhood ASC;

-- count the # of Pittsburgh restaurants by neighborhood
select business.neighborhood,
  COUNT(*) AS 'Restaurants by Neighborhood'
  from business
  inner join category on business.id = category.business_id
  where business.city = 'Pittsburgh'
  and category.category = 'Restaurants'
  group by business.neighborhood
  order by COUNT(*) DESC;

select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category, attribute.value, attribute.name from business
  right join category on business.id = category.business_id
  left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"


select * from review order by review.date limit 10;

