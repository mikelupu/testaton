
--TEST
--INDEX=['market_id']
--MEASUREMENTS=['percentage']
select market_id, makret_name, percentage 
from betfair_market
where sysdate = '123'




--TEST
--COMMENT=Second Test
select sysdate from dual

