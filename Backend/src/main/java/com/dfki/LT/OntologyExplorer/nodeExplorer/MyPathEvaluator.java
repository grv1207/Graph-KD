package com.dfki.LT.OntologyExplorer.nodeExplorer;

import org.neo4j.graphdb.Path;
import org.neo4j.graphdb.traversal.Evaluation;
import org.neo4j.graphdb.traversal.Evaluator;

/**
 * Created by gaurav on 22.12.17.
 */
public class MyPathEvaluator implements Evaluator {

    private String relationLabel;


    MyPathEvaluator(String relationLabel){

        this.relationLabel = relationLabel;

    }
    @Override
    public Evaluation evaluate(Path path) {
        if (path.length() == 0) return Evaluation.EXCLUDE_AND_CONTINUE;
        else {
            if (path.lastRelationship().getProperty("RelationLabel").toString().contains(relationLabel)){

                return Evaluation.INCLUDE_AND_PRUNE;
            }
            else return Evaluation.EXCLUDE_AND_CONTINUE;
        }



    }
}
