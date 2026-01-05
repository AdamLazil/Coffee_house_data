-- analyze 

select * from rastr r ;
select * from sell_sortiment ss ;
select * from cash_register cr ;

select date,
	   sum(value),
	   to_char(date, 'day') as weekDay
from sell_sortiment ss 
group by date
order by date desc;