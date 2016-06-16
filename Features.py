__author__ = 'alber_000'

def get_features(sentence, index, tag1, tag2):
    feature_set= {}
    word= sentence[index]
    ## Características de la propia palabra
    feature_set= {"word": word,
                  "1st previous tag": tag1,
                  "2nd previous tag": tag2}
    if len(word) == 1 :
        feature_set= {"preff(1)": word[0],
                      "suff(1)": word[0]}
    elif len(word) == 2 :
        feature_set= {"preff(1)": word[0],
                      "preff(2)": word[1:],
                      "suff(1)": word[-1:],
                      "suff(2)": word[-2:]}
    elif len(word) == 3 :
        feature_set= {"preff(1)": word[0],
                      "preff(2)": word[1:],
                      "preff(3)": word[2:],
                      "suff(1)": word[-1:],
                      "suff(2)": word[-2:],
                      "suff(3)": word[-3:]}
    elif len(word) == 4 :
        feature_set= {"preff(1)": word[0],
                      "preff(2)": word[1:],
                      "preff(3)": word[2:],
                      "preff(4)": word[3:],
                      "suff(1)": word[-1:],
                      "suff(2)": word[-2:],
                      "suff(3)": word[-3:],
                      "suff(4)": word[-4:]}
    return feature_set

