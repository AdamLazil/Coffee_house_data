
-- main tables
create table rastr (
	name varchar,
	value decimal,
	date date
);


copy rastr
from 'C:/Program Files/PostgreSQL/17/data/coffeHouse/rastrCombined.csv'
with (format csv, header, delimiter ',',encoding 'utf-8');

create table sell_sortiment (
	plu smallint,
	name varchar,
	amount decimal,
	value decimal,
	date date
);

update sell_sortiment
set plu = null
where plu = 0;


alter table sell_sortiment
add constraint FK_plu
foreign key (plu) references cash_register(plu);



copy sell_sortiment
from 'C:/Program Files/PostgreSQL/17/data/coffeHouse/combined_sortiment.csv'
with (format csv, header, delimiter ',',encoding 'utf-8');

select * from sell_sortiment;

create table cash_register (
	plu integer,
	norm varchar,
	unit varchar,
	name varchar,
	rastr_num integer,
	rastr_name varchar,
	om_num integer,
	sc decimal,
	pc decimal,
	kgl integer
);

select * from cash_register cr ;

alter table cash_register
add primary key (plu);

copy cash_register
from 'C:/Program Files/PostgreSQL/17/data/coffeHouse/cenikpokladny.csv'
with (format csv, header, delimiter ';',encoding 'win1250');


select ss.*,
	   cr.rastr_num
from sell_sortiment ss
join cash_register cr using(plu);

	
