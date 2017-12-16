create database quantdb;


create table intStocks (symbol varchar(256), timestamp date, open float, high float, low float, close float, adjclose float, volume integer);

create table intStocksWeekly (symbol varchar(256), timestamp date, open float, high float, low float, close float, adjclose float, volume integer);


create table intStocksMonthly (symbol varchar(256), timestamp date, open float, high float, low float, close float, adjclose float, volume integer);



Load data local infile 
'C:\\sp\\python\\QuantTrading\\SLV_Weekly.csv'
into table intStocksWeekly
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="SLV";

Load data local infile 
'C:\\sp\\python\\QuantTrading\\GLD_Daily.csv'
into table intStocks
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="GLD";

Load data local infile 
'C:\\sp\\python\\QuantTrading\\PAAS_Monthly.csv'
into table intStocksMonthly
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="PAAS";


Load data local infile 
'C:\\sp\\python\\QuantTrading\\GDXJ_Monthly.csv'
into table intStocksMonthly
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="GDXJ";


Load data local infile 
'C:\\sp\\python\\QuantTrading\\GOOGL.csv'
into table intStocks
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="GOOGL";

delete from intStocks where symbol = 'AAPL';

# 'C:\\sp\\python\\QuantTrading\\AAPL.csv'


Load data local infile 
'C:\\sp\\python\\QuantTrading\\VIX.csv'
into table intStocks
fields terminated by ',' IGNORE 1 lines
(@Date,open,high,low,close,adjclose,volume)
set timestamp=STR_TO_DATE(@Date,"%Y-%m-%d"), symbol="VIX";

select * from intStocks where close = 0;
delete from intStocks where close = 0;


truncate intStocks;
select count(*) from intStocks;

select * from intStocks where timestamp < '2004-09-01';
select * from intStocks where timestamp > '2017-05-21';

select min(low) from intStocks where symbol="VIX";
select * from intStocks where symbol="VIX" and low = 8.890000343322754;

select min(timestamp) from intStocks where symbol="VIX";
select * from intStocks where symbol="VIX" and low = 8.890000343322754;















create table itDays 
(select distinct timestamp as tDay from intStocks where symbol = 'AAPL'  order by tDay asc);

alter table itDays add id int PRIMARY key AUTO_INCREMENT;

create table itradingDays 
select a.id as id, a.tDay as tDay, b.tDay as prevtDay from
(select id, tDay from itDays) a
left join 
(select id+1 as id, tDay from itDays) b
on a.id=b.id;


alter table itradingDays 
add column year int,
add column month int,
add column day int,
add column dayOfWeek int, 
add column tDaysleftMonth int,
add column tDaysleftWeek int;

alter table itradingDays 
add column weekOfYear int;

alter table itradingDays 
add column tDayinMonth int;

alter table itradingDays 
add column tDayinWeek int;

update itradingDays set year=year(tDay);

update itradingDays set month=month(tDay);

update itradingDays set day=day(tDay);

update itradingDays set dayOfWeek=weekday(tDay);

update itradingDays set weekOfYear=week(tDay);


create table imaxmintDays (select year, month, min(id) as mintDay, max(id) as maxtDay from itradingDays
group by year,month);

update itradingDays set tDaysleftMonth =(select maxtDay from 
imaxmintDays where itradingDays.year=imaxmintDays.year and itradingDays.month=imaxmintDays.month)-id;
#(select quantity from table_1 where locationid=1 and table_1.itemid = table_2.itemid)

update itradingDays set tDayinMonth = id+1-(select mintDay from 
imaxmintDays where itradingDays.year=imaxmintDays.year
 and itradingDays.month=imaxmintDays.month);

create table itWeeks (select year, weekOfYear, min(id) as mintDay,
max(id) as maxtDay from itradingDays
 group by year,weekOfYear) ;

update itradingDays set tDaysleftWeek =  (select maxtDay from 
itWeeks where itradingDays.year=itWeeks.year and itradingDays.weekOfYear=itWeeks.weekOfYear)-id;


update itradingDays set tDayinWeek = id+1-(select mintDay from 
itWeeks where itradingDays.year=itWeeks.year and 
itradingDays.weekOfYear=
itWeeks.weekOfYear);



SELECT * FROM quantdb.intstocks;

select 	c.timestamp, t.id, c.adjclose, t.month, t.day, t.dayOfWeek,
		t.tDaysLeftMonth, t.tDayinMonth, t.tDayinWeek 
from 	intstocks c left join itradingdays t on 
		c.timestamp=t.tDay
where 	c.symbol='GOOGL' and 
		c.timestamp < '2017-05-22' and
		t.id >= (select min(id) from itradingdays where tDay >= '2017-05-01') - 300
order by timestamp desc;
