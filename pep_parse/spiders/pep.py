import scrapy
from lxml import etree


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        section_table = response.xpath('//section[@id="numerical-index"]')
        pep_table = section_table.xpath('table/tbody/tr')
        for pep in pep_table:
            pep_link = pep.xpath('td/a/@href')[0].get()
            yield response.follow(
                pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep_heading = response.xpath('//section[@id="pep-content"]')
        status_string = pep_heading.xpath('dl/dt[contains(text(),"Status")]')
        name_element = pep_heading.xpath('h1').get()
        parser = etree.HTMLParser()  # Для 499 PEP
        tree = etree.fromstring(name_element, parser)
        data = {
            'name': etree.tostring(tree, encoding='unicode', method='text'),
            'status': status_string.xpath(
                'following-sibling::dd/abbr/text()').get().strip(),
        }
        return data
