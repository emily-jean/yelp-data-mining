select *
from business
limit 10;

select *
from category
where category='Restaurants'
limit 10;

select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category from business
  inner join category on business.id = category.business_id
  #left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"
  and category.category = "Thai";

select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category from business
  inner join category on business.id = category.business_id
  #left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"
  and category.category = "American";

select business.id, business.name, business.neighborhood,
  business.city, business.state, catyeegory.category from business
  inner join category on business.id = category.business_id
  #left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"
  and category.category = "Middle Eastern";

select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category from business
  inner join category on business.id = category.business_id
  #left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"
  and category.category = "Chinese";

select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category from business
  inner join category on business.id = category.business_id
  #left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"
  and category.category = "Italian";


select business.id, business.name, business.neighborhood,
  business.city, business.state, category.category, attribute.value, attribute.name from business
  right join category on business.id = category.business_id
  left join attribute on category.business_id = attribute.business_id
  where business.city = "Pittsburgh"


select * from review order by review.date limit 10;


select business.id, business.name, business.neighborhood,
  business.city, business.state from business
  where business.state = "AZ";
