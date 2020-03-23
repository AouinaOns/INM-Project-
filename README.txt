%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Description des bases de données %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

A noter :
- les textes étudiés sont en anglais et extraits de pubmed.
- le thème d'étude est le cancer chez les humains.
- la clé de jointure pour les tables avec les articles est le pmid.
- Attention, les tables sur les articles n'ont pas le même nombre de lignes car la validation manuelle n'a pas été effectuée sur l'ensemble des articles.
- INM signifie interventions non-médicamenteuses (comme par exemple, activité physique, phytohtérapie, aromathérapie, hypnose...)
en anglais cela devient Non-pharamceutical interventions soit NPI, que vous retouverez dans les bases de données.
- DOI : Digital Object Identifier, un identifiant unique attribué à une étude. La consultation des documents est possible en ajoutant le DOI à l'adresse 
de base https://doi.org. exemple avec le doi 10.7326/L17-0394 : https://doi.org/10.7326/L17-0394.
- MESH : MEdical Subject Heading. Mot clé standardisé de manière internationnale ayant attrait aux problématiques médicales.

%%% Table list_mesh_npi %%%
Cette table est issue d'un premier rescencement des inm sur le site pubmed, mais aussi sur d'autres sources tels que l'HAS (haute Autorité de santé), elle contient les données suivantes :
- Mesh_Expression : inm (ou npi en anglais), retraitement avec suppression des traits d'unions et accollement des chiffres avec lettres s'il y a lieu (exemple vitamin B 6 devient vitamin B6);
- SubCategory : sous-catégorie de l'inm;
- Category : catégorie de l'inm (interventions : physiques, nutritionnelles, psychologiques, numériques ou autres).

%%% Fichier json Cancer_Studies.json %%%
Ce fichier est à la date de ernière mise à jour soit le 10 mars 2020.
Il est issu de l'extraction des données xml de PubMed, il contient:
- la clé du dictionnaire est le pmid, puis pour chaque article (il y a le doi, les citations, le titre, le nom du journal, la date de publication,  le résumé, les mots clés, 
les mots mesh, les substances, le type d'étude, les infos sur les auteurs et une variable issue du premier modèle de classification qui est mise à -1)

%%% Table KC_cleaned_160320 %%%
Attention, le séparateur est la virgule.
Cette table contient l'ensemble des articles extraits de pubmed à daté du 10 mars 2020.
Elle est le résultat de prétraitements (réalisés avec Python) sur les données PubMed, elle contient les données suivantes :
- pmid : numéro identifiant de l'article propre à pubmed;
- journalname : nom du journal de publication de l'article;
- text : concaténation du titre, de l'abstract, des mots clés et mesh et des noms de substances. 
Les pré-traitements effectués sont les suivants : suppression des url et des marques html; suppression des caractères et numéros de copyrights et d'essai clinique; suppression de la ponctuation et 
des traits d'union, des nombres, des caractères spéciaux et symboles, mise en miniscule; suppression des espaces inutiles; suppression des mots creux (stopwords), 
des 123 mots les plus fréquents du corpus et de certaines unités de mesures.

%%% Table yesno_valid %%%
Attention, le séparateur est le point-virgule.
Cette table est le résultat de validation manuelle par des experts (attention la validation a été réalisée essentiellement sur l'année 2019), elle contient les données suivantes :
- response : oui (codé 1) l'article parle d'inm et non (codé en 2) sinon;
- pmid : numéro identifiant de l'article propre à pubmed.

%%% Table ManualAnnotations %%%
Cette table est le résultat d'extraction de données PubMed et d'annotations des résumés par des experts sur les questions du bénéfice et du risque d'une INM, elle contient les données suivantes :
- pmid : numéro identifiant de l'article propre à pubmed;
- doi : identifiant de l'article universel;
- title : titre de l'article;
- pubdate : date de publication;
- mentionednpi : quelle est l'inm étudiée (s'il y a lieu);
- participant : type de participants (healthy: personnes saines, patients : personnes malades);
- ages : classes d'ages (enfants, adultes, personnes agées);
- genders : sexe de la population étudiée;
- designs : type d'étude (monocentrique, multicentrique, essai clinique...);
- outcomes : type de résultats (psychologie, biologie, étude de coûts...);
- benefit : qualification du bénéfice de l'inm (Ambigu, Aucun, Nul, Léger, Significatif);
- risk : qualification du risque de l'inm (Ambigu, Aucun, Possible, Nul, Léger, Significatif);
- cancer : type de cancer;
- mt_last_modified : date de dernière modification de l'enregistrement.




