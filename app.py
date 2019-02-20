import json
from PIL import Image

i = None

d = open("config.json", 'r')
data = json.load(d)

def setup_config():
	config = {}
	config["image"] = data["image"]
	config["image_size"] = data["image_size"]
	config["image_save_name"] = data["image_save_name"]
	if data["templates"] != None:
		config["parts"] = []
		for template_data in data["templates"]:
			r = open(template_data["path"],'r')
			template = json.load(r)
			parts = template["parts"]
			for part in parts:
				part["image"] = template_data["images"][part["image_loc"]]
				config["parts"].append(part)
	elif data["parts"] != None:
		config["parts"] = data["parts"]
	else:
		raise Exception("Invalid Config File")
	return config
			
config = setup_config()
image_size = (config["image_size"][0],config["image_size"][1])
if config["image"] == None:
	i = Image.new("RGBA",image_size,None)
else:
	i = Image.open(config["image"])
	i.mode = "RGBA"
i.load()

for part in config["parts"]:
	ci = Image.open(part["image"])
	copy_coords = (part["copy_area"][0],part["copy_area"][1],part["copy_area"][2],part["copy_area"][3])
	paste_coords = tuple()
	paste_coords = (int(part["paste_area"][0]),int(part["paste_area"][1]),int(part["paste_area"][2]),int(part["paste_area"][3]))
	crop = ci.crop(copy_coords)
	crop.load()
	crop.mode = 'RGBA'
	i.paste(crop,box=paste_coords)

i.save(config["image_save_name"])
