import numpy as np
from skge.util import ccorr
import pickle

from urllib import request
import json

import mysql.connector
with open('semantic_dict_count_old.json', 'r') as f:
    semantic_dict = json.load(f)

class Inference():
    def __init__(self):
        self.toJson()

    def toJson(self, nodePair, transitiveLabel):
        """


        :param nodePair: source node and target node
        :param transitiveLabel: edges label
        :return: dictionary of edge that has source and target node with their property and the label of edge
        """
        dict_edge = {}
        # same side ???
        # opp side key that has max value in length
        concept_dict1, concept_dict2 = {}, {}

        concept_dict1["ConceptID"] = nodePair["source"]
        dict_edge["sourceNode"] = concept_dict1

        concept_dict2["ConceptID"] = nodePair["target"]
        dict_edge["targetNode"] = concept_dict2
        dict_edge["type"] = transitiveLabel

        return dict_edge


class TransitiveInference(Inference):
    # pathDict = dict()

    def __init__(self, singlePath):
        self.pathDict = singlePath
        #self.trans_main()

    def trans_main(self):
        """

        :param pathDict: single path
        :return: dictionary of transitive edge(s)/ relation(s) if they obey transitive rule
        """
        """
        1. check if path contains CHD/PAR/isa label in its edges   ['LNC#CHD_', 'LNC#RO_has_time_aspect', 'LNC#RO_has_time_aspect', 'LNC#RO_answer_to']
        2. get transitive relation
        """
        RelationLabel = []
        TransLabels = ["CHD", "PAR", "isa"]

        for edge in self.pathDict[u'edges']:
            RelationLabel.append(edge[u'type'])

        for rel in RelationLabel:
            for label in TransLabels:
                if label in rel:
                    return self.transitiveInference(rel)

    def transitiveInference(self, transRelLabel):
        edgeList = list()

        for i in range(len(self.pathDict[u'edges']) - 1):
            nodeDict = dict()
            relSet = []

            """
            when atleast one relation type is  transRelLabel
            """
            if self.pathDict[u'edges'][i][u'type'] == transRelLabel or self.pathDict[u'edges'][i + 1][
                u'type'] == transRelLabel:

                """
                relation in same direction
                """
                if (self.pathDict[u'edges'][i][u'targetNode'][u'ConceptID'] ==
                        self.pathDict[u'edges'][i + 1][u'sourceNode'][
                            u'ConceptID']
                        or self.pathDict[u'edges'][i][u'sourceNode'][u'ConceptID'] ==
                        self.pathDict[u'edges'][i + 1][u'targetNode'][
                            u'ConceptID']):

                    nodeDict, relSet = self.getSameDirectionTransNode(nodeDict, self.pathDict[u'edges'][i], relSet)
                    nodeDict, relSet = self.getSameDirectionTransNode(nodeDict, self.pathDict[u'edges'][i + 1], relSet)

                    if (relSet[0] == relSet[1] and relSet[0] == transRelLabel):
                        edgeList.append(self.toJson(nodeDict, str("transitive--" + transRelLabel)))  # eg isa, isa

                    elif (relSet[0] != relSet[1] and relSet[0] == transRelLabel):
                        edgeList.append(self.toJson(nodeDict, str("transitive--" + relSet[1])))  # eg isa, rx

                    elif relSet[0] != relSet[1] and relSet[1] == transRelLabel:
                        edgeList.append(self.toJson(nodeDict, str("transitive--" + relSet[0])))  # eg rx, isa

                    """ 
                    2 relations in opposite direction and have same source
                    """
                elif (self.pathDict[u'edges'][i][u'sourceNode'][u'ConceptID'] ==
                      self.pathDict[u'edges'][i + 1][u'sourceNode'][
                          u'ConceptID']):
                    edgeList = self.checkRelationLabel("sourceNode", i,
                                                   str(
                                                       "transitive--" + transRelLabel))

                    """
                     2 relations in opposite direction and have same target
                    """

                elif (self.pathDict[u'edges'][i][u'targetNode'][u'ConceptID'] ==
                      self.pathDict[u'edges'][i + 1][u'targetNode'][
                          u'ConceptID']):
                    edgeList = self.checkRelationLabel("targetNode", i,
                                                   str(
                                                       "transitive--" + transRelLabel))

        return edgeList

    def checkRelationLabel(self, str, i, transRelLabel):
        """
        check both the relation label and based upon that decides which node is going to source node and target node
        """

        edgeList = list()
        tempnodeDict, tempnodeDict2 = {}, {}
        if str == "sourceNode":
            str = "targetNode"
        elif str == "targetNode":
            str = "sourceNode"

        tempnodeDict["source"] = self.pathDict[u'edges'][i][str][u'ConceptID']
        tempnodeDict["target"] = self.pathDict[u'edges'][i + 1][str][u'ConceptID']

        tempnodeDict2["source"] = self.pathDict[u'edges'][i + 1][str][u'ConceptID']
        tempnodeDict2["target"] = self.pathDict[u'edges'][i][str][u'ConceptID']

        relset = [self.pathDict[u'edges'][i][u'type'], self.pathDict[u'edges'][i + 1][u'type']]

        if relset[0] == relset[1] and relset[0] == transRelLabel:
            edgeList.append(self.toJson(tempnodeDict, transRelLabel))  # eg isa, isa
            edgeList.append(self.toJson(tempnodeDict2, transRelLabel))  # eg isa, isa

        elif relset[0] != relset[1] and relset[0] == transRelLabel:
            edgeList.append(self.toJson(tempnodeDict, relset[1]))  # eg isa, -> rx

        elif relset[0] != relset[1] and relset[1] == transRelLabel:
            edgeList.append(self.toJson(tempnodeDict2, relset[0]))  # eg rx, isa

        return edgeList

    def getSameDirectionTransNode(self, nodeDict, edge, relSet):
        """
        This gets transitive relation when edges are in same direction i:e,

        (a)--[isa]-->(b)--[rx]-->(c) and (a)<--[isa]--(b)<--[rx]--(c)

        :param nodeDict: dictionary of source and target in a single edge
        :param edge: a single edge
        :param relSet: edge label
        :return: nodeDict,relSet
        """
        if not bool(nodeDict):
            nodeDict["target"] = str(edge[u'targetNode'][u'ConceptID'])
            nodeDict["source"] = str(edge[u'sourceNode'][u'ConceptID'])
            relSet.append(str(edge[u'type']))
            return nodeDict, relSet

        elif nodeDict["target"] in (str(edge[u'targetNode'][u'ConceptID']), str(edge[u'sourceNode'][u'ConceptID'])):

            nodeDict["target"] = str(edge[u'targetNode'][u'ConceptID'])
            relSet.append(str(edge[u'type']))
            return nodeDict, relSet

        elif nodeDict["source"] in (str(edge[u'targetNode'][u'ConceptID']), str(edge[u'sourceNode'][u'ConceptID'])):
            nodeDict["source"] = str(edge[u'sourceNode'][u'ConceptID'])
            relSet.append(str(edge[u'type']))
            return nodeDict, relSet


class HolographicInference(Inference):

    def __init__(self, singPath):
        #Inference.__init__(self)
        self.pathDict = singPath
        #self.relDict = relDict
        #self.hole_main()

    def mysqlconnection(self, NodePair):
        edge_list = []
        node1 = NodePair[0]
        node2 = NodePair[1]
        #cnx = mysql.connector.connect(host='127.0.0.1', user='admin', passwd='719b6917', db='holographic_DB')
        cnx =  mysql.connector.connect(host='127.0.0.1', user='root', passwd='123', db='holographic_DB') #new_holo_DB holographic_DB

        cursor = cnx.cursor()
        queryString = "SELECT Nodeparameters.* FROM Nodeparameters inner join NodeMapping " \
                      "WHERE NodeMapping.CUIID =  %s and NodeMapping.NodeID= Nodeparameters.NodeID;"

        cursor.execute(queryString, [node1])
        listNode1Embedding = []
        for values in cursor:
            listNode1Embedding.append(values[1:])

        if (bool(listNode1Embedding)):
            sourceEmbedding = np.array(listNode1Embedding[0])
            npSourceEmbedding = np.float64([sourceEmbedding, ]*166 ) #len(self.relDict)

            cursor.execute(queryString, [node2])
            listNode2Embedding = []
            for values in cursor:
                listNode2Embedding.append(values[1:])

            if (bool(listNode2Embedding)):
                TargetEmbedding = np.array(listNode2Embedding[0])
                npTargetEmbedding = np.float64([TargetEmbedding, ] *166 ) #len(self.relDict)

                cursor.execute(
                    "SELECT rp.* FROM Relparameters rp  order by rp.RelID") #inner join UIRelMapping rm on rm.RelID = rp.RelID;

                listRelEmbedding = []
                completedRelEmbed = []
                for values in cursor:
                    listRelEmbedding.append(values[1:])
                    completedRelEmbed.append(values)
                relArray = np.float64(listRelEmbedding)

                score = self._scores(npSourceEmbedding,relArray, npTargetEmbedding)
                #print(score)
                above_threshold = np.argwhere(score >= 1.692736  )[:, 0] # old - 1.692736 1.713793
                #print(above_threshold)
                #print(score[49],score[8])
                if len(above_threshold)>0:
                    #if len(above_threshold)>3:
                        #above_threshold = sorted(range(len(above_threshold)), key=lambda i: above_threshold[i], reverse=True)[:3]

                    format_strings = ','.join(['%s'] * len(above_threshold))

                    query = "SELECT rp.* FROM RelMapping rp  where rp.RelID IN (%s) order by rp.RelID "%format_strings
                    #print(query)

                    cursor.execute( query, [x for x in map(int,above_threshold)])

                    for values in cursor:
                        if self.semantic_sanity_check(node1,node2,values[0]):

                            localNodeDict = dict()
                            localNodeDict['source'] = node1
                            localNodeDict['target'] = node2
                            #print(values[0],score[values[1]])
                            edge_list.append(self.toJson(localNodeDict,values[0]))
                    #cursor.execute(queryString, [argument_string])
                    return edge_list
                else:
                    return None


    def semantic_sanity_check(self,node1,node2,rel_type):
        valid_tuple_instance = False
        node1_semantic_list = ''.join(self.get_semantic_from_solr(node1))
        node2_semantic_list = ''.join(self.get_semantic_from_solr(node2))
        for node1_semantic in node1_semantic_list.split(';'):
            for node2_semantic in node2_semantic_list.split(';'):
                node1_semantic = node1_semantic.strip().replace(',', '')
                node2_semantic = node2_semantic.strip().replace(',', '')
                if  rel_type in  semantic_dict[node1_semantic][node2_semantic].keys():
                     valid_tuple_instance = True
                     return valid_tuple_instance

                elif rel_type in semantic_dict[node2_semantic][node1_semantic].keys():
                     valid_tuple_instance = True
                     return valid_tuple_instance

        return valid_tuple_instance




    def get_semantic_from_solr (self,node):
        connection = request.urlopen('http://127.0.0.1:8983/solr/MRSTY/select?indent=on&q=IX_umlsCode:'+node+'&wt=python')  # http://127.0.0.1:8983/solr/MRSTY
        #connection = request.urlopen('http://127.0.0.1:8986/solr/MRSTY/select?indent=on&q=IX_umlsCode:'+node+'&wt=python')

        response = eval(connection.read())

        return response['response']['docs'][0]['IX_sty']

    def score_dictionary(self,NodePair):
        edge_list = []
        node1 = NodePair[0]
        node2 = NodePair[1]
        cnx = mysql.connector.connect(host='127.0.0.1', user='root', passwd='123', db='holographic_DB')

        cursor = cnx.cursor()
        queryString_node = "SELECT NodeID from NodeMapping " \
                      "WHERE NodeMapping.CUIID =  %s "

        queryString_relID = "SELECT RelID from RelMapping "

        cursor.execute(queryString_node, [node1])
        src_id,trgt_id=0,0
        for values in cursor:
            src_id = values[0]

        cursor.execute(queryString_node, [node2])

        for values in cursor:
            trgt_id = values[0]

        ll_rel= np.arange(0,166,dtype=int)

        ll_src = [src_id]*len(ll_rel)
        ll_tgt = [trgt_id] * len(ll_rel)
        score = model._scores(ll_src,ll_rel,ll_tgt)

        above_threshold = np.argwhere(score >= 1.692736)[:, 0]
        print(score[49], score[8])
        if len(above_threshold) > 0:
            # if len(above_threshold)>3:
            # above_threshold = sorted(range(len(above_threshold)), key=lambda i: above_threshold[i], reverse=True)[:3]

            format_strings = ','.join(['%s'] * len(above_threshold))

            query = "SELECT rp.* FROM RelMapping rp  where rp.RelID IN (%s) order by rp.RelID " % format_strings

            cursor.execute(query, [x for x in map(int, above_threshold)])
            for values in cursor:
                localNodeDict = dict()
                localNodeDict['source'] = node2
                localNodeDict['target'] = node1
                print(values[0], score[values[1]])
                edge_list.append(self.toJson(localNodeDict, values[0]))
            # cursor.execute(queryString, [argument_string])
            return edge_list
        else:
            return None


    def _scores(self,  SourceEmbedding, relArray,TargetEmbedding):
        return np.sum(relArray * ccorr(SourceEmbedding,TargetEmbedding), axis=1)

    def hole_main(self):
        NodePair = []
        #edgeList = []
        # all the edges in a single path
        for edge in self.pathDict[u'edges']:
            """
            This gets me first and last node of a path
            """
            srcnode = edge[u'sourceNode'][u'ConceptID']
            targetnode = edge[u'targetNode'][u'ConceptID']

            if (NodePair.__contains__(srcnode)):
                NodePair.remove(srcnode)
            else:
                NodePair.append(srcnode)

            if (NodePair.__contains__(targetnode)):
                NodePair.remove(targetnode)
            else:
                NodePair.append(targetnode)

        # we should have src and target nodes of a single path in Nodeset
        first_holo = self.mysqlconnection(NodePair)
        second_holo = self.mysqlconnection(NodePair[::-1])
        #first_holo = self.score_dictionary(NodePair)

        if first_holo :
            #not bool(first_holo) or not first_holo.__contains__("empty"):
            newedgeList = list(filter(("empty").__ne__, first_holo))
            return newedgeList
        elif second_holo:
            newedgeList = list(filter(("empty").__ne__, second_holo))
            return newedgeList
        else:
            return None

