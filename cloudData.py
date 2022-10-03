import json
from va_client import VAPlatformClient
import constants

print('=======================================================')
print('Configure Authentication ==============================')
print('=======================================================')

with open(constants.TENNANT, 'r') as config_file:
	config_data = json.load(config_file)
	
client = VAPlatformClient(
		url=config_data['vaPlatformUrl'],
		accessKey=config_data['accessKey'],
		secretKey=config_data['secretKey']
)


def get_new_job_data (data):
	response = client.create_new_job(data)
	#print(response)
	response = response['data']

	#response = response[0]
	
	return response

def get_job_status(post_data,job_status_id):
	response = client.send_job_status(post_data,job_status_id)
	print("}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}","This is the reponse from post job api",response)
	
	


def get_cloud_data(camera_id,model_name) :  ## Get Camera ,Model Id , Object Type Id ,Event Type Id and Return Required Data


	with open(constants.TENNANT, 'r') as config_file:
		config_data = json.load(config_file)
	client = VAPlatformClient(
		url=config_data['vaPlatformUrl'],
		accessKey=config_data['accessKey'],
		secretKey=config_data['secretKey'])

	#print(client.get_cameras())
	cameras = client.get_cameras()
	
	data = cameras['data']
	#print(data)

	cameras_data = []
	#Use for-loops

	for dictionary in data:

		if (dictionary["id"] == camera_id):
			cameras_data.append(dictionary)
	 #[element for element in cameras_data if element['']]
	#print("Required camera:",cameras_data)
	for i in cameras_data:
		host = str(i["rtspHost"])
		port = str(i['rtspPort'])
		path = str(i['rtspPath'])
		user_name = str(i['rtspUsername'])
		user_password = str(i['rtspPassword'])
		camera_id = str(i['id'])
	#print("!!!!!!!!!!!! For Crowd Counting   !!!!!!!!!!!!!!",host,port,path,user_name,user_password)
	final_url = 'rtsp://'+user_name+':'+user_password+'@'+host+':'+str(port)+path
	#final_url = "rr"
	#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",final_url)
	print('=======================================================')
	print('Get Camera Feed =================================')
	print('=======================================================')

	#print("*"*10,"Cam URL:",final_url,"*"*10)

	print('=======================================================')
	print('Get Video Alert Types =================================')
	print('=======================================================')

	crowd_alert_types = client.get_video_alert_types()
	data = crowd_alert_types['data']
	
	#Social Distancing & camera id is 2

	crowd_alert_type_data = []
	#print("models name in video alert types api",data)

	for dictionary in data:

		if (dictionary["name"] == model_name):

			crowd_alert_type_data.append(dictionary)
	#print("Required video alert type data:",crowd_alert_type_data)

	for i in crowd_alert_type_data:
		crowd_alert_type_object = i["name"]
		alert_type_id = i['id']
	#print("*"*10,"Alert Type Id :",alert_type_id,"*"*10)

	print('=======================================================')
	print('Get Video Event Types =================================')
	print('=======================================================')

	#print(client.get_video_event_types())
	crowd_event_types = client.get_video_event_types()
	#print(video_alert_types)
	data = crowd_event_types['data']
	#print(data)
	#Social Distancing & camera id is 2

	crowd_event_type_data = []
	#Use for-loop

	for dictionary in data:
		if (dictionary["name"] == "Alert"):
			crowd_event_type_data.append(dictionary)
	 #[element for element in cameras_data if element['']]
	#print(crowd_event_type_data)

	for i in crowd_event_type_data:
		crowd_event_type_object = i["name"]
		event_type_id = i['id']
		#print("*"*10,"Event Type Id :",event_type_id,"*"*10)


	print('=======================================================')
	print('Get Model id =================================')
	print('=======================================================')

	response = client.get_dl_models()
	result = {}
	# print(response)
	for model in response:
		result[model['name']] = model['id']

	dl_model_id = result[model_name]
	#print("*"*10,"Dl Model Id :",dl_model_id,"*"*10)

	return alert_type_id,event_type_id,dl_model_id ,final_url , model_name,camera_id
