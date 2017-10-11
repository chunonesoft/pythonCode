#coding=utf-8

'''
TP：True Positive
FP: False Positive
TN: True Negative
FN: False Negative
识别率是分类器正确分类的样本数与总样本数之比
accuracy=(TP + TN)/(TP + TN + FP + FN)
'''
def calculate_accuracy(TP, TN, FP ,FN):
    accuracy = (TP + TN)/(TP + TN + FP + FN)
    return accuracy

'''
精确率分类为真实正例样本数与分类为正例样本数之比
precision = TP／(TP + FP)
'''
def calculate_precision(TP, FP):
    precision = TP/(TP + FP)
    return precision

'''
召回率分类为真实正例样本数与所有正例样本数之比
'''
def calculate_recall(TP, FN):
    recall = TP/(TP+FN)
    return recall
'''
F-score:识别率的延伸，结合了精确率和召回率
'''
def calculate_f_score(TP, FP, FN):
    precision = calculate_precision(TP, FP)
    recall = calculate_recall(TP, FN)
    f_score = 2*recall*precision/(recall + precision)
    return f_score
