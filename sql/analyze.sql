-- analyze 

select * from rastr r ;
select * from sell_sortiment ss ;
select * from cash_register cr ;


create view time_income as (
select date,
	   sum(value) as income,
	   to_char(date, 'day') as weekDay
from sell_sortiment ss 
group by date
order by date desc);

drop view time_income;

select * from time_income;
	 
-- according weekday
with cte as (
select
     sum(income) as income,
     extract(ISODOW from ti.date) as numday,
     weekday
from time_income ti
group by weekday, extract(ISODOW from ti.date)
)
select
	 income,
	 numday,
	 weekday
from cte
order by numday;

;
     