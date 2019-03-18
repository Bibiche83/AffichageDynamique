#  PROJET AffichageDynamique

Projet BTS Affichage Dynamique en Python

Adrien : Etudiant en BTS SN IR 

Langage utilisé : PYTHON

# PRESENTATION 

L'objectif de ce projet est de permettre l'affichage d'informations pertinentes pour les élèves de l'établissement, sur des moniteurs placés dans des bâtiments différents d'un lycée. 

Les informations habituelles peuvent concerner par exemple : 
•	 Les absences des professeurs
•	 Les modifications d’emplois du temps 
•	Les événements divers concernant l'établissement (sécurité, portes ouvertes …) 
•	Les menus cantine, etc.

Le type d'informations affichées (types texte, images ou vidéos), outre les exemples décris ci-dessus, pourra être défini par un sondage réalisé auprès des élèves de l'établissement, au tout début du projet.  

L'affichage dans le lycée se fera sur plusieurs moniteurs identiques, placés dans des sites différents, reliés sur le même réseau d’établissement. 

L'affichage en interne, sur les moniteurs, sera de type défilant. 
L'administrateur pourra saisir les informations à afficher, décider de leur durée et ordre d'affichage, et des plage horaires d'utilisation.  

La mise à jour et la saisie d'informations seront effectuées par le personnel de l'établissement, disposant de l'autorisation de le faire.
 Cette tâche ne devra pas nécessiter de compétences approfondies en informatique, la saisie se fera au moyen d'une interface la plus simple possible.  
 
Les applications ne devront être réalisées qu'avec des composants logiciels gratuits ou disponibles au lycée, et sera installée sur un PC standard fonctionnant sous Windows. L'ensemble sera conçu comme une architecture trois tiers.  
Chaque écran, disposant d'une entrée HDMI, sera piloté par soit par un micro-ordinateur Raspberry, soit par un mini-PC Zotac, reliés au réseau de l'établissement. 


# Ce qui est demandé à l'étudiant 

Pour chaque étudiant, il est demandé : 
•	 Analyse du projet : diagrammes SysML et UML nécessaires à la description fonctionnelle du projet : les candidats devront fournir au moins les diagrammes UML suivants : diagrammes de classes, diagrammes de déploiement, diagrammes de séquences. 

•	Conception globale et détaillée : diagrammes SysML et UML nécessaires à la description de la conception. 

•	 Exigences de qualités : 
-	Adaptabilité : la modification doit être aisée • Maniabilité : l'effort nécessaire pour l'apprentissage et la mise en œuvre doit être minime 
-	 Sécurité : protéger et contrôler l'accès au code et aux données 
-	Robustesse : accomplir sans défaillance l'ensemble des fonctionnalités spécifiées 
-	Testabilité : faciliter les procédures de test permettant de s'assurer de l'adéquation des fonctionnalités

# CONCEPTION D'UNE IHM EN PYTHON 

Conception d’une application sur PC permettant la saisie des informations à afficher et l'enregistrement d'un scénario. Le langage utilisé sera Python l’environnement de développement est laissé au choix de l’étudiant, mais devra être gratuit. 

Chaque ensemble d'informations constitue un scénario, qui sera enregistré sur le serveur au format XML. Il sera prévu un scénario par défaut. Un scénario sera déclaré actif, pour être affiché.  

Les informations affichées sur l'écran seront soit : 
•	Des images au format JPEG *
•	 Des vidéos, aux formats pouvant être lus avec VLC sur le Raspberry et mini-PC Zotac 
•	 Du texte au format PDF. 
 
L’application devra permettre de définir un fichier scénario, comprenant au moins : 
•	 L’écran concerné, afin de différencier les affichages si besoin
•	 L’emplacement réseau du fichier à afficher • La durée d’affichage, pour chaque fichier 
•	La plage horaire d’affichage 

 Les scénarios devront pouvoir être visualisés, enregistrés, supprimés et édités. Il est impératif que le format choisi pour la définition des scénarios (fichier XML) choisi soit commun pour tous les étudiants. Les fichiers scénarios seront enregistrés sur le réseau. 
 
L’application devra permettre l’affichage immédiat d’un scénario. 
 
 

 



