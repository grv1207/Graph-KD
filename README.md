# Graph-KD: Exploring Relational Information for Knowledge Discovery.  
**Roland Roller, Gaurav Vashisth, Philippe Thomas, He Wang, Michael Mikhailov and Mark Stevenson**
[To appear] Proceedings of the International Semantic Web Conference 2019.



Graph-KD is a general graph exploring tool, which has following functionalities:
1. Finding K-shortest path between two nodes.
2. Exploring paths around a given node.
3. Infering relations between source and target node of a given path.



The knowledge-graph that is used to build this tool is the **UMLS (Unified Medical Language System) dataset** which is freely available at [UMLS website](https://uts.nlm.nih.gov/home.html)

In order to use Graph-Kb you should have:
* Neo4j 
* JVM
* Python 3.x

The following tutorial supports only **Unix-Systems**

## I) [ Neo4j-Setup ]:
----------------------

### 1.1) Neo4j 3.2 requires the Java 8 runtime. To install java 8 on ubuntu 16.04:
* `echo "deb http://httpredir.debian.org/debian jessie-backports main" | sudo tee -a /etc/apt/sources.list.d/jessie-backports.list`
* `sudo apt-get update`
* `sudo add-apt-repository ppa:webupd8team/java`
* `sudo apt-get update`
* `sudo apt-get install oracle-java8-installer`


### 1.2) Add the Neo4j repository: 
* `wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -`
* `echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list`
* `sudo apt-get update`

### 1.3) Installing Neo4j:
* `sudo apt-get install neo4j=3.2.2`

### 1.4) Check Neo4j installation:
* `systemctl start neo4j` to start Neo4j.
* `systemctl status neo4j` to check the status whether Neo4j is running.
* `systemctl stop neo4j` (After testing whether Neo4j is running, please disconnect the Neo4j service).

### 1.5) Change the password of NEO4j server(Important)
* After starting the Neo4j service (`systemctl start neo4j`) please open `http://localhost:7474/browser/` on your local browser.

* **Username:** `neo4j` 
  **Password:** `neo4j` 
  this will redirect you to set a new password.

### 1.6) Add server plugin (Java package) to the Neo4j:
* Stop the Neo4j instance before performing following steps (`systemctl stop neo4j`)
* `cp  com.dfki.LT.OntologyExplorer-1.0-SNAPSHOT.jar /var/lib/neo4j/plugins/`


## II) [ Neo4j-Database ]:
--------------------------

### 2.1) Create database for Neo4j (If you don't have graph.DB file)
* The default Neo4j function was used to create the DB.
* In order to create DB for Neo4j we need 4 files (*2 header files and 2 content files*)

#### Header files (attached with the repository in Header_files)
##### Create ( nheader.txt )
Content: `:ID,ConceptID,ConceptName` 

* `:ID`                   ==> Node IDbiomedical-dfki
* `ConceptID,ConceptName` ==> Properties of the node

##### Create ( rheader.txt ) 
Content: `:START_ID,:END_ID,:TYPE,RelationLabel,weight` 

* `:START_ID,:END_ID` ==> Node ID
* `:Type`             ==> Vocabulary
* `RelationLable`     ==> Relation Name
* `weight`            ==> Edge weight

#### Content file
##### Create nodefile(node.txt) 
This file contains data for node in 3 columns comma separated, without header.

##### Create relationfile(relation.txt)
This file contains data for relation in 4 columns comma separated, without header.


### 2.2) Command to create a Neo4j DB

`neo4j-import --into graph.db --nodes:<Node label> "nheader.txt,node.txt" --relationships "rheader.txt,relation.txt"  --skip-duplicate-node true`
* `--into` Name of the generated database
	- `graph.db` Recommended name
* `--nodes:UMLSConcepts` Node label **Note:** When you have one label only you provide it via this command, but when you have too many labels you must provide them via a file.
	- `"nheader,node"` Name of the **Node-Header-File** (nheader.txt) and the **Node-Content-File** (nodefile)
* `--relationships`
	- `"rheader,relation"` Name of the **Relation-Header-File** (rheader.txt) and the **Relation-Content-File** (relationfile)
* `--skip-duplicate-node` 
	- `true` Skip duplicate nodes

After running this command a **graph.db** folder will be generated in the present directory, you need to move this file into the following folder **/var/lib/neo4j/data/databases/**

## III) [ Additional information ]:
-----------------------------------

### 3.1) (optional) Change the default Neo4j Database **PATH**: 

Default location of the folder is:  **/var/lib/neo4j/data/databases/**

To change the path of the folder:

* Open **neo4j.conf** by typing `gedit /etc/neo4j/neo4j.conf`

* Replace line **dbms.directories.data=/var/lib/neo4j/data** with **dbms.directories.data=**`<folder of your choice>`

* Copy the **graph.db** into `<folder of your choice>`**/databases/**
    


### 3.2) Command to copy the graph.db file into Neo4j's database folder 

* `cp -r graph.db /var/lib/neo4j/data/databases/`



### 3.3) (IMPORTANT) Everytime you add a new graph.db file you must stop the Neo4j instance otherwise you will corrupt the database.

### 3.4) (IMPORTANT!!!) In order to exploit NEO4j's efficient graph traversal speed, we have to index the database and this can be done via 
* ` CREATE INDEX ON :<Node label>(<Node property>) ` 
* ` CREATE INDEX ON :UMLSConcepts(ConceptID) `


### 3.4) User-Interface:
* cd to UI/biomedical-dfki-0.1/bin
* Run `./biomedical-dfki`
* Open the browser and type http://localhost:9000/graph-kd


