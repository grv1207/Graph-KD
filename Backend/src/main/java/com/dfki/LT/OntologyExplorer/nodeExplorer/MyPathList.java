package com.dfki.LT.OntologyExplorer.nodeExplorer;


import org.neo4j.graphdb.Path;

/**
 * Created by gaurav on 02.01.18.
 */
public class MyPathList   {
    private  Path path;
    private  Integer length;


    MyPathList(Path path, Integer length){
        this.path = path;
        this.length = length;

    }

    public  Path getPath() {
        return path;
    }


    public  Integer getLength() {
        return length;
    }

    @Override
    public String toString() {
        return "MyPathList{path: "+getPath() +" length : "+getLength()+" }";
    }
}
