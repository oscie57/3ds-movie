import json, os
from flask import Flask, send_file, render_template, request

app = Flask(__name__)

def consolecheck(useragent):

    if "New Nintendo 3DS like iPhone" in useragent:
        console = "n3ds"
    elif "Nintendo WiiU" in useragent:
        console = "wiiu"
    elif "Nintendo 3DS" in useragent:
        console = "o3ds"
    elif "Nintendo DSi" in useragent:
        console = "ndsi"
    else:
        console = "unk"

    return console


def validitycheck():
    with open('list.json', 'r', encoding="utf-8") as f:
        file = json.load(f)

    for list in file['lists']:

        if 'title' not in file['lists'][list]:
            raise ValueError(f"Key 'title' not in '{list}'!")
        if 'description' not in file['lists'][list]:
            raise ValueError(f"Key 'description' not in '{list}'!")
        if 'folder' not in file['lists'][list]:
            raise ValueError(f"Key 'folder' not in '{list}'!")
        if 'type' not in file['lists'][list]:
            raise ValueError(f"Key 'type' not in '{list}'!")

        folder = file['lists'][list]['folder']
        if folder[3:][:-1] not in os.listdir(folder[:3]):
            raise ValueError(f"Folder '{folder}' found in '{list}' doesn't exist. ")


@app.route('/')
def main():
    useragent = request.headers.get('User-Agent')

    consoleraw = consolecheck(useragent)

    match consoleraw:
        case "n3ds":
            console = "a New Nintendo 3DS"
        case "wiiu":
            console = "a Nintendo Wii U"
        case "o3ds":
            console = "an Old Nintendo 3DS"
        case "ndsi":
            console = "a Nintendo DSi"
        case "unk":
            console = "an unknown device"
        case _:
            console = "_"

    return render_template('index.html', console=console)


@app.route('/list')
def list():
    with open('list.json', 'r', encoding="utf-8") as f:
        file = json.load(f)

    all_section = []

    for item in file['lists']:
        
        name = item

        title = file['lists'][item]['title']
        desc = file['lists'][item]['description']
        folder = file['lists'][item]['folder']
        type = file['lists'][item]['type']
        videos = 0
        
        for item in os.listdir(folder):
            videos += 1

        section = [name, title, desc, folder, type, videos]

        all_section.append(section)

    print(all_section)
    

    return render_template('list.html', data=all_section, datalen=len(all_section))


@app.route('/list/<list>')
def list2(list):

    with open('list.json', 'r', encoding='utf-8') as f:
        file = json.load(f)

    if list not in file['lists']:
        return render_template('error.html', error="Invalid list value.")

    name = list

    title = file['lists'][list]['title']
    desc = file['lists'][list]['description']
    folder = file['lists'][list]['folder']
    type = file['lists'][list]['type']

    videocount = 0
    videolist = []


    if type == "tv":
        return render_template('error.html', error="TV type is currently not supported.")

    for item in os.listdir(folder):
        videocount += 1
        videolist.append(item)



    all_section = [name, title, desc, folder, type, videocount, videolist]


    return render_template('list2.html', data=all_section)


@app.route('/list/<list>/file/<movie>')
def movie(list, movie):
    
    with open('list.json', 'r', encoding='utf-8') as f:
        file = json.load(f)

    folder = file['lists'][list]['folder']


    moviedir = folder + movie

    print(moviedir)

    return send_file(moviedir)

@app.route('/css/<sheet>.css')
def css(sheet):

    return send_file(f"./static/{sheet}.css")


if __name__ == '__main__':
    validitycheck()
    app.run("192.168.0.34", 81, debug=True)
