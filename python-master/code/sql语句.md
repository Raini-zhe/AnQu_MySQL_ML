开发中使用的sql 语句（已经过验证）

#选择词库中的词，按照priority ,searchCount 排序，并显示前100记录
select * from wordSelectFeature order by priority desc , searchCount desc group by cluster limit 100;

select * from wordSelectFeature where searchCount < 5000 order by priority desc , searchCount desc limit 100;

<!-- select * from wordSelectFeature where word like '陌陌'; -->
select * from wordSelectFeature where group by cluster order by priority desc , searchCount desc limit 100;

select word from wordSelectFeature where group  

#创建SOM分析结果表
create table SOMwordSelectFeature (word varchar(255),priority int,searchCount int,relevancy float,cluster int);

#竞品ID样例
'443354861','799406905','457517348','453640300','615187629','471802217','521922264','389801252','847334708','592331499','606080169','611129419','825355393','608188610','933456837','599534650'
