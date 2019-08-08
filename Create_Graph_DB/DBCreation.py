import re
import sys
import argparse
import codecs

def processfile():
    "Gets unique pair of vocab_RelationLabel_Relation and save it in a file called UMLS_final"
    f_out_final = open("UMLS_final", 'w')
    cnt=0
    umls_rel={}
    #file = open("UMLS_relations.txt", encoding='utf8')
    file = codecs.open(sys.argv[1], encoding='utf8')
    for umls in file:
    #with open('UMLS_relations.txt', 'rb') as umls:

        umls = re.sub("\t","", umls)
        umls = re.sub("^ *", "", umls)
        umls = re.sub("\n", "", umls)
        umls = re.sub(" ", "|", umls)
        data=umls.split("|")

        nr=data[0]#
        reference = data[1]+"_"+data[3]
        rel=data[1]
        rela=data[2]

        if int(nr) > 50:
            if not (rela=="" and not (rel=="CHD" )):
                if nr not in umls_rel:
                    umls_rel[nr]={}

                if reference not in umls_rel[nr]:
                    umls_rel[nr][reference]={}

                umls_rel[nr][reference][rela]=0


    for numb in umls_rel.keys():


        for rel_lab in umls_rel[numb].keys():



            if len(umls_rel[numb][rel_lab])<=2:
                #print ("great!")
                tmp_str=re.sub("_", "|", rel_lab)
                f_out_final.write(tmp_str+"|"+list(umls_rel[numb][rel_lab].keys())[0]+"\n")
            """else:
                print ("numb:", numb)
                print (">", rel_lab, "::", umls_rel[numb][rel_lab])
                print ("analyse")"""
    print("UMLS_final file created")
def CreateDictionary():
    umls = codecs.open('UMLS_final',encoding='utf8')
    umls_dict = {}
    for line in umls:
        line = re.sub("\n","",line)
        umls_dict[line.split("|")[0]+"_"+line.split("|")[1]+"_"+line.split("|")[2] ] = None
    print("total valid and unique umls_relations: "+str(len(umls_dict)))
    return umls_dict


def Relationshipcreation(umls_dict):
    """

    :param umls_dict:
    :return: a file name relation attributes in a format of : :START_ID,:END_ID,:TYPE,RelationLabel,weight
    """
    f_out_final = open("relation", 'w')
    with codecs.open(sys.argv[2],'r') as mrrel:
    #with open ('MRREL.txt','r') as mrrel:
        for i,line in enumerate(mrrel) :
            if ((line.split("|")[0]!= line.split("|")[4]) and (line.split("|")[10] != "TKMT" ) ):
                value = line.split("|")[3]+"_"+line.split("|")[10]+"_"+line.split("|")[7]
                if value in  umls_dict:
                    #print(line.split("|")[0]+","+line.split("|")[4]+","+line.split("|")[3]+"_"+line.split("|")[7]+","+1)
                    f_out_final.write(line.split("|")[0]+","+line.split("|")[4]+","+line.split("|")[10]+"," +line.split("|")[3]+"_"+line.split("|")[7]+","+str(1) + "\n")
    print("Relation file created!")
def nodecreation():
    """

    :return: a file name relation attributes in a format of : :ID,ConceptID,ConceptName
    """
    #node = open('MRCONSO.txt', encoding='utf8')
    node = codecs.open(sys.argv[3], encoding='utf8')
    node_dict = {}
    for i, line in enumerate(node) :
        line = re.sub("\n","",line)
        #0,1,6,11,14  C0000005|ENG|Y|MSH|(131)I-Macroaggregated Albumin|0|N|256|

        if (line.split("|")[1]=="ENG" and line.split("|")[6] == "Y" ):
            k = line.split("|")[0].lstrip().rstrip()
            if k not in node_dict:
                #print(k+"::"+line.split("|")[14].lstrip().rstrip().replace(",", "_"))
                node_dict[k] = line.split("|")[14].lstrip().rstrip()


    f_out_final = open("node", 'w')
    for k, v in node_dict.items():
        v = v.replace(",", "")
        v = re.sub('\W+', '_',v)
        f_out_final.write(k.split("_")[0].lstrip().rstrip()+","+k.split("_")[0].lstrip().rstrip()+","+v.lstrip().rstrip() + "\n")
    print("Node file created!")
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script creates a node and relation file, used for creating DB')
    parser.add_argument('UMLS_relation', metavar='UMLS_relation', type= str, nargs='+',
                        help='path of the UMLS_relation file, if not current directory')

    parser.add_argument('MRREL', metavar='MRREL', type=str, nargs='+',
                        help='path of the MRREL.RRF file, if not current directory')

    parser.add_argument('MRCONSO', metavar='MRCONSO', type=str, nargs='+',
                        help='path of the MRCONSO.RRf file, if not current directory')


    args = parser.parse_args()

    processfile()
    umls_dict = CreateDictionary()
    Relationshipcreation(umls_dict)
    nodecreation()
