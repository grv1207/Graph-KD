package com.dfki.LT.OntologyExplorer.nodeExplorer;

import com.google.gson.Gson;
import junit.framework.Assert;
import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;
import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;
import org.neo4j.graphdb.*;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.neo4j.server.rest.repr.Representation;

import java.io.File;
import java.io.IOException;

/**
 * Created by gaurav on 08.11.17.
 */
public class GraphTraversalTest  {
    final static Logger logger = Logger.getLogger(GraphTraversalTest.class);
    protected GraphDatabaseService graphDb;
    @org.junit.Before
    public void setUp() {
        logger.debug("Setting Up DB");
        graphDb = new GraphDatabaseFactory().newEmbeddedDatabase(new File("DB/graph.db/"));

    }

    @org.junit.After
    public void tearDown() {
        logger.debug("shutting down DB");
        if (graphDb != null) {
            graphDb.shutdown();
        }

    }

    private void run(String source, int length, String[] vocab, String Label, Integer LabelType) throws Exception {
        GraphTraversal obj1 = new GraphTraversal();
        obj1.exploring(graphDb,source,vocab,Label, length,LabelType);

    }

    /**
     * Relation label :-)
     */
    @org.junit.Test
    public void test_relation_type_Depth1() throws Exception {
        // Depth 1 and total paths should be 9
        logger.debug(" Depth = 1 and total paths = 9");
        run("C0000039",3, new String[]{"all"},"MSH;RN;mapped_to",0);

    }
    @org.junit.Test
    public void test_relation_type_Depth3() throws Exception{

        // Depth 3 and total paths should be 2583
        logger.debug(" Depth = 3 and total paths = 2583");
        run("C0000039",3, new String[]{"all"},"NDFRT_FMTSME;RO;chemical_structure_of",0);
    }
    @org.junit.Test
    public void test_relation_type_Depth2() throws Exception{
        // Depth 2 and total paths should be 9
        logger.debug(" Depth = 2 and total paths = 9");
        run("C0000039",3, new String[]{"all"},"MSH;RO;has_mapping_qualifier",0);

    }


    /**
        for semantic type
      */
    @org.junit.Test
    public void test_semantic_type_Depth1() throws Exception {

        logger.debug(" Depth = 1 ,total paths = 11");
        run("C0000039",1, new String[]{"all"},"Organic Chemical",1);

    }
    @org.junit.Test
    public void test_semantic_type_Depth2() throws Exception{


        logger.debug(" Depth = 2 and total paths 9 ");
        run("C0000039",2, new String[]{"all"},"Chemical Viewed Structurally",1);
    }
    @org.junit.Test
    public void test_semantic_type_Depth3() throws Exception{

        logger.debug(" Depth = 3 and total paths = 1");
        run("C0000039",3, new String[]{"all"},"Amino Acid Peptide or Protein",1);

    }

    @org.junit.Test
    public void test_semantic_type_Depth4() throws Exception{

        logger.debug(" Depth = 2 and total paths = 1");
        run("C0003419",3, new String[]{"all"},"Sign or Symptom",1);

    }


}