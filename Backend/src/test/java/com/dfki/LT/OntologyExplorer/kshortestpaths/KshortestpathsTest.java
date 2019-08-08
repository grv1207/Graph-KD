package com.dfki.LT.OntologyExplorer.kshortestpaths;

import static org.junit.Assert.*;
import org.apache.log4j.Logger;
import org.junit.Assert;
import org.junit.Test;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.neo4j.server.rest.repr.Representation;

import java.io.File;

/**
 * Created by gaurav on 08.11.17.
 */
public class KshortestpathsTest {

    final static Logger logger = Logger.getLogger(KshortestpathsTest.class);
    protected GraphDatabaseService graphDb;
    @org.junit.Before
    public void setUp() throws Exception {
        logger.debug("Setting Up DB");
        graphDb = new GraphDatabaseFactory().newEmbeddedDatabase(new File("DB/graph.db/"));

    }

    @org.junit.After
    public void tearDown() throws Exception {
        logger.debug("shutting down DB");
        if (graphDb != null) {
            graphDb.shutdown();
        }
    }

    public String run(String source,String target ,int depth, String[] vocab){
        Kshortestpaths testKpaths = new Kshortestpaths();
        Representation out = testKpaths.kshortestpaths(graphDb,source,target,depth,vocab);
        return out.toString();
    }

    @Test
    public void AllVocabDepthOne() {
        logger.info("1 Direct Path");
            run("C0000039", "C0043950", 1, new String[]{"all"});
    }


    @Test
    public void AllVocabDepthTwo() {
        logger.info("3 Paths should be there");
       run("C0003419","C0030193",2,new String[]{"NDFRT","MSH"});
    }

    @Test
    public void AllMultiVocabDepth() {
        logger.info("10 Paths should be there");
        run("C0003419", "C0030193", 3, new String[]{"all"});

    }
    /*

    @Test
    public void MultivocabDepthOne() {
        Assert.assertEquals(run("C0003419","C0030193",1,new String[]{"NDFRT","MSH"}),1);
    }

    @Test
    public void SingleVocabDepthOne() {

        Assert.assertEquals(run("C0003419","C0030193",1,new String[]{"NDFRT"}),1);
    }
    @Test
    public void MultivocabDepthThree() {
        Assert.assertEquals(run("C0003419","C0030193",2,new String[]{"NDFRT","MSH"}),3);
    }

    @Test
    public void SingleVocabDepthThree() {
        Assert.assertEquals(run("C0003419","C0030193",2,new String[]{"NDFRT"}),3);
    } */


}