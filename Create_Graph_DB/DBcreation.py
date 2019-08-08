import operator
import re
import sys
import argparse
import codecs
import os

#python DBcreation.py 0 UMLS_relations.txt "../META/MRREL.RRF" "../MRCONSO.RRF"
#> go to UMLS_Analyse and solve remaining relations!
#python DBcreation.py 1 UMLS_relations.txt "../META/MRREL.RRF" "../META/MRCONSO.RRF"
# now remove redundant data:
# cat relation > tmp 
# cat tmp | sort | uniq > relation

def processfile():
    "Gets unique pair of vocab_RelationLabel_Relation and save it in a file called UMLS_final"
    f_out_final = open("UMLS_final", 'w')
    f2_out_final = open("UMLS_Analyse", 'w')
    cnt=0
    umls_rel={}
    #file = open("UMLS_relations.txt", encoding='utf8')
    file = codecs.open(args.UMLS_relation[0], encoding='utf8')
    for umls in file:
    #with open('UMLS_relations.txt', 'rb') as umls:

        umls = re.sub("\t","", umls)
        umls = re.sub("^ *", "", umls)
        umls = re.sub("\n", "", umls)
        umls = re.sub(" ", "|", umls)
        data=umls.split("|")

        nr=data[0]#
        reference = data[1]+"#"+data[3]
        rel=data[1]
        rela=data[2]

        if int(nr) > 50:
            # we don't want MDR and MSH from non English sources
            if not ( ( re.match("^MDR", data[3]) and len(data[3])>3 ) or ( re.match("^MSH", data[3]) and len(data[3])>3 ) or ( data[3] == "SCTSPA" ) ):
                # we accept only RO, RN or CHD relations -> beside CHD, RO and RN must have also a rela label
                if rel == "RO" or rel == "RN" or rel == "CHD":
                    if not (rela=="" and not (rel=="CHD" )):
                        # if not (rela=="" and not (rel=="CHD" or rel=="PAR")):
                        if nr not in umls_rel:
                            umls_rel[nr]={}

                        if reference not in umls_rel[nr]:
                            umls_rel[nr][reference]={}

                        umls_rel[nr][reference][rela]=0
    for numb in umls_rel.keys():
        for rel_lab in umls_rel[numb].keys():
            if len(umls_rel[numb][rel_lab])<=2:
                #print ("great!")
                tmp_str=re.sub("#", "|", rel_lab)
                f_out_final.write(tmp_str+"|"+list(umls_rel[numb][rel_lab].keys())[0]+"\n")
            else:
                f2_out_final.write("numb: "+ numb+" > "+ rel_lab+ " :: "+ str(umls_rel[numb][rel_lab])+"\n")
    if is_non_zero_file("UMLS_Analyse"):
        print("UMLS_final file created but there are content in UMLS_Analyse, run again after merging relations")
        return 1
    else:
        print("Complete UMLS_final file created")
        return 2

def is_non_zero_file(fpath):
      if  os.path.isfile(fpath) and os.stat(fpath).st_size >= 0 :
          return True
      else:
          return  False

def CreateDictionary():
    umls = codecs.open('UMLS_final',encoding='utf8')
    umls_dict = {}
    for line in umls:
        line = re.sub("\n","",line)
        umls_dict[line.split("|")[0]+"_"+line.split("|")[1]+"_"+line.split("|")[2] ] = None
    print("total valid and unique umls_relations: "+str(len(umls_dict)))
    return umls_dict


def Relationshipcreation(umls_dict, mrrel):
    """

    :param umls_dict:
    :return: a file name relation attributes in a format of : :START_ID,:END_ID,:TYPE,RelationLabel,weight
    """
    f_out_final = open("relation", 'w')
    with codecs.open(mrrel,'r') as mrrel:
    #with open ('MRREL.txt','r') as mrrel:
        for i,line in enumerate(mrrel) :
            if ((line.split("|")[0]!= line.split("|")[4]) and (line.split("|")[10] != "TKMT" ) ):
                value = line.split("|")[3]+"_"+line.split("|")[10]+"_"+line.split("|")[7]
                if value in  umls_dict:
                    #print(line.split("|")[0]+","+line.split("|")[4]+","+line.split("|")[3]+"_"+line.split("|")[7]+","+1)
                    f_out_final.write(line.split("|")[0]+","+line.split("|")[4]+","+line.split("|")[10]+"," +line.split("|")[10]+";"+line.split("|")[3]+";"+line.split("|")[7]+","+str(1) + "\n")
    print("Relation file created!")

def nodecreation(MRCONSO):
    """

       :return: a file name relation attributes in a format of : :ID,ConceptID,ConceptName
       """
    # node = open('MRCONSO.txt', encoding='utf8')
    node = codecs.open(MRCONSO, encoding='utf8')
    node_dict = {}
    for i, line in enumerate(node) :
        line = re.sub("\n","",line)
        #print(line.split("|"))  #0,1,6,11,14  C0000005|ENG|Y|MSH|(131)I-Macroaggregated Albumin|0|N|256|

        """if (line.split("|")[1]=="ENG" and line.split("|")[6] == "Y" ):
            k = line.split("|")[0].lstrip().rstrip()
            if k not in node_dict:
                print(k+"::"+line.split("|")[14].lstrip().rstrip().replace(",", "_"))
                node_dict[k] = line.split("|")[14].lstrip().rstrip()"""

        if (line.split("|")[1].lstrip().rstrip() == "ENG" and line.split("|")[6].lstrip().rstrip() == "Y"):
            cui = line.split("|")[0].lstrip().rstrip()
            node_name = line.split("|")[14].lstrip().rstrip().lower()
            node_name = node_name.replace(",", " ")
            #node_name = re.sub('\W+', ' ', node_name)
            if cui not in node_dict:
                node_dict[cui] = {}
            if node_name not in node_dict[cui]:
                node_dict[cui][node_name] = 1
            else :
                node_dict[cui][node_name] = node_dict[cui][node_name] + 1
    #sorted_x = []
    f_out_final = open("node", 'w')
    for cui in node_dict:
        #print(cui+"::"+sorted(node_dict[cui].items(), key=operator.itemgetter(1),reverse=True)[0][0] )
        label_name = sorted(node_dict[cui].items(), key=operator.itemgetter(1),reverse=True)[0][0]
        f_out_final.write(cui+","+cui+","+label_name + "\n")

    """f_out_final = open("node", 'w')
    for k, v in node_dict.items():
        #print(,v)
        #print(k.split[0]+","+k.split("_")[0]+","+v+","+k.split("_")[1])
        #break
        v = v.replace(",", "")
        v = re.sub('\W+', ' ',v)
        f_out_final.write(k.split("_")[0].lstrip().rstrip()+","+k.split("_")[0].lstrip().rstrip()+","+v.lstrip().rstrip() + "\n")"""


def runscript():
    umls_dict = CreateDictionary()
    Relationshipcreation(umls_dict, args.MRREL[0])
    nodecreation(args.MRCONSO[0])



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script creates a node and relation file, used for creating DB')
    parser.add_argument('Run',type=int,nargs='+',
                        help='Indicate whether it is first run(0) or running after analysing (1) , default is 0', default=0)
    parser.add_argument('UMLS_relation', metavar='UMLS_relation', type= str, nargs='+',
                        help='path of the UMLS_relation file, if not current directory')
    parser.add_argument('MRREL', metavar='MRREL', type=str, nargs='+',
                        help='path of the MRREL.RRF file, if not current directory')

    parser.add_argument('MRCONSO', metavar='MRCONSO', type=str, nargs='+',
                        help='path of the MRCONSO.RRf file, if not current directory')




    args = parser.parse_args()
    if args.Run[0] == 0:
        status = processfile()
        if status == 2:
            runscript()
        else :
            exit()

    elif args.Run[0] == 1:
        runscript()


