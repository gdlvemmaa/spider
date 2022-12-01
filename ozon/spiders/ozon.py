import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..items import OzonItem
from ..settings import TIMEOUT_SEC


class OzonSpider(scrapy.Spider):
    name = 'ozon'
    allowed_domains = ['www.ozon.ru']
    main_url = 'https://www.ozon.ru'
    first_page = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating&type=49659'
    itm_cnt = 0
    __xpath_query = {
        'pagination': '//div[@class="an0a"//div[@class="aam9 _4-a"]/a',
        'item_links': '//div[contains(@class, "s4k")]//a[contains(@class, "tile-hover-target")]/@href',
        'prop_labels': '//div[@id="section-characteristics"]//div[@class="ly6"]//div[@class="y81"]/span[@class="l9y"]'
                       '/text()',
        'prop_values': '//div[@id="section-characteristics"]//div[@class="ly6"]//div[@class="ly9"]',
        'name': '//h1[@class="w8n"]/text()'
    }

    def start_requests(self):
        yield SeleniumRequest(url=self.first_page,
                              callback=self.parse,
                              wait_time=TIMEOUT_SEC,
                              wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, "footer[class='zc0']"))
                              )

    def parse(self, response, **kwargs):
        while True:
            item_links = response \
                .xpath(self.__xpath_query['item_links']).extract()

            for link in item_links:
                yield SeleniumRequest(url=self.main_url + link,
                                      callback=self.item_parse,
                                      wait_time=TIMEOUT_SEC,
                                      wait_until=EC.presence_of_element_located(
                                          (By.CSS_SELECTOR, "footer[class='zc0']"))
                                      )
                self.itm_cnt += 1
                if self.itm_cnt == 100:
                    break
            try:
                next_page = response.xpath(self.__xpath_query['pagination']).click()
                yield SeleniumRequest(url=self.main_url + next_page,
                                      callback=self.parse,
                                      wait_time=TIMEOUT_SEC,
                                      wait_until=EC.presence_of_element_located(
                                          (By.CSS_SELECTOR, "footer[class='zc0']"))
                                      )
            except Exception:
                break

    def item_parse(self, response):
        item_properties = {}
        property_values = []

        property_labels = response \
            .xpath(self.__xpath_query['prop_labels']).extract()

        property_value_selectors = response \
            .xpath(self.__xpath_query['prop_values'])

        for selector in property_value_selectors:
            text = selector.xpath('/text()').extract()
            if text:
                property_values.append(text)
            else:
                property_values.append(selector.xpath('/a/text()').extract())

        item_properties.update(dict(zip(property_labels, property_values)))

        item_properties['name'] = response.xpath(self.__xpath_query['name']).extract()

        if item_properties.get('Версия Android'):
            item_properties['os_version'] = item_properties.get('Версия Android')
        else:
            item_properties['os_version'] = item_properties.get('Версия iOS')

        yield OzonItem(
            name=item_properties['name'],
            os_version=item_properties['os_version']
        )