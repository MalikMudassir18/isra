import json
from va_client_v2 import VAPlatformClient
import argparse
import pandas as pd
import constants

def start(cfg):

    with open(f'{cfg}', 'r') as config_file:
        config_data = json.load(config_file)
    client = VAPlatformClient(
        url=config_data['vaPlatformUrl'],
        accessKey=config_data['accessKey'],
        secretKey=config_data['secretKey']
    )
    cameras = client.get_cameras()
    model_data = client.get_dl_models()




    # print list of cameras names
    if thing == "camera":
        a = cameras['data']
        def cameras_list():
            
            for i in range(len(a)):
                print(a[i]['name'])
        if camera_list:
            cameras_list()





    # print all the informations about a single camera
        def get_camera_info(data):
            
            for i in range(len(a)):
                if a[i]["name"] == data:
                    print(a[i])

        if camera_info:
            print(camera_info)
            get_camera_info(camera_info[0])





    #create rtsp of a single camera
        def create_rtsp(cname):
            
            for i in range(len(a)):
                if a[i]['name'] ==cname:

                    host, port, path = str(a[i]["rtspHost"]), str(a[i]['rtspPort']), str(a[i]['rtspPath'])
                    user_name, user_password = str(a[i]['rtspUsername']), str(a[i]['rtspPassword'])
                    camera_id = str(a[i]['id'])
            final_url = 'rtsp://'+user_name+':'+user_password+'@'+host+':'+str(port)+path
            print(final_url)

        if rtsp:
            create_rtsp(rtsp[0])






        def create_camera_csv():
            
            alist = []
            rtsp_list = []
            for i in range(len(a)):
                alist.append(a[i].values())
                host, port, path, = str(a[i]["rtspHost"]), str(a[i]['rtspPort']),str(a[i]['rtspPath'])
                user_name, user_password = str(a[i]['rtspUsername']), str(a[i]['rtspPassword'])
                camera_id = str(a[i]['id'])
                final_url = 'rtsp://'+user_name+':'+user_password+'@'+host+':'+str(port)+path
                rtsp_list.append(final_url)

            df = pd.DataFrame(alist,columns = a[i].keys())
            df["Final_rtsp"] = rtsp_list
            df.to_csv("cameras_info.csv")
            print("*"*30, "CSV File naming cameras_info.csv has been created ","*"*30)
        if csv:
            create_camera_csv()




    elif thing == "model":
        def mod_list():
            for i in range(len(model_data)):
                print(model_data[i]['name'])

        if model_list:
            mod_list()
        def mod_info(data):
            
            for i in range(len(model_data)):
                if model_data[i]["name"] == data:
                    print(model_data[i])
        if model_info:
            mod_info(model_info[0])

        def create_models_csv():
            
            alist = []
            blist = []
            clist = []
            dlist = []
            for i in range(len(model_data)):
                alist.append(model_data[i].values())
                blist.append(model_data[i]["dlObjects"][0]["name"])
                clist.append(model_data[i]["dlObjects"][0]["attributes"][0]["key"])
                dlist.append(model_data[i]["dlObjects"][0]["attributes"][0]["values"])
            df = pd.DataFrame(alist,columns = model_data[i].keys())
            df["Category"] = blist
            df['key'] = clist
            df['values'] = dlist
            df.drop('dlObjects', inplace=True, axis=1)
            df.to_csv("models_info.csv")
            print("*"*30, "CSV File naming models_info.csv has been created ","*"*30)
        if model_csv:
            create_models_csv()
    else:
        print("Please enter any argument camera or models")






if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('-cfg', type=str, required=False, default=constants.TENNANT, help="enter the name of config.json file")

    subparsers = parser.add_subparsers(dest='thing')
    subparsers.required = False

    #Camera
    camera = subparsers.add_parser(name="camera")
    camera.add_argument("-camera_list", action="store_true", required=False, default=False)

    camera.add_argument('-camera_info', nargs="+", required=False, default="", dest = "camera_info")

    camera.add_argument('-rtsp', nargs="+",  required=False,  default="", dest ="rtsp")

    camera.add_argument("-camera_csv",required=False, action="store_true", default=False)

    #Model
    models = subparsers.add_parser(name="model")
    models.add_argument("-model_list", action="store_true", required=False, default=False)
    models.add_argument('-model_info', nargs="+", required=False, default="", dest = "model_info")
    models.add_argument("-model_csv",required=False, action="store_true", default=False)
    args = vars(parser.parse_args())
    cfg = args['cfg']
    

    thing = args["thing"]
    camera_list = None
    camera_info = None
    rtsp = None
    camera_csv = None

    model_list = None
    model_info = None
    model_csv = None





    if thing == 'camera':
        camera_list = args['camera_list']
        camera_info = args['camera_info']
        rtsp = args['rtsp']
        csv = args['camera_csv']


    if thing == "model":
        model_list = args['model_list']
        model_info = args["model_info"]
        model_csv = args["model_csv"]


    start(cfg)
