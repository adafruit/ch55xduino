import os
import json

thisScriptPath = os.path.dirname(os.path.realpath(__file__))
indexJsonPath = os.path.join(thisScriptPath, '../../../package_ch55xduino_mcs51_index.json')
#check if index.json exists
if not os.path.isfile(indexJsonPath):
    print('index.json not found, please run fetchForQingCloud.py first')
    exit(1)

neededUrlFiles = []

#parse index.json
with open(indexJsonPath, 'r') as f:
    indexJson = json.load(f)
    print('index.json loaded')
    versionsList = indexJson["packages"][0]["platforms"]
    #just keep the newest version (1st one)
    versionsList = [versionsList[0]]
    indexJson["packages"][0]["platforms"] = versionsList
    coreUrl = versionsList[0]["url"]
    neededUrlFiles.append(coreUrl)
    MCS51ToolsVersion = versionsList[0]["toolsDependencies"][0]["version"]
    sdccVersion = versionsList[0]["toolsDependencies"][1]["version"]
    toolsList = indexJson["packages"][0]["tools"]
    matchToolsList = []
    for tool in toolsList:
        if tool["name"] == "MCS51Tools":
            if tool["version"] == MCS51ToolsVersion:
                matchToolsList.append(tool)
        elif tool["name"] == "sdcc":
            if tool["version"] == sdccVersion:
                matchToolsList.append(tool)
    indexJson["packages"][0]["tools"]=matchToolsList
    for tool in matchToolsList:
        systemList = tool["systems"]
        for system in systemList:
            neededUrlFiles.append(system["url"])
    savePath = os.path.join(thisScriptPath, 'generatedFiles/package_ch55xduino_mcs51_index_newest.json')
    with open(savePath, 'w') as f:
        json.dump(indexJson, f, indent=4)
        print('index.json saved to {}'.format(savePath))

print(neededUrlFiles)
for url in neededUrlFiles:
    #download file into thisScriptPath/generatedFiles with wget
    savePath = os.path.join(thisScriptPath, 'generatedFiles', os.path.basename(url))
    if os.path.isfile(savePath):
        print('{} already exists, skip download'.format(savePath))
    else:
        os.system('wget -O {} {}'.format(savePath, url))

CorsQingCloudUrlPrefix = "https://ch55xduino.pek3b.qingstor.com/"

#iterate through indexJson and find all urls
def iterate_json(json_obj):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == "url":
                # if value.startswith(CorsQingCloudUrlPrefix):
                #     #replace url with local file path
                #     json_obj[key] = os.path.join(thisScriptPath, 'generatedFiles', os.path.basename(value))
                fileName = os.path.basename(value)
                json_obj["url"]=CorsQingCloudUrlPrefix+fileName
            else:
                iterate_json(value)
    elif isinstance(json_obj, list):
        for item in json_obj:
            iterate_json(item)
    else:
        # Do something with the value
        pass

iterate_json(indexJson)

savePath = os.path.join(thisScriptPath, 'generatedFiles/package_ch55xduino_mcs51_index_newest_qingcloud.json')
with open(savePath, 'w') as f:
    json.dump(indexJson, f, indent=4)
    print('index.json saved to {}'.format(savePath))
