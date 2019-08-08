package com.dfki.LT.OntologyExplorer.kshortestpaths;

/**
 * PathExpander class is initiated to get paths of all types and  both directions
 * to find k-shortest path,  Neo4j GraphAlgoFactory Class is used which has findAllPaths methods
 * to limit to only k-shortest, path's length is limited to maxLength
 *
 * */

import org.apache.log4j.Logger;
import org.neo4j.graphalgo.GraphAlgoFactory;
import org.neo4j.graphdb.*;

import java.util.*;
/**
 * Created by gaurav on 08.11.17.
 */


public class KShortestPathsAlgo {
    final static Logger logger = Logger.getLogger(KShortestPathsAlgo.class);


    public List<Path> run(Node start, Node end, int maxLength, List<String> vocabList) {
        PathExpander myExpanderObj  = PathExpanders.allTypesAndDirections();

        List<Path> result = new LinkedList<Path>();
        for (int depth= 1; depth <= maxLength ; depth++) {
            for (Path path : GraphAlgoFactory.shortestPath(myExpanderObj,depth).findAllPaths(start, end) )
                if (!result.contains(path))
                    if (vocabList.contains("all"))
                        result.add(path);

                    else {
                        int counter = 0;
                        for (Relationship rel : path.relationships())
                            if (vocabList.contains(rel.getType().name().toString())) {
                                counter++;
                            }
                        if (depth == counter)
                            result.add(path);
                    }
            if(result.size() > 0) break;
            else logger.debug("Path ~found @ Depth: "+String.valueOf(depth) );
        }
        return result;

    }
}
