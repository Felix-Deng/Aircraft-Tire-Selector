import requests 
import base64
from io import BytesIO
from PIL import Image as Image2

# Connect to Onshape 
API_ACCESS = ""
API_SECRET = ""

# Onshape document URL: https://cad.onshape.com/documents/81a21aba2821f554e5472fd7/w/6cd589ff79938fbd07f79634/e/5bccbe205d093a75bc04459b
DID = "81a21aba2821f554e5472fd7"
WID = "6cd589ff79938fbd07f79634"
EID = "5bccbe205d093a75bc04459b"

def get_shaded_view(_view_mat: str, _config="") -> str: 
    response = requests.get(
        "https://cad.onshape.com/api/partstudios/d/{}/w/{}/e/{}/shadedviews".format(
            DID, WID, EID
        ), 
        auth=(API_ACCESS, API_SECRET), 
        headers={
            "Accept": "application/json;charset=UTF-8; qs=0.09", 
            "Content-Type": "application/json"
        }, 
        params={
            "viewMatrix": _view_mat, 
            "outputHeight": 500, # default: 500
            "outputWidth": 500, # default: 500
            "pixelSize": 0,  # 0 will size the display to fit the output image dimensions
            "configuration": _config 
        }
    )
    if response.ok: 
        return response.json()['images'][0]
    else: 
        raise Exception("API call failed ...")


def get_frame(img_src: str) -> Image2.Image: 
    img_tmp = Image2.open(BytesIO(base64.b64decode(img_src)))
    alpha = img_tmp.getchannel('A')
    # Convert the image into P mode but only use 255 colors in the palette out of 256
    img_tmp = img_tmp.convert("RGB").convert(
        "P", palette=Image2.ADAPTIVE, colors=255
    )
    # Set all pixel values below 5 to 255 , and the rest to 0
    mask = Image2.eval(alpha, lambda a:255 if a <= 5 else 0)
    # Paste the color of index 255 and use alpha as a mask
    img_tmp.paste(255, mask)
    img_tmp.info['transparency'] = 255
    return img_tmp 


iso_view = str([
    0.707, 0.707, 0., 0., 
    -0.408, 0.408, 0.817, 0., 
    0.577, -0.577, 0.577, 0.
])[1:-1]

scopes = {
    "Dm": (12, 56), 
    "Wm": (4, 21), 
    "D": (4, 24), 
    "DF": (5, 33), 
    "PR": (4, 38)
}

Dm_hist = [15, 18, 22, 24, 32, 52]
Wm_hist = [6, 6.5, 6.6, 9.5, 9.75, 20.5] 
D_hist = [6, 8, 10, 10.5, 18, 20] 
DF_hist = [7.5, 9.75, 12, 12.25, 20.5, 23.75] 

imgs = [] # store images of each frame 

for i in range(len(Dm_hist)): 
    config = "Dm%3D{}%2Binch%3BWm%3D{}%2Binch%3BD%3D{}%2Binch%3BDF%3D{}%2Binch".format(
        Dm_hist[i], Wm_hist[i], D_hist[i], DF_hist[i]
    )
    img = get_shaded_view(iso_view, config)
    imgs.append(get_frame(img))
    
animation = BytesIO()
imgs[0].save(
    animation, "GIF", save_all=True, loop=0, append_images=imgs[1:], disposal=2, duration=500
)
with open('opt_animation.gif', 'wb') as f: 
    f.write(animation.getvalue())