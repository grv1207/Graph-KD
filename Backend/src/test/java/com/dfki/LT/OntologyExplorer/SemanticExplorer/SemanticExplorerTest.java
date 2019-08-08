package com.dfki.LT.OntologyExplorer.SemanticExplorer;

import org.apache.log4j.Logger;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.neo4j.graphdb.factory.GraphDatabaseSettings;

import java.io.File;

public class SemanticExplorerTest {


    final static Logger logger = Logger.getLogger(SemanticExplorerTest.class);

    protected GraphDatabaseService graphDb;
    @org.junit.Before
    public void setUp() {
        logger.debug("Setting Up DB");
        graphDb = new GraphDatabaseFactory().newEmbeddedDatabaseBuilder(new File("DB/graph.db/"))
                .setConfig(GraphDatabaseSettings.allow_upgrade,"true")
                .newGraphDatabase();
        //registerShutdownHook( graphDb );
    }

    @org.junit.After
    public void tearDown() {
        logger.debug("shutting down DB");
        if (graphDb != null) {
            graphDb.shutdown();
        }

    }

    private void run(String source, int length, String[] vocab, String semanticType) throws Exception {
        SemanticNodeExplorer obj1 = new SemanticNodeExplorer();
        obj1.semanticExploration(graphDb,source,vocab,semanticType, length);

    }


    /**
     * Rigourous Test :-)
     */
    @org.junit.Test
    public void testDepth1() throws Exception {

        logger.debug(" Depth = 1 ,total paths = 11");
        run("C0000039",1, new String[]{"all"},"Organic Chemical");

    }
    @org.junit.Test
    public void testDepth3() throws Exception{

        // Depth 2 and total paths should be 2583   C0002776
        logger.debug(" Depth = 2 and total paths 9 ");
        run("C0000039",2, new String[]{"all"},"Chemical Viewed Structurally");
    }
    @org.junit.Test
    public void testDepth2() throws Exception{
        // Depth 2 and total paths should be 9
        logger.debug(" Depth = 3 and total paths = 1");
        run("C0000039",3, new String[]{"all"},"Amino Acid Peptide or Protein");

    }
}
