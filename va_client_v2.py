import jwt
import json
import requests
from datetime import datetime



class VAPlatformClient:

	def __init__(self, url, accessKey, secretKey):
		self.__url = url
		self.__token = ''
		self.__accessKey = accessKey
		self.__secretKey = secretKey
		self.__identity = "identity"
		self.__vaPlatform = "va-platform"

	def __is_token_expired(self):
		try:
			payload = jwt.decode(self.__token, verify=False)
			if (payload.get('exp') <= datetime.now().timestamp()):
				return True
			else:
				return False
		except:
			return True

	def __get_auth_headers(self, is_json_content=True):
		if self.__is_token_expired():
			
			result = requests.post(
				url=f'{self.__url}/{self.__identity}/api/v2/accounts/access/authentication',
				data=json.dumps({
					'accessKey': self.__accessKey,
					'secretKey': self.__secretKey
				}),
				headers={
					'Content-Type': 'application/json'
				}
			)
			self.__token = json.loads(result.content).get('token')
	

		if is_json_content:
			return {
				'Content-Type': 'application/json',
				'x-auth-token': self.__token
			}
		else:
			return { 'x-auth-token': self.__token }


	def get_cameras(self):
		print(f'{self.__url}/{self.__vaPlatform}/api/v2/cameras')
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/cameras', 
			headers=self.__get_auth_headers()
		)
		#print(result.content)
		#print(url)
		return json.loads(result.content)

	def get_dl_models(self):
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/dl-models', 
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def get_video_event_types(self):
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/video-event-types', 
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def get_video_alert_types(self):
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/video-alert-types', 
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def get_camera_stream_types(self):
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/camera-stream-types', 
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def get_camera_input_types(self):
		result = requests.get(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/camera-rtsp-input-types', 
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def create_video_event(self, data):
		result = requests.post(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/video-events',
			data=json.dumps(data),
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)

	def upload_video_event_file(self, file_name, file_path, mime_type):
		files = {'file': (file_name, open(file_path, 'rb'), mime_type)}
		result = requests.post(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/video-events/upload',
			files=files,
			headers=self.__get_auth_headers(is_json_content=False)
		)
		return json.loads(result.content)
	def  create_new_job(self,data1):
		result = requests.post(
			url='https://api.onstak.io/services/identity/api/v2/accounts/access/authentication',
			data=json.dumps({
				'accessKey': self.__accessKey,
				'secretKey': self.__secretKey,

			}),
			headers={
				'Content-Type': 'application/json'
			}
		)
		self.__token = json.loads(result.content).get('token')
		head = {'x-auth-token': self.__token, 'Content-Type': 'application/json'}

		result = requests.post(
			
			url='https://api.onstak.io/services/va-platform/api/v2/rois/query',
			headers=head,
			data= json.dumps(data1)
			
		)

		return json.loads(result.content)

	def send_job_status(self, data,job_status_id):


		result = requests.put(
			url=f'{self.__url}/{self.__vaPlatform}/api/v2/rois/'+str(job_status_id),
			data=json.dumps(data),
			headers=self.__get_auth_headers()
		)
		return json.loads(result.content)




		

		

		

