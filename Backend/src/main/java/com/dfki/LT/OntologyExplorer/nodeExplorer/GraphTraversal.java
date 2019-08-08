package com.dfki.LT.OntologyExplorer.nodeExplorer;

import com.google.gson.Gson;
import org.apache.log4j.Logger;
import org.neo4j.graphdb.*;
import org.neo4j.graphdb.traversal.Evaluators;
import org.neo4j.graphdb.traversal.TraversalDescription;
import org.neo4j.graphdb.traversal.Uniqueness;
import org.neo4j.server.plugins.*;
import org.neo4j.server.rest.repr.Representation;
import org.neo4j.server.rest.repr.ValueRepresentation;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by gaurav on 08.11.17.
 */

public class GraphTraversal extends ServerPlugin  {
    final static Logger logger = Logger.getLogger(GraphTraversal.class);

    @Description("Get all paths within a range of given path length, default is 3 and  having specific relationship label")
    @PluginTarget(GraphDatabaseService.class)

    public Representation exploring(
            @Source GraphDatabaseService graphDb,
            @Description("Source node of the path") @Parameter(name = "source") String Source,
            @Description("Vocabulary of the concept pair") @Parameter(name = "vocabulary") String  Vocabulary[],
            @Description("label contained in the path") @Parameter(name = "label" ) String LabelName,
            @Description("Depth to which to explore, Default value is 3 ") @Parameter(name = "depth", optional = true ) Integer Depth,
            @Description("Boolean value if 0 then node with relation label, if 1 the node with semantic") @Parameter(name = "labelType") Integer LabelType
    )  {
        System.out.print(Source);
        Transaction tx = graphDb.beginTx();
        Label conceptlabel = Label.label("UMLSConcepts");
        Node src =  graphDb.findNode(conceptlabel, "ConceptID",Source);
        String resJSON ;
        List<Map<String, Object>> paths = new ArrayList<>() ;
        if (src != null){
            List<String> vocabList = new ArrayList<>(Arrays.asList(Vocabulary));


            int traversalDepth = (Depth == null ? 3 : Depth );

            int travserser=1 ;
            /**long startTraversertime = System.currentTimeMillis();
            long endTraversertime = System.currentTimeMillis();
            long stopTraverse = endTraversertime - startTraversertime ; */

            // for semantic type node
            if (LabelType==1){
                while(paths.isEmpty() && travserser <=traversalDepth  ){ // && stopTraverse <= 16L
                    paths = explorePath_semantic(graphDb,src,LabelName,vocabList,travserser);
                    travserser ++ ;
                    //endTraversertime = System.currentTimeMillis();
                    //stopTraverse = endTraversertime - startTraversertime ;
                }

            }
            // for relation label node
            else {
                while(paths.isEmpty() && travserser <=traversalDepth  ){ //&& stopTraverse <= 16L
                    paths = explorePath_relation(graphDb,src,LabelName,vocabList,travserser);
                    travserser ++ ;
                    //endTraversertime = System.currentTimeMillis();
                    //stopTraverse = endTraversertime - startTraversertime ;
                }


            }




            StringBuilder sb = new StringBuilder();
            sb.append("Total graphs for src:").append(Source)
                    .append(" traversal_Depth:").append(String.valueOf(travserser-1))
                    .append("  vocab:").append(String.valueOf(vocabList)).append("  and Label:").append(LabelName).append(" is :").append(String.valueOf(paths.stream().count())) ;

            logger.info(sb);

        }
        else {
            StringBuilder sb = new StringBuilder();
            sb.append("Node: ").append(Source).append("  does not exist!!!");
            logger.info(sb);


        }
        tx.success();
        tx.close();
        Gson gson = new Gson();
        resJSON = gson.toJson(paths, paths.getClass());
        return ValueRepresentation.string(resJSON);



    }




    private List<Map<String, Object>> explorePath_relation(GraphDatabaseService graphDb, Node srcnode, String RelationLabel, List<String> vocabList, int Depth )  {
        MyPathEvaluator myevaluatorObj = new MyPathEvaluator(RelationLabel);
        TraversalDescription td = graphDb.traversalDescription();
        List<Path> PathList = new ArrayList<>();
        if(vocabList.contains("all")){

            PathList = td.depthFirst()     // this is fast when compared to breadth first
                    .evaluator(Evaluators.fromDepth(1))
                    .evaluator(Evaluators.atDepth(Depth))
                    .evaluator(myevaluatorObj)
                    .uniqueness(Uniqueness.NODE_PATH)
                    .traverse(srcnode)
                    .stream().collect(Collectors.toList());


        } else {
            if(vocabList.size()==1){
                PathList = td.breadthFirst()
                        .evaluator(Evaluators.fromDepth(1))
                        .evaluator(Evaluators.toDepth(Depth))
                        .evaluator(myevaluatorObj)
                        .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                        .uniqueness(Uniqueness.NODE_PATH)
                        .traverse(srcnode)
                        .stream().collect(Collectors.toList());
            }

                else if(vocabList.size()==2){
                    PathList = td.breadthFirst()
                            .evaluator(Evaluators.fromDepth(1))
                            .evaluator(Evaluators.toDepth(Depth))
                            .evaluator(myevaluatorObj)
                            .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                            .relationships(RelationshipType.withName(vocabList.get(1)),Direction.BOTH)
                            .uniqueness(Uniqueness.NODE_PATH)
                            .traverse(srcnode)
                            .stream().collect(Collectors.toList());
                }
            else if(vocabList.size()==3){
                PathList = td.breadthFirst()
                        .evaluator(Evaluators.fromDepth(1))
                        .evaluator(Evaluators.toDepth(Depth))
                        .evaluator(myevaluatorObj)
                        .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                        .relationships(RelationshipType.withName(vocabList.get(1)),Direction.BOTH)
                        .relationships(RelationshipType.withName(vocabList.get(2)),Direction.BOTH)
                        .uniqueness(Uniqueness.NODE_PATH)
                        .traverse(srcnode)
                        .stream().collect(Collectors.toList());
                }
            else logger.info("Please provide either All or maximum of 3 vocabulary");


            }

        List<Map<String, Object>> finalPaths;
        finalPaths  = PathList.stream().map(path -> getPathAsMap(path)).collect(Collectors.toList());

        return finalPaths;
    }


    private List<Map<String, Object>> explorePath_semantic(GraphDatabaseService graphDb, Node srcnode, String semanticType, List<String> vocabList, int Depth )  {
        SemanticPathEval myevaluatorObj = new SemanticPathEval(semanticType);
        TraversalDescription td = graphDb.traversalDescription();
        List<Path> PathList = new ArrayList<>();
        if(vocabList.contains("all")){

            PathList = td.breadthFirst()     // this is fast when compared to breadth first
                    .evaluator(Evaluators.fromDepth(1))
                    .evaluator(Evaluators.atDepth(Depth))
                    .evaluator(myevaluatorObj)
                    .uniqueness(Uniqueness.NODE_PATH)
                    .traverse(srcnode)
                    .stream().collect(Collectors.toList());


        } else {
            if(vocabList.size()==1){
                PathList = td.breadthFirst()
                        .evaluator(Evaluators.fromDepth(1))
                        .evaluator(Evaluators.toDepth(Depth))
                        .evaluator(myevaluatorObj)
                        .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                        .uniqueness(Uniqueness.NODE_PATH)
                        .traverse(srcnode)
                        .stream().collect(Collectors.toList());
            }

            else if(vocabList.size()==2){
                PathList = td.breadthFirst()
                        .evaluator(Evaluators.fromDepth(1))
                        .evaluator(Evaluators.toDepth(Depth))
                        .evaluator(myevaluatorObj)
                        .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                        .relationships(RelationshipType.withName(vocabList.get(1)),Direction.BOTH)
                        .uniqueness(Uniqueness.NODE_PATH)
                        .traverse(srcnode)
                        .stream().collect(Collectors.toList());
            }
            else if(vocabList.size()==3){
                PathList = td.breadthFirst()
                        .evaluator(Evaluators.fromDepth(1))
                        .evaluator(Evaluators.toDepth(Depth))
                        .evaluator(myevaluatorObj)
                        .relationships(RelationshipType.withName(vocabList.get(0)),Direction.BOTH)
                        .relationships(RelationshipType.withName(vocabList.get(1)),Direction.BOTH)
                        .relationships(RelationshipType.withName(vocabList.get(2)),Direction.BOTH)
                        .uniqueness(Uniqueness.NODE_PATH)
                        .traverse(srcnode)
                        .stream().collect(Collectors.toList());
            }
            else logger.info("Please provide either All or maximum of 3 vocabulary");


        }

        List<Map<String, Object>> finalPaths;
        finalPaths  = PathList.stream().map(path -> getPathAsMap(path)).collect(Collectors.toList());

        return finalPaths;
    }







    static  Map<String, Object> getPathAsMap( Path path) {
        Map<String, Object> p = new HashMap<>();
        return toMap( path, p);
    }


     static Map<String, Object> toMap(Path path, Map<String, Object> p) {
        List<Map<String, Object>> nodes = new ArrayList<>();
        for (Node node : path.nodes()) {
            nodes.add(getNodeAsMap(node));
        }
        p.put("nodes", nodes);

        List<Map<String, Object>> edges = new ArrayList<>();
        for (Relationship rel : path.relationships()) {
            edges.add(getRelationshipAsMap(rel));
        }

        p.put("edges", edges);
        return p;
    }




    static  Map<String, Object> getNodeAsMap(Node node) {
        Map<String, Object> n = new HashMap<>();
        n.put("properties", getPropertyMap(node));
        return n;
    }


    static  Map<String, Object> getRelationshipAsMap(Relationship relationship) {

    Map<String, Object> r = new HashMap<>();
    r.put("type", relationship.getProperty("RelationLabel"));
    r.put("sourceNode", getPropertyRel(relationship.getStartNode()));
    r.put("targetNode", getPropertyRel(relationship.getEndNode()));
    return r;
    }

    static Map<String, Object> getPropertyMap(Node node) {
        Map<String, Object> properties = new HashMap<>();
        properties.put("ConceptName", node.getProperty("ConceptName"));
        properties.put("ConceptID", node.getProperty("ConceptID"));

        return properties;
    }

    static Map<String, Object> getPropertyRel(PropertyContainer container) {
    Map<String, Object> properties = new HashMap<>();
    properties.put("ConceptID", container.getProperty("ConceptID"));
    return properties;
    }

}
