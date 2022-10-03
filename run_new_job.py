import json
import shutil
import uuid
import os, time
import subprocess
import argparse, logging.handlers
from cloudData import get_cloud_data , get_new_job_data , get_job_status


logging.basicConfig(filename="log.txt", level=logging.INFO,
							format="%(asctime)s %(message)s", filemode="w")
os.makedirs("new-job-run", exist_ok=True)

def start(args):

	update_roi_flag = {
		"pageSize": 100,
		"query": [
			{
				"action": "$eq",
				"name": "is_read",
				"value": 0
			}
		]
	}

	while True :
		try:
			time.sleep(0.03)
			response = get_new_job_data(update_roi_flag)
			time.sleep(0.03)
			
			print("*"*15,"New Job Data From Cloud","*"*15)
			logging.info("New Job Data From Cloud")
			print("*"*15,"*"*15)
			print("Response length  : ",len(response))

			if len(response) > 0 :
				for i in response :
					# print("*"*30,i,"*"*30)
					response = i
					if args.model_name == response['dl_model']['name'] or args.all_models:
						camera_id = response['cameraId']
						machine_id = response['edgeMachineId']
						roi_name = response['name']
						job_status_id = response['id']
						models = response['dl_model']
						model_name = models['name']
						model_id = models['id']
						roi_coordinates = response['roi_coordinates']
						object_type = response['objectType']
						object_count = response['count']
						machine_id = response['edgeMachineId']
						tenant_id = response['tenantId']

						print("*"*20,"This Data Get From Backend To Run The Job  ","*"*20)
						logging.info("This Data Get From Backend To Run The Job ")
						logging.info("dl model name : "+str(model_name))
						logging.info("dl model id :"+str(model_id))
						logging.info("camera Id :"+str(camera_id))
						logging.info("machine_id :"+str(machine_id))
						logging.info("Roi name :"+str(roi_name))

						multiple_roi = {}
						for dictionary in  roi_coordinates:
							roi_name = dictionary['name']
							pre_process_roi = dictionary['coordinates']
							final_roi = []
							for i in pre_process_roi:
								x = i['x']
								y= i['y']
								final_roi.append([x,y])
							multiple_roi[roi_name]=final_roi
						print('=======================================================')
						print('Get Data From Cloud And Store It =================================')

						logging.info('================ Get Data From Cloud And Store It =================================')

						print('=======================================================')
						print('=======================================================')
						print('Get Camera Url ,Model Id , Object Type Id ,Event Type Id , Final Url  =================================')

						logging.info('================ Get Camera Url ,Model Id , Object Type Id ,Event Type Id , Final Url  =================================')
						
						print('=======================================================')
						
						file_name = "new-job-run/"+model_name+'-'+'cam-id-'+str(camera_id)+'-data.json'
						file_name=file_name.replace(" ","")
						destination = 'dlmodels/'+model_name+'/'
						delete_file = destination+'/'+file_name
						
						if os.path.exists(file_name):
							print("*"*20,"remove exist json file","*"*20)
							logging.info("remove exist json file")
							logging.info(os.remove(file_name))
							os.remove(file_name)

						else:
							print("*"*20,"can not delete Json file because first time creation","*"*20)
							logging.info("can not delete Json file because first time creation")
						
						with open(file_name,"a+") as f:
							print("*"*20,"create  Json file to store the data","*"*20)
							
							logging.info("create  Json file to store the data")					
							
							alert_type_id,event_type_id,dl_model_id ,final_url,model_name,camera_id = get_cloud_data(camera_id=camera_id,model_name=model_name)
							
							required_data = {
							'model_name': model_name,
							"camera_id": camera_id,
							"dl_model_id": dl_model_id,
							"alert_type_id": alert_type_id ,
							"event_type_id": event_type_id,
							"final_url": final_url,
							"rois": multiple_roi,
							"object_type": object_type,
							"object_count" : object_count ,
							"machine_id" : machine_id ,
							"tenant_id" : tenant_id
							}

							print("*"*10,"This Data Store In  System ","*"*10)
							logging.info("This Data Store In  System ")

							logging.info(json.dump(required_data,f))

						job_info = 'camid:'+str(camera_id)+'-'+'modelname-'+model_name
						ouid1 = str(uuid.uuid4())
						job_status = {"jobId":str(ouid1), "jobInfo":job_info, "jobStatus":"running"}
						get_job_status(job_status,job_status_id)
					else:
						if args.all_models ==True:

							print("Found this model *{}* instead of *{}*:".format(response['dl_model']['name'],args.all_models))
							logging.info("Found this model *{}* instead of *{}*:".format(response['dl_model']['name'],args.all_models))
						else:
							print("Found this model *{}* instead of *{}*:".format(response['dl_model']['name'],args.model_name))
							logging.info("Found this model *{}* instead of *{}*:".format(response['dl_model']['name'],args.model_name))							
			else:
				continue
		except Exception as e:
			print("Exception states {} !".format(e))
			logging.info(e)
			continue

if __name__ == '__main__':
	par = argparse.ArgumentParser(description='Run new job for specific model.')
	par.add_argument('-m','--model_name',help='''--model_name="Social Distance". MODELS Names are : 
Mask Detection
, Social Distance
, Crowd
, Intrusion
, Facial Recognition
, Age & Gender
, Emotions
, Occupancy
, NLP
, Vehicles
, Weapon
, Pose Detection
, License Plates Recognition
, People Count
, Person Fall Detection
, Enter Exit
, Parking Slot
, Person  Detection
, Traffic Flow
, PPE
, Fire Detection
, Temperature Detection Smoke Detection ''')
	par.add_argument('-a','--all_models', default = False, action='store_true', dest="all_models", help = "To download all models")
	args = par.parse_args()
	start(args)
