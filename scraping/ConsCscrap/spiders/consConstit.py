#!/usr/bin/python2.7
# encoding: utf-8

import re
import csv
#from scrapy.spiders import BaseSpider, CrawlSpider, Rule, Spider
from scrapy.spiders import CrawlSpider, Rule

#from scrapy.loader import ItemLoader
from scrapy.http import Request, TextResponse, Response
#from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.selector import Selector

#from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ConsCscrap.items import listCCitem

class CCspider(CrawlSpider):
    name = 'listCC'
    handle_httpstatus_list = [404, 301]
    start_urls = ['http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/les-decisions-par-date.4614.html']
    #start_urls = ['http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/2015/sommaire-2015.142956.html']

    
    rules = (Rule(LxmlLinkExtractor(allow=(), restrict_xpaths="//div[@id='articlesArchives']"),
                  callback="parse_dc", follow=True),)
    
    def parse_dc(self, response):
        print("In Parse_DC")
        sel = Selector(response)
        decision = response.selector.xpath("//li[@class='ld']")
        items = []
        for el in decision:
            item = listCCitem()
            item['dd'] = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[0]
            #item['mm'] = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[1]
            
            mois = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[1]

            if mois == 'janvier':
                item['mm'] = '01'
            elif mois == u'février': 
                item['mm'] = '02'
            elif mois == 'mars':
                item['mm'] = '03'
            elif mois == 'avril':
                item['mm'] = '04'
            elif mois == 'mai':
                item['mm'] = '05'
            elif mois == 'juin':
                item['mm'] = '06'
            elif mois == 'juillet':
                item['mm'] = '07'
            elif mois == u'août':
                item['mm'] = '08'
            elif mois == 'septembre':
                item['mm'] = '09'
            elif mois == 'octobre':
                item['mm'] = '10'
            elif mois == 'novembre':
                item['mm'] = '11'
            elif mois == u'décembre':
                item['mm'] = '12'
            else:
                item['mm'] = mois

            item['yy'] = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[2]
            item['num_dc'] = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[6]
            
            type_dc = "".join(map(unicode.strip, el.xpath("./a/text()").extract()))
            item['type_dc'] = "".join(map(str, re.findall('\w*$', type_dc)))
                                    
            objet = "".join(map(unicode.strip, el.xpath("./em/text()").extract()))
            item["objet_dc"] = " ".join(objet.split())
            
            
            sol_dc = "".join(map(unicode.strip, el.xpath("./em/small/text()").extract()))
            item["sol_dc"] = "".join(map(str, re.findall('[^\[].*(?<!\])', sol_dc.encode('utf-8'))))
            
            item["publi_dc"] = "".join(map(unicode.strip, el.xpath("./em/em/text()").extract()))

            item['link_dc'] = "http://www.conseil-constitutionnel.fr"+"".join(map(unicode.strip, el.xpath("./a/@href").extract()))


            #http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/2007/2007-108-orga/decision-n-2007-108-orga-du-13-juin-2007.108012.html
            #http://wwww.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/2007/2007-107-orga/decision-n-2007-107-orga-du-25-janvier-2007.108075.html'

            #yield item
            yield Request(item['link_dc'], meta={'item':item}, callback=self.dc_parse)
            #items.append(item)
        #return items
            

    def dc_parse(self, response):
        sel = Selector(response)
        decision = response.selector.xpath("//div[@id='mainContent']")
        items = []
        for el in decision:
            item = response.request.meta['item']
            item['ecli_dc'] = "".join(map(unicode.strip, el.xpath("./div[@id='ecli']/text()").extract()))

            reg = "(Georges VEDEL|Louis JOXE|Robert LECOURT|Francis MOLLET-VI\xc9VILLE|L\xe9on JOZEAU-MARIGN\xc9|Daniel MAYER|Robert FABRE|Robert BADINTER|Jacques LATSCHA|Maurice FAURE|Jean CABANNES|Noelle Lenoir|Jacques ROBERT|Georges ABADIE|Marcel RUDLOFF|No\xeblle LENOIR|Roland DUMAS|Val\xe9ry GISCARD d'ESTAING|Etienne Dailly|Michel AMELLER|Alain LANCELOT|Yves GU\xc9NA|Pierre MAZEAUD|Simone VEIL|Jean-Claude COLLIARD|Monique PELLETIER|Olivier DUTHEILLET de LAMOTHE|Dominique SCHNAPPER|Pierre JOXE|Jean-Louis PEZANT|Jacqueline de GUILLENCHMIDT|Pierre STEINMETZ|Jacques BARROT|Hubert HAENEL|Jean-Louis DEBR\xc9|Guy CANIVET|Renaud DENOIX de SAINT MARC|Jacques CHIRAC|Michel CHARASSE|Claire BAZY MALAURIE|Nicolas SARKOZY|Nicole MAESTRACCI|Nicole BELLOUBET|Lionel JOSPIN|Jean-Jacques HYEST|Laurent FABIUS|Corinne LUQUIENS|Michel PINAULT)"

            pres_dc = u"".join(map(unicode.strip, el.xpath("./a[@id='information_seance']/following-sibling::p/text()").extract()))
            item['membres'] = re.findall(str(reg), pres_dc)

            yield item



"""
class DCspider(Spider):

    name = 'pdfCC'
    handle_httpstatus_list = [404, 301]
    start_urls = ["http://www.conseil-constitutionnel.fr"]

    def parse(self, response):
        YEAR = "2014"
        TYPE = ['dc', 'qpc']
        mesTypes = ['DC', 'QPC']
        with open('/home/antonin/Bureau/ConsCscrap/ConsCscrap/spiders/listCC.csv') as csvfile:
            reader = csv. DictReader(csvfile)
            mesURL = []
            item = ConsContItem()
            for row in reader:
                try:
                    if int(row['yy']) > 2012:
                        if row['type_dc'] in mesTypes:
                            #mesURL.append("http://www.conseil-constitutionnel.fr/conseil-constitutionnel/root/bank/download/"+str(row['num_dc']).replace('-','')+str(row['type_dc'])+str(row['num_dc']).replace('-', '')+str(row['type_dc']).lower()+".pdf")
                            item['file_urls'] = ["http://www.conseil-constitutionnel.fr/conseil-constitutionnel/root/bank/download/"+str(row['num_dc']).replace('-','')+str(row['type_dc'])+str(row['num_dc']).replace('-', '')+str(row['type_dc']).lower()+".pdf"]
                            item['text'] = str(row['dd'])+str(row['mm'])+str(row['yy'])+str(row['num_dc'])

                            #item['file_urls'].append("http://www.conseil-constitutionnel.fr/conseil-constitutionnel/root/bank/download/"+str(row['num_dc']).replace('-','')+str(row['type_dc'])+str(row['num_dc']).replace('-', '')+str(row['type_dc']).lower()+".pdf")
                            yield item
                        else:
                            pass
                    else:
                        pass
                except ValueError:
                    pass

        yield ConsContItem(
            file_urls=mesURL
            )


        for n in range(400, 442):
            for el in TYPE:
                item = ConsContItem()
                items = []
                item['file_urls'] = mesURL
                #item['file_urls'] = ["http://www.conseil-constitutionnel.fr/conseil-constitutionnel/root/bank/download/"+YEAR+"%d" %(n)+el.upper()+YEAR+"%d" %(n)+el+".pdf"]
                #numeroDC = "".join(map(str, re.findall('(?<=download/2014)(\d{1,4})', str(item['file_urls']))))
                #typeDC = "".join(map(str, re.findall('(DC|QPC)', str(item['file_urls']))))
                #item['text'] = YEAR+"-"+numeroDC+" "+typeDC
                yield item



    Quelques indications pour la recherche :
    - 2015 : DC (710-728) ; QPC (-522) ; L(252) ; ORGA (133-



     # Une manière de faire rapide pour récupérer le document depuis l'url...
    def parse(self, response):
        yield ConsContItem(
            file_urls=["http://www.conseil-constitutionnel.fr/conseil-constitutionnel/root/bank/download/2005%dDC2005%ddc.pdf" %(n, n) for n in range(500, 542)]
            )
"""
