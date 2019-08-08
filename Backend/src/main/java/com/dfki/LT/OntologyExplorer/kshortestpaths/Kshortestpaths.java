package com.dfki.LT.OntologyExplorer.kshortestpaths;
/**
 * Pass src node and target node to KshortestPathsAlgo to get a list of all the shortest paths
 * convert pathList to an array of nodes and relationship and then pass it to UI as a json string.
 *
 * */

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import org.apache.commons.lang.StringUtils;
import org.apache.log4j.Logger;
import org.neo4j.graphdb.*;
import org.neo4j.server.plugins.*;
import org.neo4j.server.rest.repr.Representation;
import org.neo4j.server.rest.repr.ValueRepresentation;

import java.util.*;
import java.util.stream.Collectors;

public class Kshortestpaths extends ServerPlugin {
        final static Logger logger = Logger.getLogger(Kshortestpaths.class);
        @Description("Get the k-shortest paths from source to target")
        @PluginTarget(GraphDatabaseService.class)

        public Representation kshortestpaths(
                @Source GraphDatabaseService graphDb,
                @Description("Source node of the path") @Parameter(name = "concept1") String src,
                @Description("Target node of the path") @Parameter(name = "concept2") String trgt,
                @Description("The max depth for a paths to retrieve") @Parameter(name = "length") Integer l,
                @Description("Vocabulary of the concept pair") @Parameter(name = "vocabulary") String  Vocabulary[]

        )

        {
            StringBuilder sb = new StringBuilder();
            sb.append("Received Request for k-shortest src: :").append(String.valueOf(src))
                    .append(", target:").append(String.valueOf(trgt))
                    .append(", vocab:").append(Arrays.asList(Vocabulary))
                    .append(", depth:").append(String.valueOf(l))
            ;

            logger.info(sb);

            List<Map<String, Object>> pathList = new ArrayList<>() ;
            String resJSON ;
            List<String> vocabList = new ArrayList<>(Arrays.asList(Vocabulary));
            Transaction tx = graphDb.beginTx() ;

            KShortestPathsAlgo algo = new KShortestPathsAlgo();  // set debug
            Label conceptlabel = Label.label("UMLSConcepts");

            Node source =  graphDb.findNode(conceptlabel, "ConceptID",src);
            Node target = graphDb.findNode(conceptlabel, "ConceptID",trgt);


            try {
                pathList = algo.run(source, target, l, vocabList)
                        .stream()
                        .map(path -> getPathAsMap(path))
                        .collect(Collectors.toList());
                logger.debug(String.valueOf(pathList.stream().count()));

            }
            catch (Exception ex){
                logger.fatal(ex.getMessage());
                logger.debug("exception");

            }
            finally {
                tx.success();
                tx.close();

                Gson gson = new Gson();
                resJSON = gson.toJson(pathList, pathList.getClass());
                StringBuilder sb2 = new StringBuilder();
                sb2.append("Total Paths found: ").append(String.valueOf(pathList.stream().count())) ;

                logger.info(sb2);


            }



            return ValueRepresentation.string(resJSON);
        }



    private static  Map<String, Object> getPathAsMap(Path path) {
        Map<String, Object> p = new HashMap<>();
        int weight = 0;

        for (Relationship rel : path.relationships()) {

            weight = weight + getRelationshipWeight(rel);


        }
        p.put("WeightPerPath",weight);



        return toMap(path, p);
    }

    private static int getRelationshipWeight(Relationship rel) {
        int weight;
        weight = Integer.parseInt(String.valueOf(rel.getProperty("weight")));
        return weight;
    }



    private static Map<String, Object> toMap(Path path, Map<String, Object> p) {


        List<Map<String, Object>> nodes = new ArrayList<>();
        List<Map<String, Object>> edges = new ArrayList<>();
        for (Node node : path.nodes()) {
            nodes.add(getNodeAsMap(node));
        }
        p.put("nodes", nodes);

        for (Relationship rel : path.relationships()) {
            edges.add(getRelationshipAsMap(rel));
        }

        p.put("edges", edges);


        return p;
    }

    private static  Map<String, Object> getNodeAsMap(Node node) {
        Map<String, Object> n = new HashMap<>();
        n.put("properties", getPropertyMap(node));
        return n;
    }

    private static  Map<String, Object> getRelationshipAsMap(Relationship relationship) {
        Map<String, Object> r = new HashMap<>();
        r.put("type", relationship.getProperty("RelationLabel"));
        r.put("sourceNode", getPropertyRel(relationship.getStartNode()));
        r.put("targetNode", getPropertyRel(relationship.getEndNode()));
        r.put("WeightPerEdge",relationship.getProperty("weight"));


        return r;
    }


    private static Map<String, Object> getPropertyMap(PropertyContainer container) {
        Map<String, Object> properties = new HashMap<>();
        for (String key : container.getPropertyKeys()) {
            properties.put(key, container.getProperty(key));
        }
        return properties;
    }
    private static Map<String, Object> getPropertyRel(PropertyContainer container) {
        Map<String, Object> properties = new HashMap<>();
        properties.put("ConceptID", container.getProperty("ConceptID"));


        return properties;
    }




}
