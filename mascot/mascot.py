import random
from mascot.comments import GOOD, BAD, NEUTRAL

def get_comment(eval_data):
    if eval_data["type"] == "cp":
        score = eval_data["value"]
        if score > 100:
            return random.choice(GOOD)
        elif score < -100:
            return random.choice(BAD)
        else:
            return random.choice(NEUTRAL)
    elif eval_data["type"] == "mate":
        if eval_data["value"] > 0:
            return "Şah çekiyorsun, galibiyet yakın! 😎"
        else:
            return "Dikkat! Mat oluyorsun 😨"
