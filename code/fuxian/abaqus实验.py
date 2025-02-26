from abaqus import *
from abaqusConstants import *
from odbAccess import openOdb
import numpy as np

#这段代码是建立实验矩阵脚本
for i in range(1,35):
    mdb.models['Model-1'].loads['Load-1'].setValues(cf2=-i*20, 
    distributionType=UNIFORM, field='')
    for j in range(15,68):
        mdb.models['Model-1'].loads['Load-2'].setValues(cf2=-j*15, 
        distributionType=UNIFORM, field='')
        jobName = 'Job-'+str(i*20)+'-'+str(j*15)
        mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS, 
   	    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    	memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    	explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
   	    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
   	    scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
  	    multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
        mdb.jobs[jobName].submit(consistencyChecking=OFF)


#求某个为0时
mdb.models['Model-1'].loads['Load-2'].setValues(cf2=-0.0000001, 
    distributionType=UNIFORM, field='')
for j in range(1,51):
    mdb.models['Model-1'].loads['Load-1'].setValues(cf2=-j*20, 
    distributionType=UNIFORM, field='')
    jobName = 'Job-'+str(j*20)+'-'+str(0)
    mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS, 
   	atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
   	modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
   	scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
  	multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
    mdb.jobs[jobName].submit(consistencyChecking=OFF)


#这段代码是将文件夹里面的odb文件的数据提取出来为TXT文件：U
import os
import shutil
from abaqus import *
from abaqusConstants import *
from odbAccess import openOdb
import numpy as np
# 设置文件夹路径
input_folder = r"D:\A_happy_work_whole_life\abaques2023\temp\125data\ODB_700-1000#15-1005" # 输入文件夹路径
output_folder = r"D:\A_happy_work_whole_life\abaques2023\temp\125data\ODB_700-1000#15-1005_U"  # 输出文件夹路径
for file_name in os.listdir(input_folder):
    if file_name.endswith(".odb"):
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace(".odb", ".txt"))
        odb = openOdb(path=input_file_path)  
        for step_name in odb.steps.keys():
            current_step = odb.steps[step_name]  #获取当前的分析步
            #获取当前的分析步的最后一个frame中的位移数据
            displace_field = current_step.frames[-1].fieldOutputs["U"]
            #将位移数据写入txt文件
            with open(output_file_path, 'w') as file:
                file.write("nodeID, UMagnitude, U1, U2, U3 \n")
                for value in displace_field.values:
                    nodeID = value.nodeLabel
                    UMagnitude = np.linalg.norm(value.data)
                    U1 = value.data[0]
                    U2 = value.data[1]
                    U3 = value.data[2]
                    line = '{}, {}, {}, {}, {} \n'.format(nodeID, UMagnitude, U1, U2, U3)
                    file.write(line)
            odb.close()
            
 #这段代码是将文件夹里面的odb文件的数据提取出来为TXT文件：E           
import os
import shutil
from abaqus import *
from abaqusConstants import *
from odbAccess import openOdb
import numpy as np
# 设置文件夹路径
input_folder = r"D:\A_happy_work_whole_life\abaques2023\temp\125data\ODB_700-1000#15-1005" # 输入文件夹路径
output_folder = r"D:\A_happy_work_whole_life\abaques2023\temp\125data\ODB_700-1000#15-1005_E" # 输出文件夹路径
for file_name in os.listdir(input_folder):
    if file_name.endswith(".odb"):
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace(".odb", ".txt"))
        odb = openOdb(path=input_file_path)  
        for step_name in odb.steps.keys():
            current_step = odb.steps[step_name]  #获取当前的分析步
            #获取当前的分析步的最后一个frame中的ying数据
            E_field = current_step.frames[-1].fieldOutputs["E"]
            #将应变数据写入txt文件
            with open(output_file_path, 'w') as file:
                file.write("elementID, MISES \n")
                for value in E_field.values:
                    elementID = value.elementLabel
                    Mises = value.mises
                    line = '{}, {} \n'.format(elementID, Mises)
                    file.write(line)
            odb.close()
            
                          
output_folder = r"D:\A_happy_work_whole_life\abaques2023\temp\ODB_TXT_U"  # 输出文件夹路径            
input_file_path = r"D:\A_happy_work_whole_life\abaques2023\temp\ODB_DATA_ODB\Job-1-3.odb"
output_file_path = os.path.join(output_folder, file_name.replace(".odb", ".txt"))
job_name = file_name.replace(".odb", "")
odb = openOdb(path=input_file_path)        
for step_name in odb.steps.keys():
        current_step = odb.steps[step_name]
        displace_field = current_step.frames[-1].fieldOutputs["U"]
        with open(output_file_path, 'w') as file:
            file.write("nodeID, UMagnitude, U1, U2, U3 \n")
            for value in displace_field.values:
                nodeID = value.nodeLabel
                UMagnitude = np.linalg.norm(value.data)
                U1 = value.data[0]
                U2 = value.data[1]
                U3 = value.data[2]
                line = '{}, {}, {}, {}, {} \n'.format(nodeID, UMagnitude, U1, U2, U3)
                file.write(line)
odb.close()    

#单独实验代码 #改载荷cf2和改名字
mdb.models['Model-1'].loads['Load-1'].setValues(cf2=-600, 
    distributionType=UNIFORM, field='')
mdb.models['Model-1'].loads['Load-2'].setValues(cf2=-90, 
    distributionType=UNIFORM, field='')
jobName = 'Job-'+str(600)+'-'+str(90) #改名字
mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS, 
   	    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    	memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    	explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
   	    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
   	    scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
  	    multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
mdb.jobs[jobName].submit(consistencyChecking=OFF)