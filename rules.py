# prediction mapping
# category

category_to_material = {
    "plastic_soda_bottles": "plastic",
    "plastic_water_bottles": "plastic",
    "plastic_detergent_bottles": "plastic",
    "plastic_beverage_bottles": "plastic",
    "plastic_food_containers": "plastic",
    "plastic_straws": "plastic",
    "plastic_cup_lids": "plastic",
    "plastic_shopping_bags": "plastic",
    "plastic_trash_bags": "plastic",
    "disposable_plastic_cutlery": "plastic",

    "glass_beverage_bottles": "glass",
    "glass_food_jars": "glass",
    "glass_cosmetic_containers": "glass",

    "steel_food_cans": "metal",
    "aluminum_food_cans": "metal",
    "aluminum_soda_cans": "metal",
    "aerosol_cans": "metal",

    "cardboard_boxes": "paper",
    "cardboard_packaging": "paper",
    "office_paper": "paper",
    "newspaper": "paper",
    "paper_cups": "paper",

    "styrofoam_cups": "styrofoam",
    "styrofoam_food_containers": "styrofoam",

    "food_waste": "organic",
    "coffee_grounds": "organic",
    "tea_bags": "organic",
    "eggshells": "organic",

    "clothing": "textile",
    "shoes": "textile"
}

#default recyclability state of the items:
material_defaults = {
    "plastic": True,
    "paper": True,
    "glass": True,
    "metal": True,
    "styrofoam": False,
    "organic": False,
    "textile": False,
    "unknown": False
}

#specific item overrides

item_override={
    "plastic_straws": False,
    "plastic_shopping_bags": False,
    "plastic_cup_lids": False,
    "plastic_trash_bags": False,
    "disposable_plastic_cutlery": False,
    "paper_cups": False,
    "tea_bags": False,
}

def get_material(category: str) -> str:
    return category_to_material.get(category, "unknown")

def recyclability(category: str) -> bool:
    if category in item_override:
        return item_override.get(category)
    else:
        material_type = get_material(category)
        return material_defaults.get(material_type, False)



## rule engine: to futher filter out items that are not dry,clean or rigid based on blue recyling bin rules
def rule_engine(category,is_clean,is_dry,is_rigid):
  recyclable=recyclability(category)

  material=get_material(category)

  if not is_clean:
    return{"Explanation":"residues can contaminate entire batches of recyclables"}

  if not is_dry:
    return{"Explanation":"Wet recyclables lower material recovery quality"}

  if material=="plastic" and not is_rigid:
    return{"Explanation":"Soft plastics such as bags,films and wrappers can become entangled in sorting machines"}

  if recyclable==False:
    return{"Explanation":f"{category} cannot be recylced in the Singapore Blue Bin"}

  elif recyclable==True:
    return{"Explanation":f"{category} can be recycled in the Singapore Blue Bin"}
