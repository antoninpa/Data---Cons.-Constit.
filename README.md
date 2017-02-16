Conseil Constitutionnel
=============================

Copyright (c) 2017 Antonin Paillet

**License**: [Creative Commons Attribution 4.0 International (CC BY-NC-SA 4.0)]
(https://creativecommons.org/licenses/by-nc-sa/4.0/).  

Les seules données statistiques sur le Conseil Constitutionnel sont publiées dans les [Nouveaux Cahiers du Conseil Constitutionnel] 
(http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/nouveaux-cahiers-du-conseil/les-nouveaux-cahiers-du-conseil-constitutionnel.5069.html),
dont la lecture est payante. Par curiosité autant que par jeu j'ai donc décidé de collecter les données et de voir s'il est possible d'en tirer quelques enseignements. 

Il y a trois dossiers : 
* */scraping* : pour récupérer les données sur le site du CC
* */data* : pour produire quelques statistiques avec les données;
* */PDFcrawl* : en bonus, pour récupérer toutes les décisions en .pdf dans un seul dossier

## /scraping

Pour récupérer les données j'utilise le framework python [Scrapy] (https://scrapy.org/).

À partir d'une page du CC, les décisions sont classées de la manière suivante : */liste_des_années/décisions_par_année/décision/*. 
Pour récupérer toutes les données pertinentes, les requêtes sont faites sur les 3 niveaux (avec une conservation des données entre le niveau 2 et 3).

