# use this script to extract the bioprocess data


ann_path = "/Users/NidhiVyas/Documents/CMU-Spring2018/Semantics/BioProcess/bioprocess/dataset/enable_annotation/train/p120.ann"
sent_path = "/Users/NidhiVyas/Documents/CMU-Spring2018/Semantics/BioProcess/bioprocess/dataset/enable_annotation/train/p120.txt"
semantic_roles  = ["Agent", "Theme", "Source", "Dest", "Loc", "Result", "Other"]
triggers = ["Trigger", "Entity"]
# TODO: need to split on sentences, cant preprocess because the start and end position then need to be recalculated
# TODO: () creating an issue in token match, either inexact or without() should be matched


def ExtractTriggers(sentence, annotations, trigger_tokens):
    triggers, arguments = [], []
    triggers_helpers = []
    #tokens  = sentence # sentence in form of tokens
    type_role = annotations[1] # semantic role
    arg1, arg2  = annotations[2].split(':')[1], annotations[3].split(':')[1]
    cur_start = 0
    for token in sentence:
        token_temp = token.replace('.','').replace(',','').replace('\(','').replace('\)','')
        if (token_temp, arg1) in trigger_tokens:
            start = trigger_tokens[(token_temp, arg1)][0]
            end =  trigger_tokens[(token_temp, arg1)][1]
            #print start, end, cur_start
            if cur_start>=int(start) and cur_start<=int(end):
                triggers.append(1)
                triggers_helpers.append(1)
                #print token
        elif (token_temp, arg2) in trigger_tokens:
            start = trigger_tokens[(token_temp, arg2)][0]
            end =  trigger_tokens[(token_temp, arg2)][1]
            #print start, end, cur_start
            if cur_start>=int(start) and cur_start<=int(end):
                triggers.append(1)
                triggers_helpers.append(2)
                #print token
        else:
            triggers.append(0)
            triggers_helpers.append(0)
        cur_start+=len(token)+1 # current start position of the word

    return [s.replace('.','').replace(',','') for s in sentence], triggers, triggers_helpers

def ExtractRoles(triggers_helpers, annotations):
    argument_markers = []
    #print annotations, triggers_helpers

    for a in range(0,len(triggers_helpers)):
        if triggers_helpers[a]==0:
            argument_markers.append('O')
        if triggers_helpers[a]==1:
            if a!=0 and triggers_helpers[a-1]==1:
                argument_markers.append('1-I-'+annotations[1])
            else:
                argument_markers.append('1-B-'+annotations[1])
        if triggers_helpers[a]==2:
            if a!=0 and triggers_helpers[a-1]==2:
                argument_markers.append('2-I-'+annotations[1])
            else:
                argument_markers.append('2-B-'+annotations[1])
    #print argument_markers
    return argument_markers

def Extract(sent_path, ann_path):
    temp_return = []
    # each training example
    with open(ann_path, 'r') as rp:
        lines = rp.readlines()
    with open(sent_path, 'r') as sp:
        sent = sp.readlines()[0].split() # TODO: split on , and . too
    trigger_tokens = dict() # (actual word , trigger_ID ) => (start_ID, end_ID )

    for ann in lines:
        if ann.split()[1] in triggers:
            for a in ann.split()[4:]:
                trigger_tokens[a, ann.split()[0]] = (ann.split()[2], ann.split()[3])
        if ann.split()[1] in semantic_roles:
            sent_markers, trigger_markers, triggers_helpers = ExtractTriggers(sent, ann.split(), trigger_tokens)
            argument_markers = ExtractRoles(triggers_helpers, ann.split())
            temp_return.append((sent_markers, trigger_markers, argument_markers))
            # TODO: fix here, it should save for each
    return temp_return

#(sent_markers, trigger_markers, argument_markers) = Extract(sent_path, ann_path)


import os
base = "/Users/NidhiVyas/Documents/CMU-Spring2018/Semantics/BioProcess/bioprocess/dataset/enable_annotation/"
dir = ["test/", "train/"]
test = []
train  = []
for d in dir:
    path = base+d
    files = os.listdir(path)
    for i in range(250):
        if 'p'+str(i)+".txt" in files:
            file_txt = path+'p'+str(i)+".txt"
            file_ann = path+'p'+str(i)+".ann"
            temp_return = Extract(file_txt, file_ann)
            if d=="test/": test+=temp_return
            else: train+=temp_return
            print file_txt
print len(test)
print len(train)
#print train[0]
import pickle
with open('ProcessBank_train.p', 'wb') as handle:
    pickle.dump(train, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('ProcessBank_test.p', 'wb') as handle:
    pickle.dump(test, handle, protocol=pickle.HIGHEST_PROTOCOL)
print 'Done'
