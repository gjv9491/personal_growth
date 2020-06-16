--a. The names of all salespeople that have an order with Samsonic. 
select 
s."Name" as salesperson
from sales."Customers" c
left outer join sales."Orders" o
on c."Id"=o.cust_id
left outer join sales."Salesperson" s
on o.salesperson_id=s.id
where c."Name" = 'Samsonic'

--"Bob"
--"Ken"

--b. The names of all salespeople that do not have any order with Samsonic. 

select 
s."Name" as salesperson
from sales."Salesperson" s
left outer join sales."Orders" o
on o.salesperson_id = s.id
where s."Name" not in 
(
select 
s."Name" as salesperson
from sales."Customers" c
left outer join sales."Orders" o
on c."Id"=o.cust_id
left outer join sales."Salesperson" s
on o.salesperson_id=s.id
where c."Name" = 'Samsonic'
)

--"Abe"
--"Chris"
--"Dan"
--"Joe"

--c. The names of salespeople that have 2 or more orders. 

select
s."Name" as salesperson,
count(o."Number") as orders
from sales."Salesperson" s
left join sales."Orders" o
on s.id = o.salesperson_id
group by 
s."Name"
having 
count(o."Number") >= 2

--"Dan"	3
--"Bob"	2

--d. The names and ages of all salespersons must having a salary of 100,000 or greater.

select 
s."Name" as salesperson,
s."Age" as age
from
sales."Salesperson" s
where s."Salary" >= 100000

--"Abe"	61
--"Ken"	57

--e. What sales people have sold more than 1400 total units?

select 
s."Name" as salesperson,
sum(o."Amount") units
from
sales."Orders" o
left join sales."Salesperson" s
on o."salesperson_id"=s."id"
group by 
s."Name"
having sum(o."Amount") > 1400;

--"Dan"	1470
--"Bob"	2940
--"Ken"	1800

--f. When was the earliest and latest order made by dan?

select 
s."Name" as salesperson,
min(o.order_date) earliest_date,
max(o.order_date) latest_date
from 
sales."Salesperson" s
left join sales."Orders" o
on o."salesperson_id"=s."id"
where s."Name" = 'Dan'
group by
s."Name";

--"Dan"	"1998-02-03"	"1998-05-06"

