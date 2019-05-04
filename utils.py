# -*- coding: utf-8 -*-
"""
@author: Ulrich
"""

import torch
import numpy as np
import xlwt 

# define a function to plot confusion matrix
def confusion(sample_num, labels_num, label_pred, label):
    matrix = torch.zeros(labels_num, labels_num)
    _, target = torch.max(label, 1)
    for i in range(sample_num):
        actual_label = target[i]
        predicted_label = label_pred[i]

        matrix[actual_label][predicted_label] += 1

    return matrix

def F1_score(m):
    TP, FP, FN = [], [], []
    precision, recall, F1 = [], [], []
    m = m.data.numpy()
    
    TP.append(m[0][0])
    TP.append(m[0][1])
    TP.append(m[0][2])
    
    FP.append(m[1][0] + m[2][0])
    FP.append(m[1][1] + m[2][1])
    FP.append(m[1][2] + m[2][2])
    
    FN.append(m[0][1] + m[0][2])
    FN.append(m[1][0] + m[1][2])
    FN.append(m[2][0] + m[2][1])
    
    for i in range(3):    
        precision.append(TP[i] / (TP[i] + FP[i]))
        recall.append(TP[i] / (TP[i] + FN[i]))
        F1.append(2 * precision[i] * recall[i] / (precision[i] + recall[i]))
        
    print("Precision: {} ; \nAverage precision: {}".format(precision, np.mean(precision)))
    print("Recall: {} ; \nAverage recall: {}".format(recall, np.mean(recall)))
    print("F1 Score: {} ; \nAverage F1 Score: {}".format(F1, np.mean(F1)))
    
# Write matrix data into an excel file.
def saveExcel(data, path, sheet_num, fill_color=False):
    file = xlwt.Workbook()
    sheet1 = file.add_sheet(sheet_num, cell_overwrite_ok=True)
    
    # Color of cells.
    st = xlwt.easyxf('pattern: pattern solid;')
    st.pattern.pattern_fore_colour = 4
    
    [h, l] = data.shape
    for i in range(h):
        for j in range(l):
            if fill_color and (i != 0 and j!= 0 and i != j) and data[i, j] < 15:
                sheet1.write(i, j, data[i, j].item(), st)
            else:
                sheet1.write(i, j, data[i, j].item())
    file.save(path)

# The input vectors should be numpy vector form.
def vector_angle(vec1, vec2):
    list1 = vec1.data.numpy()
    list2 = vec2.data.numpy()

    val = np.dot(list1, list2) / np.linalg.norm(list1) / np.linalg.norm(list2)
    radian = np.arccos(val) # 0 - PI
    
    angle = radian * 180 / np.pi
    angle = np.nan_to_num(angle)

    return angle
    
def saveParas(model, input_data, vec_size):
    weight_mat = model.hidden.weight.data
    saveExcel(weight_mat, 'weight.xls', u'sheet1')

    a_hidden = model.getActivationVec(input_data)
    saveExcel(a_hidden[:,:] - 0.5, 'activation.xls', u'sheet1')
    
    vectorangle_mat = np.zeros((vec_size, vec_size))
    idx_list = list(range(1, vec_size))
    vectorangle_mat[0, 1:] = idx_list[:]
    vectorangle_mat[1: , 0] = idx_list[:]
    for i in idx_list:
        for j in idx_list:
            if i == j:
                vectorangle_mat[i][j] = 0
            else:
                vectorangle_mat[i][j] = vector_angle(a_hidden[:, i-1], a_hidden[:, j-1])
    saveExcel(vectorangle_mat, 'vector_angle.xls', u'sheet1', fill_color=True)
    
    print("Datas has been successfully saved in Excel files!")
    
    
    
