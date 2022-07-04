import re

def ceklabelstres(labellist):
    label = ["Cemas","Rileks","Tegang","Tenang"]
    result_list = []
    for data in labellist:
        result_list.append(label[data])          
    return result_list


def ceklabelGSR(labellist):
    label = ['2-4','4-6','<2','>6']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelGSRintoModel(gsr):
    if gsr >= 2 and gsr < 4 :
        return 0
    elif gsr >= 4 and gsr < 6:
        return 1
    elif gsr < 2:
        return 2
    elif gsr > 6:
        return 3
    return -1

def ceklabelHR(labellist):
    label = ['60-70','70-90','90-100','>100']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelHRintoModel(hr):
    if hr >= 60 and hr < 70 :
        return 0
    elif hr >= 70 and hr < 90:
        return 1
    elif hr >= 90 and hr < 100:
        return 2
    elif hr >= 100:
        return 3
    return -1

def ceklabelBP(labellist):
    label = ['100/70-110/75','110/75-120/85','120/90-130/110','>130/110']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelBPintoModel(bp):
    Systolic_BP = int(re.sub(r'[/].*', '', bp))
    Diastolic_BP = int(re.sub(r'.*[/]', '', bp))


    if Systolic_BP >= 100 and Systolic_BP <= 110 and Diastolic_BP >= 70 and Diastolic_BP < 75:
        return 0
    elif Systolic_BP >= 110 and Systolic_BP <= 120 and Diastolic_BP >= 75 and Diastolic_BP < 85:
        return 1
    elif Systolic_BP >= 120 and Systolic_BP <= 130 and Diastolic_BP >= 90 and Diastolic_BP < 110:
        return 2
    elif Systolic_BP >= 130 and Diastolic_BP >= 110:
        return 3
    return -1

def ceklabelSUHU(labellist):
    label = ['33-35','35-36','36-37','<33']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelSUHUintoModel(suhu):
    if suhu >= 33 and suhu < 35 :
        return 0
    elif suhu >= 35 and suhu < 36:
        return 1
    elif suhu >= 36 and suhu < 37:
        return 2
    elif suhu < 33:
        return 3
    return -1

def ceklabelRESPIRASI(labellist):
    label = ['16-18','19-20','>20']
    result_list = []
    for data in labellist:
        result_list.append(label[data])
    return result_list

def ceklabelRESPIRASIintoModel(respirasi):
    if respirasi >= 16 and respirasi < 18 :
        return 0
    elif respirasi >= 19 and respirasi < 20:
        return 1
    elif respirasi >= 20:
        return 2
    return -1

