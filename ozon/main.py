from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings
from spiders.ozon import OzonSpider
import pandas as pd

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(OzonSpider)
    crawl_proc.start()

    # processing parsed data
    columns = ['name', 'os_version']
    df = pd.read_csv('../data/parsed_data.csv', header=None, names=columns,
                     sep=';')
    result_df = df.groupby('os_version')['name'].aggregate(
        ['count']).sort_values("count", ascending=False)
    result_df.to_csv('../data/processed_data.txt', encoding='utf-8', sep='-',
                     header=False)
