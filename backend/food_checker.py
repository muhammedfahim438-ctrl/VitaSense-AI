# ══════════════════════════════════════════════════════════════
# VitaSense AI - Food Safety Checker for Diabetics
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# ══════════════════════════════════════════════════════════════

# ── FOOD DATABASE ─────────────────────────────────────────────
# GI = Glycemic Index (how fast food raises blood sugar)
#      Low GI  = below 55  (safe for diabetics)
#      Med GI  = 56 to 69  (moderate, eat in small portions)
#      High GI = 70+       (avoid or limit)
#
# GL = Glycemic Load (GI x carbs / 100)
#      Low GL  = below 10  (safe)
#      Med GL  = 11 to 19  (moderate)
#      High GL = 20+       (avoid)
# ──────────────────────────────────────────────────────────────

FOOD_DATABASE = {

    # ── GRAINS & RICE ─────────────────────────────────────────
    'white rice':       {'gi':72, 'gl':29, 'carbs':28, 'calories':130,
                         'category':'Grains',
                         'status':'avoid',
                         'alternatives':['brown rice','cauliflower rice','quinoa'],
                         'portion':'If eaten, limit to 1/4 cup cooked'},
    'brown rice':       {'gi':50, 'gl':16, 'carbs':23, 'calories':112,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['quinoa','barley','oats'],
                         'portion':'Limit to 1/2 cup cooked per meal'},
    'white bread':      {'gi':75, 'gl':20, 'carbs':15, 'calories':79,
                         'category':'Grains',
                         'status':'avoid',
                         'alternatives':['whole wheat bread','rye bread','multigrain bread'],
                         'portion':'Avoid or limit to 1 small slice'},
    'whole wheat bread':{'gi':52, 'gl':12, 'carbs':12, 'calories':69,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['rye bread','sourdough','oat bread'],
                         'portion':'1 slice per meal is acceptable'},
    'chapati':          {'gi':52, 'gl':14, 'carbs':18, 'calories':104,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['jowar roti','bajra roti','ragi roti'],
                         'portion':'1 small chapati per meal'},
    'roti':             {'gi':52, 'gl':14, 'carbs':18, 'calories':104,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['jowar roti','bajra roti','ragi roti'],
                         'portion':'1 small roti per meal'},
    'oats':             {'gi':55, 'gl':13, 'carbs':27, 'calories':150,
                         'category':'Grains',
                         'status':'safe',
                         'alternatives':['steel cut oats are even better'],
                         'portion':'1/2 cup cooked — ideal breakfast'},
    'quinoa':           {'gi':53, 'gl':13, 'carbs':21, 'calories':120,
                         'category':'Grains',
                         'status':'safe',
                         'alternatives':['barley','bulgur wheat'],
                         'portion':'1/2 cup cooked per meal'},
    'barley':           {'gi':28, 'gl':12, 'carbs':44, 'calories':193,
                         'category':'Grains',
                         'status':'safe',
                         'alternatives':['quinoa','oats'],
                         'portion':'1/2 cup cooked — great for diabetics'},
    'maida':            {'gi':85, 'gl':33, 'carbs':76, 'calories':364,
                         'category':'Grains',
                         'status':'avoid',
                         'alternatives':['whole wheat flour','almond flour','ragi flour'],
                         'portion':'Avoid completely'},
    'idli':             {'gi':69, 'gl':23, 'carbs':39, 'calories':156,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['ragi idli','oats idli'],
                         'portion':'2 small idlis maximum per meal'},
    'dosa':             {'gi':69, 'gl':25, 'carbs':40, 'calories':168,
                         'category':'Grains',
                         'status':'moderate',
                         'alternatives':['ragi dosa','oats dosa','moong dosa'],
                         'portion':'1 small plain dosa per meal'},

    # ── VEGETABLES ────────────────────────────────────────────
    'broccoli':         {'gi':10, 'gl':1, 'carbs':7, 'calories':34,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['cauliflower','spinach','kale'],
                         'portion':'Unlimited — excellent for diabetics'},
    'spinach':          {'gi':15, 'gl':1, 'carbs':4, 'calories':23,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['kale','lettuce','methi'],
                         'portion':'Unlimited — very beneficial'},
    'carrot':           {'gi':39, 'gl':2, 'carbs':10, 'calories':41,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['beetroot in moderation'],
                         'portion':'1 medium carrot per day is fine'},
    'potato':           {'gi':78, 'gl':28, 'carbs':37, 'calories':164,
                         'category':'Vegetables',
                         'status':'avoid',
                         'alternatives':['sweet potato','cauliflower','turnip'],
                         'portion':'Avoid or limit to very small portions'},
    'sweet potato':     {'gi':54, 'gl':11, 'carbs':27, 'calories':112,
                         'category':'Vegetables',
                         'status':'moderate',
                         'alternatives':['regular potato has higher GI'],
                         'portion':'Half a medium sweet potato per meal'},
    'tomato':           {'gi':15, 'gl':1, 'carbs':4, 'calories':18,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['all vegetables with low GI are good'],
                         'portion':'Unlimited — great for diabetics'},
    'cucumber':         {'gi':15, 'gl':1, 'carbs':4, 'calories':16,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['zucchini','celery'],
                         'portion':'Unlimited — ideal snack for diabetics'},
    'bitter gourd':     {'gi':20, 'gl':1, 'carbs':4, 'calories':17,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['karela juice is also beneficial'],
                         'portion':'Excellent for diabetics — eat freely'},
    'karela':           {'gi':20, 'gl':1, 'carbs':4, 'calories':17,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['bitter gourd juice'],
                         'portion':'Highly recommended for diabetics'},
    'ladies finger':    {'gi':20, 'gl':1, 'carbs':7, 'calories':33,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['bitter gourd','methi'],
                         'portion':'Excellent for blood sugar control'},
    'okra':             {'gi':20, 'gl':1, 'carbs':7, 'calories':33,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['ladies finger is same food'],
                         'portion':'Excellent for blood sugar control'},
    'onion':            {'gi':10, 'gl':1, 'carbs':9, 'calories':40,
                         'category':'Vegetables',
                         'status':'safe',
                         'alternatives':['garlic also beneficial'],
                         'portion':'Use freely in cooking'},

    # ── FRUITS ────────────────────────────────────────────────
    'apple':            {'gi':36, 'gl':6, 'carbs':25, 'calories':95,
                         'category':'Fruits',
                         'status':'safe',
                         'alternatives':['pear','guava','berries'],
                         'portion':'1 small apple per day is fine'},
    'banana':           {'gi':51, 'gl':13, 'carbs':27, 'calories':105,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['apple','guava','papaya'],
                         'portion':'Half a small banana only — limit intake'},
    'mango':            {'gi':51, 'gl':8, 'carbs':25, 'calories':99,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['guava','papaya','apple'],
                         'portion':'2-3 small slices only — high in sugar'},
    'grapes':           {'gi':59, 'gl':11, 'carbs':18, 'calories':69,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['berries','apple','pear'],
                         'portion':'Small handful (10-15 grapes) only'},
    'watermelon':       {'gi':72, 'gl':4, 'carbs':8, 'calories':30,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['cucumber','muskmelon'],
                         'portion':'Small slice only due to high GI'},
    'orange':           {'gi':43, 'gl':5, 'carbs':12, 'calories':47,
                         'category':'Fruits',
                         'status':'safe',
                         'alternatives':['guava','apple','pear'],
                         'portion':'1 medium orange per day is fine'},
    'guava':            {'gi':12, 'gl':1, 'carbs':14, 'calories':68,
                         'category':'Fruits',
                         'status':'safe',
                         'alternatives':['apple','pear','berries'],
                         'portion':'Excellent for diabetics — 1 guava daily'},
    'papaya':           {'gi':60, 'gl':7, 'carbs':11, 'calories':43,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['guava','apple','pear'],
                         'portion':'Small portion — beneficial but moderate GI'},
    'strawberry':       {'gi':40, 'gl':1, 'carbs':8, 'calories':32,
                         'category':'Fruits',
                         'status':'safe',
                         'alternatives':['blueberry','raspberry','blackberry'],
                         'portion':'1 cup per day — great for diabetics'},
    'blueberry':        {'gi':53, 'gl':6, 'carbs':21, 'calories':84,
                         'category':'Fruits',
                         'status':'safe',
                         'alternatives':['strawberry','raspberry'],
                         'portion':'1/2 cup per day recommended'},
    'pineapple':        {'gi':59, 'gl':7, 'carbs':13, 'calories':50,
                         'category':'Fruits',
                         'status':'moderate',
                         'alternatives':['guava','apple','orange'],
                         'portion':'Small portion only — moderate GI'},

    # ── DAIRY ─────────────────────────────────────────────────
    'milk':             {'gi':31, 'gl':4, 'carbs':12, 'calories':150,
                         'category':'Dairy',
                         'status':'safe',
                         'alternatives':['low fat milk','almond milk','soy milk'],
                         'portion':'1 cup per day — choose low fat'},
    'curd':             {'gi':36, 'gl':3, 'carbs':6, 'calories':100,
                         'category':'Dairy',
                         'status':'safe',
                         'alternatives':['greek yogurt','buttermilk'],
                         'portion':'1 cup per day — probiotic benefits'},
    'yogurt':           {'gi':36, 'gl':3, 'carbs':6, 'calories':100,
                         'category':'Dairy',
                         'status':'safe',
                         'alternatives':['greek yogurt is better','curd'],
                         'portion':'1 cup plain yogurt per day'},
    'paneer':           {'gi':27, 'gl':1, 'carbs':4, 'calories':265,
                         'category':'Dairy',
                         'status':'safe',
                         'alternatives':['tofu','low fat paneer'],
                         'portion':'100g per day — good protein source'},
    'cheese':           {'gi':0, 'gl':0, 'carbs':1, 'calories':400,
                         'category':'Dairy',
                         'status':'moderate',
                         'alternatives':['low fat cheese','paneer'],
                         'portion':'Small amounts only due to high fat'},
    'butter':           {'gi':0, 'gl':0, 'carbs':0, 'calories':717,
                         'category':'Dairy',
                         'status':'moderate',
                         'alternatives':['olive oil','ghee in small amounts'],
                         'portion':'Very small amounts only'},
    'ice cream':        {'gi':57, 'gl':6, 'carbs':28, 'calories':207,
                         'category':'Dairy',
                         'status':'avoid',
                         'alternatives':['frozen yogurt','fruit sorbet','dark chocolate'],
                         'portion':'Avoid — high sugar and fat content'},

    # ── PROTEINS ──────────────────────────────────────────────
    'egg':              {'gi':0, 'gl':0, 'carbs':1, 'calories':155,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['egg whites are even better'],
                         'portion':'2 eggs per day is recommended'},
    'chicken':          {'gi':0, 'gl':0, 'carbs':0, 'calories':165,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['fish','turkey','tofu'],
                         'portion':'100-150g grilled or boiled per meal'},
    'fish':             {'gi':0, 'gl':0, 'carbs':0, 'calories':136,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['salmon is best for omega 3'],
                         'portion':'150-200g per meal — excellent choice'},
    'dal':              {'gi':29, 'gl':5, 'carbs':20, 'calories':116,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['moong dal','masoor dal','chana dal'],
                         'portion':'1 cup cooked per meal — great for diabetics'},
    'lentils':          {'gi':29, 'gl':5, 'carbs':20, 'calories':116,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['beans','chickpeas','moong'],
                         'portion':'1 cup cooked per meal'},
    'chickpeas':        {'gi':28, 'gl':8, 'carbs':27, 'calories':164,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['kidney beans','black beans','lentils'],
                         'portion':'1/2 cup cooked per meal'},
    'tofu':             {'gi':15, 'gl':1, 'carbs':2, 'calories':76,
                         'category':'Protein',
                         'status':'safe',
                         'alternatives':['paneer','tempeh'],
                         'portion':'100-150g per meal — excellent protein'},

    # ── BEVERAGES ─────────────────────────────────────────────
    'water':            {'gi':0, 'gl':0, 'carbs':0, 'calories':0,
                         'category':'Beverages',
                         'status':'safe',
                         'alternatives':['lemon water','infused water'],
                         'portion':'8-10 glasses per day — most important!'},
    'green tea':        {'gi':0, 'gl':0, 'carbs':0, 'calories':2,
                         'category':'Beverages',
                         'status':'safe',
                         'alternatives':['black tea without sugar','herbal tea'],
                         'portion':'2-3 cups per day — helps blood sugar'},
    'coffee':           {'gi':0, 'gl':0, 'carbs':0, 'calories':2,
                         'category':'Beverages',
                         'status':'safe',
                         'alternatives':['black coffee without sugar is best'],
                         'portion':'1-2 cups per day without sugar or milk'},
    'fruit juice':      {'gi':65, 'gl':15, 'carbs':26, 'calories':110,
                         'category':'Beverages',
                         'status':'avoid',
                         'alternatives':['eat whole fruits instead','water','green tea'],
                         'portion':'Avoid — eat whole fruits instead of juice'},
    'soft drink':       {'gi':63, 'gl':16, 'carbs':39, 'calories':150,
                         'category':'Beverages',
                         'status':'avoid',
                         'alternatives':['water','green tea','lemon water'],
                         'portion':'Avoid completely'},
    'cola':             {'gi':63, 'gl':16, 'carbs':39, 'calories':150,
                         'category':'Beverages',
                         'status':'avoid',
                         'alternatives':['water','sparkling water','green tea'],
                         'portion':'Avoid completely — very high sugar'},

    # ── SWEETS & SNACKS ───────────────────────────────────────
    'sugar':            {'gi':65, 'gl':7, 'carbs':100, 'calories':387,
                         'category':'Sweets',
                         'status':'avoid',
                         'alternatives':['stevia','jaggery in small amounts'],
                         'portion':'Avoid completely or use substitutes'},
    'jaggery':          {'gi':84, 'gl':10, 'carbs':98, 'calories':383,
                         'category':'Sweets',
                         'status':'avoid',
                         'alternatives':['stevia','dates in small amounts'],
                         'portion':'Avoid — high GI despite being natural'},
    'honey':            {'gi':58, 'gl':11, 'carbs':82, 'calories':304,
                         'category':'Sweets',
                         'status':'moderate',
                         'alternatives':['stevia','very small amount of honey'],
                         'portion':'Very small amounts only — 1 teaspoon max'},
    'dark chocolate':   {'gi':23, 'gl':6, 'carbs':46, 'calories':546,
                         'category':'Sweets',
                         'status':'moderate',
                         'alternatives':['70% or higher cocoa is best'],
                         'portion':'1-2 small squares per day acceptable'},
    'nuts':             {'gi':15, 'gl':1, 'carbs':6, 'calories':607,
                         'category':'Snacks',
                         'status':'safe',
                         'alternatives':['almonds, walnuts, pistachios are best'],
                         'portion':'Small handful (30g) per day — great snack'},
    'almonds':          {'gi':0, 'gl':0, 'carbs':22, 'calories':579,
                         'category':'Snacks',
                         'status':'safe',
                         'alternatives':['walnuts','pistachios','cashews in moderation'],
                         'portion':'10-15 almonds per day — excellent for diabetics'},
    'walnuts':          {'gi':15, 'gl':1, 'carbs':14, 'calories':654,
                         'category':'Snacks',
                         'status':'safe',
                         'alternatives':['almonds','flaxseeds'],
                         'portion':'5-7 walnuts per day — omega 3 benefits'},
    'biscuit':          {'gi':70, 'gl':10, 'carbs':65, 'calories':422,
                         'category':'Snacks',
                         'status':'avoid',
                         'alternatives':['nuts','seeds','whole grain crackers'],
                         'portion':'Avoid — high GI and refined flour'},
    'samosa':           {'gi':55, 'gl':17, 'carbs':28, 'calories':262,
                         'category':'Snacks',
                         'status':'avoid',
                         'alternatives':['roasted chana','nuts','vegetables'],
                         'portion':'Avoid — deep fried and high carb'},
}

# ── STATUS COLORS ─────────────────────────────────────────────
STATUS_INFO = {
    'safe':     {'color': '#10B981', 'label': 'Safe for Diabetics',    'emoji': '✅'},
    'moderate': {'color': '#F59E0B', 'label': 'Eat in Moderation',     'emoji': '⚠️'},
    'avoid':    {'color': '#EF4444', 'label': 'Avoid / Limit',         'emoji': '❌'},
}

# ══════════════════════════════════════════════════════════════
# MAIN FUNCTION — CHECK FOOD SAFETY
# ══════════════════════════════════════════════════════════════
def check_food(food_name):
    """
    Takes a food name and returns safety info for diabetics.
    """
    if not food_name:
        return {'status': 'error', 'message': 'Please enter a food name'}

    # Normalize input
    food_key = food_name.strip().lower()

    # Direct match
    if food_key in FOOD_DATABASE:
        food = FOOD_DATABASE[food_key]
        status_info = STATUS_INFO[food['status']]
        return {
            'status':       'success',
            'food_name':    food_name.title(),
            'found':        True,
            'gi':           food['gi'],
            'gl':           food['gl'],
            'carbs':        food['carbs'],
            'calories':     food['calories'],
            'category':     food['category'],
            'safety':       food['status'],
            'safety_label': status_info['label'],
            'safety_color': status_info['color'],
            'safety_emoji': status_info['emoji'],
            'alternatives': food['alternatives'],
            'portion':      food['portion'],
            'gi_category':  get_gi_category(food['gi']),
        }

    # Partial match
    for key, food in FOOD_DATABASE.items():
        if food_key in key or key in food_key:
            status_info = STATUS_INFO[food['status']]
            return {
                'status':       'success',
                'food_name':    food_name.title(),
                'found':        True,
                'gi':           food['gi'],
                'gl':           food['gl'],
                'carbs':        food['carbs'],
                'calories':     food['calories'],
                'category':     food['category'],
                'safety':       food['status'],
                'safety_label': status_info['label'],
                'safety_color': status_info['color'],
                'safety_emoji': status_info['emoji'],
                'alternatives': food['alternatives'],
                'portion':      food['portion'],
                'gi_category':  get_gi_category(food['gi']),
            }

    # Not found
    return {
        'status':    'success',
        'food_name': food_name.title(),
        'found':     False,
        'message':   f'Sorry, {food_name} is not in our database yet. '
                     f'As a general rule for diabetics: avoid high sugar '
                     f'and processed foods. Consult your doctor for specific advice.',
        'general_tips': [
            'Choose foods with low Glycemic Index (below 55)',
            'Avoid sugar, white rice, white bread and processed foods',
            'Prefer vegetables, whole grains, lean proteins and nuts',
            'Always check food labels for sugar and carb content',
            'Consult your dietitian for a personalized meal plan',
        ]
    }

def get_gi_category(gi):
    if gi == 0:
        return 'No GI (protein/fat)'
    elif gi < 55:
        return f'Low GI ({gi}) — Safe'
    elif gi < 70:
        return f'Medium GI ({gi}) — Moderate'
    else:
        return f'High GI ({gi}) — Avoid'

def get_all_safe_foods():
    return [k.title() for k,v in FOOD_DATABASE.items() if v['status']=='safe']

def get_all_avoid_foods():
    return [k.title() for k,v in FOOD_DATABASE.items() if v['status']=='avoid']

# ══════════════════════════════════════════════════════════════
# TEST
# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Testing food_checker.py...\n")
    test_foods = ['rice','apple','mango','broccoli','samosa','karela','unknown food']
    for food in test_foods:
        result = check_food(food)
        if result.get('found'):
            print(f"  {result['safety_emoji']} {food.title():<20} → {result['safety_label']:<25} GI:{result['gi']}")
        else:
            print(f"  ❓ {food.title():<20} → Not found in database")
    print(f"\n  Total foods in database : {len(FOOD_DATABASE)}")
    print(f"  Safe foods              : {len(get_all_safe_foods())}")
    print(f"  Avoid foods             : {len(get_all_avoid_foods())}")