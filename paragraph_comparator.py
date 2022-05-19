import difflib
import re

def tokenize(s):
    return re.split('\s+', s)

def compare(s1, s2):

    s1 = tokenize(s1)
    s2 = tokenize(s2)
    matcher = difflib.SequenceMatcher(a=s1, b=s2)
    matches = matcher.get_matching_blocks()
    paraA = []
    paraB = []
    p1 = 0
    p2 = 0

    if(matches[0].a != p1):
        sent = " ".join(s1[p1:matches[0].a])
        paraA.append({"tkn":sent, "cl":"red"})
        p1 = matches[0].a


    if(matches[0].b != p2):
        sent = " ".join(s2[p2:matches[0].b])
        paraB.append({"tkn":sent, "cl":"red"})
        p2 = matches[0].b


    for index,match in enumerate(matches):
        if(match.size != 0):
            # for first para
            if(match.a == p1):
                sent = " ".join(s1[match.a:match.a+match.size])
                paraA.append({"tkn":sent, "cl":"gn"})
                p1 = match.a+match.size

                if(len(matches)-1 > index):
                    sent = " ".join(s1[p1:matches[index+1].a])
                    paraA.append({"tkn":sent, "cl":"rd"})
                    p1 = matches[index+1].a

            # for second para
            if(match.b == p2):
                sent = " ".join(s2[match.b:match.b+match.size])
                paraB.append({"tkn":sent, "cl":"gn"})
                p2 = match.b+match.size

                if(len(matches)-1 > index):
                    sent = " ".join(s2[p2:matches[index+1].b])
                    paraB.append({"tkn":sent, "cl":"rd"})
                    p2 = matches[index+1].b
                # print("Match             : {}".format(match))
                # print("Matching Sequence : {}".format(s1[match.a:match.a+match.size]))
    return {"p1":paraA, "p2":paraB}