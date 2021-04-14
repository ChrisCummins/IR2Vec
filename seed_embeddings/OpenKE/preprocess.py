# Copyright (c) 2021, S. VenkataKeerthy, Rohit Aggarwal
# Department of Computer Science and Engineering, IIT Hyderabad
#
# This software is available under the BSD 4-Clause License. Please see LICENSE
# file in the top-level directory for more details.
#
""" This script generates entity2id.txt, train2id.txt and relation2id.txt  """

# arg1 : path of the file generated by collectIR Pass

import re
import sys
import argparse
import os


def getEntityDict(config):
    ip = open(str(config.tripletFile), "r")
    content = ip.read()
    uniqueWords = sorted(set(content.split()))
    ip.close()

    op = open(os.path.join(config.preprocessed_dir, "entity2id.txt"), "w")
    i = 0
    entityDict = {}
    op.write(str(len(uniqueWords)) + "\n")
    for word in uniqueWords:
        op.write(str(word) + "\t" + str(i) + "\n")
        entityDict[str(word)] = str(i)
        i += 1
    op.close()
    return entityDict


def getRelationDict(config):
    ip = open(str(config.tripletFile), "r")
    content = ip.read()
    sentences = content.split("\n")
    maxLen = [len(sentence.strip().split("  ")) for sentence in sentences]
    maxArgs = max(maxLen) - 2
    ip.close()

    relationDict = {}

    op = open(os.path.join(config.preprocessed_dir, "relation2id.txt"), "w")
    op.write(str(maxArgs + 3) + "\n")
    relationDict["Type"] = "0"
    relationDict["Next"] = "1"

    op.write("Type	0\n")
    op.write("Next	1\n")
    for i in range(maxArgs):
        op.write("Arg" + str(i) + "\t" + str(i + 2) + "\n")
        relationDict["Arg" + str(i)] = str(i + 2)
    op.close()

    return relationDict


def createTrain2ID(ed, rd, config):
    ip = open(str(config.tripletFile), "r")
    content = ip.read()
    sentences = content.split("\n")

    op = open(os.path.join(config.preprocessed_dir, "train2id.txt"), "w")
    opc = ""
    toWrite = ""
    nol = 0
    for sentence in sentences:
        s = sentence.strip().split("  ")
        l = len(s)
        if s[0] != "":
            if opc != "":
                if s[0] not in ed:
                    print(sentence)
                    print(s)
                    print(l)
                    print(str(sentences.index(sentence)))
                    print(s[0] + " not found in ed")
                if "Next" not in rd:
                    print("Next not found in rd")
                toWrite += ed[opc] + "\t" + ed[s[0]] + "\t" + rd["Next"] + "\n"
                nol += 1
            opc = s[0]
            toWrite += ed[opc] + "\t" + ed[s[1]] + "\t" + rd["Type"] + "\n"
            nol += 1
            i = 0
            for arg in range(2, l):
                toWrite += (
                    ed[opc] + "\t" + ed[s[arg]] + "\t" + rd["Arg" + str(i)] + "\n"
                )
                nol += 1
                i += 1
    op.write(str(nol) + "\n")
    op.write(toWrite)
    op.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tripletFile",
        dest="tripletFile",
        metavar="FILE",
        help="Path of the triplet file generated by collectIR pass.",
        required=True,
    )
    parser.add_argument(
        "--preprocessed-dir",
        dest="preprocessed_dir",
        metavar="DIRECTORY",
        help="Path of the triplet file generated by collectIR pass.", default=None)
    config = parser.parse_args()
    if config.preprocessed_dir is None:
        config.preprocessed_dir = os.path.join(os.path.dirname(config.tripletFile), "preprocessed")
        i =0
        while os.path.exists(config.preprocessed_dir):
            i +=1
            config.preprocessed_dir = config.preprocessed_dir + str(i)
        os.makedirs(config.preprocessed_dir)
    ed = getEntityDict(config)
    rd = getRelationDict(config)
    createTrain2ID(ed, rd, config)

    print("Files are generated at the path ", config.preprocessed_dir)
