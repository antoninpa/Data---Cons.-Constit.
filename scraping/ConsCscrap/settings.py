# Scrapy settings for bsJP project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'ConsConstit'

SPIDER_MODULES = ['ConsCscrap.spiders']
NEWSPIDER_MODULE = 'ConsCscrap.spiders'
#FILES_STORE = '/home/antonin/Bureau/ConsCscrap/LeConsConstit'
#ITEM_PIPELINES = {'ConsCscrap.pipelines.MyPDFpipelines': 1}   # Ce pipeline permet de transmettre le titre du doc
#ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
#DOWNLOAD_DELAY = 1
