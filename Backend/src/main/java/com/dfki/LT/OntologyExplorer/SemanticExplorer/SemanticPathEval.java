package com.dfki.LT.OntologyExplorer.SemanticExplorer;

import org.neo4j.graphdb.Path;
import org.neo4j.graphdb.traversal.Evaluation;
import org.neo4j.graphdb.traversal.Evaluator;

public class SemanticPathEval implements Evaluator {

    private String semanticType;


    SemanticPathEval(String semanticType){

        this.semanticType = semanticType;

    }
    @Override
    public Evaluation evaluate(Path path) {
        if (path.length() == 0) return Evaluation.EXCLUDE_AND_CONTINUE;
        else {
            //System.out.println(path);
            //System.out.println(path.endNode().getProperty("ConceptSymantic").toString());
            if (path.endNode().getProperty("ConceptSymantic").toString().contains(semanticType)){
                //System.out.println(path.toString());

                return Evaluation.INCLUDE_AND_PRUNE;
            }
            else return Evaluation.EXCLUDE_AND_CONTINUE;
        }



    }
}
