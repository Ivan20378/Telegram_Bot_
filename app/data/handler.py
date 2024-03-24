import json

def get_wanderers(f_path:str = "app/data/wanderers.json") -> list:
    with open(f_path) as file:
        data = json.load(file)
        films = data.get("wanderers")
        return films

def get_wanderer(id:int=0, f_path:str = "app/data/wanderers.json") -> dict:
    return get_wanderers(f_path)[id]

def save_wanderer(wanderer:dict = {}, f_path:str = "app/data/wanderers.json") -> bool:
    with open(f_path) as file:
        data = json.load(file)
        films = data.get("wanderers")
        films.append(wanderer)
    with open(f_path, 'w') as file:
        json.dump(data, file, indent=4)
    return True

if __name__ == "__main__":
    print(get_wanderers())