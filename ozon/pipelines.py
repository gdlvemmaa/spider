# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface


class OzonPipeline:
    def process_item(self, item, spider):
        with open('data/parsed_data.csv', 'a') as file:
            file.write(f'{item["name"]};{item["os_version"]}\n')

        return item
