import pickle
import allennlp
import spacy, torch, numpy

# total data = 371696
# total train = 70% = 260187
# total dev = 15% =55754
# total test = 15% = 55754

with open("srl_data.p", 'rb') as dataFile:
    with open("train_wtriggers.txt", 'w') as trainp:
        with open("test_wtriggers.txt", 'w') as testp:
            with open("dev_wtriggers.txt", 'w') as devp:
                train, dev, test, l = 0,0,0, 0
                data = pickle.load(dataFile)
                for i in data:
                    l+=1
                    words, triggers, arguments = i[0], i[1], i[2]
                    index = 1
                    for w in range(len(words)):
                        s2w  = str(index)+" "+str(words[w])+" - "+str(triggers[w])+" "+str(arguments[w])+"\n"
                        index+=1
                        try:
                            if l%3==1 and dev<55754:
                                devp.write(s2w)
                            elif l%3==2 and test<55754:
                                testp.write(s2w)
                            else:
                                trainp.write(s2w)
                        except:
                            continue

                    if l%3==1 and dev<55754:
                        devp.write('\n')
                        dev+=1
                    elif l%3==2 and test<55754:
                        testp.write('\n')
                        test+=1
                    else:
                        trainp.write('\n')
                        train+=1

print(l, '= # total instances')
