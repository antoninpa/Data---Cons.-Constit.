#!/usr/bin/python2.7
# encoding: utf-8

import re
import csv

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, TextResponse, Response
from scrapy.selector import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ConsCscrap.items import listCCitem

class CCspider(CrawlSpider):
    name = 'listCC'
    handle_httpstatus_list = [404, 301]
    
    # Page du Cons. Constit. qui renvoie, pour chaque année, à toutes les décisions prises
    start_urls = ['http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/les-decisions-par-date.4614.html']
    
    rules = (Rule(LxmlLinkExtractor(allow=(), restrict_xpaths="//div[@id='articlesArchives']"),
                  callback="parse_annee", follow=True),)
    
    def parse_annee(self, response):
        
        decisions = response.selector.xpath("//li[@class='ld']")

        for el in decisions:
            item = listCCitem()
            
            # Pas très élégant, mais cela me permet de régler les problèmes d'encodage
            item['dd'] = "".join(map(unicode.strip, el.xpath("./a/text()").extract())).split()[0]

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

            # On récupère les données sur la page /année/ et on continue sur la page /décision/
            yield Request(item['link_dc'], meta={'item':item}, callback=self.parse_decision)



    def parse_decision(self, response):
        decision = response.selector.xpath("//div[@id='mainContent']")
        for el in decision:
            item = response.request.meta['item']
            item['ecli_dc'] = "".join(map(unicode.strip, el.xpath("./div[@id='ecli']/text()").extract()))

            # Pour recenser les membres qui ont pris une décision on utilise le regex : 
            reg = "(Georges VEDEL|Louis JOXE|Robert LECOURT|Francis MOLLET-VI\xc9VILLE|L\xe9on JOZEAU-MARIGN\xc9|Daniel MAYER|Robert FABRE|Robert BADINTER|Jacques LATSCHA|Maurice FAURE|Jean CABANNES|Noelle Lenoir|Jacques ROBERT|Georges ABADIE|Marcel RUDLOFF|No\xeblle LENOIR|Roland DUMAS|Val\xe9ry GISCARD d'ESTAING|Etienne Dailly|Michel AMELLER|Alain LANCELOT|Yves GU\xc9NA|Pierre MAZEAUD|Simone VEIL|Jean-Claude COLLIARD|Monique PELLETIER|Olivier DUTHEILLET de LAMOTHE|Dominique SCHNAPPER|Pierre JOXE|Jean-Louis PEZANT|Jacqueline de GUILLENCHMIDT|Pierre STEINMETZ|Jacques BARROT|Hubert HAENEL|Jean-Louis DEBR\xc9|Guy CANIVET|Renaud DENOIX de SAINT MARC|Jacques CHIRAC|Michel CHARASSE|Claire BAZY MALAURIE|Nicolas SARKOZY|Nicole MAESTRACCI|Nicole BELLOUBET|Lionel JOSPIN|Jean-Jacques HYEST|Laurent FABIUS|Corinne LUQUIENS|Michel PINAULT)"
            pres_dc = u"".join(map(unicode.strip, el.xpath("./a[@id='information_seance']/following-sibling::p/text()").extract()))
            item['membres'] = re.findall(str(reg), pres_dc)

            yield item
