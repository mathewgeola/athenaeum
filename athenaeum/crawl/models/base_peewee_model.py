from peewee import CharField, DateTimeField, DecimalField, SmallIntegerField
from athenaeum.crawl.models.base_data_peewee_model import BaseDataPeeweeModel


class BasePeeweeModel(BaseDataPeeweeModel):
    spider_name = CharField(index=True, null=True, verbose_name='爬虫名称')
    spider_source = CharField(null=True, verbose_name='爬虫来源')
    spider_url = CharField(max_length=2048, null=True, verbose_name='爬虫链接')
    spider_start_datetime = DateTimeField(null=True, verbose_name='爬虫开始日期时间')
    spider_limit_interval = DecimalField(decimal_places=2, null=True, verbose_name='爬虫限制间隔时间')
    spider_run_interval = DecimalField(decimal_places=2, null=True, verbose_name='爬虫运行间隔时间')
    spider_status = SmallIntegerField(index=True, null=True, verbose_name='爬虫状态')
