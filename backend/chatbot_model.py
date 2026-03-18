# ══════════════════════════════════════════════════════════════
# VitaSense AI - Diabetes Chatbot
# Catalyst Crew | Nehru Arts and Science College, Coimbatore
# ══════════════════════════════════════════════════════════════

import re

# ══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — 50+ Diabetes Topics
# ══════════════════════════════════════════════════════════════
KNOWLEDGE_BASE = [

    # ── WHAT IS DIABETES ──────────────────────────────────────
    {
        'keywords': ['what is diabetes', 'define diabetes', 'diabetes meaning',
                     'explain diabetes', 'about diabetes'],
        'answer': """🩺 <b>What is Diabetes?</b><br><br>
Diabetes is a chronic condition where the body cannot properly regulate blood sugar (glucose) levels.<br><br>
<b>There are 3 main types:</b><br>
• <b>Type 1 Diabetes</b> — The immune system attacks insulin-producing cells. Requires insulin injections. Usually diagnosed in children and young adults.<br>
• <b>Type 2 Diabetes</b> — The body doesn't use insulin properly. Most common type (90% of cases). Linked to lifestyle factors.<br>
• <b>Gestational Diabetes</b> — Occurs during pregnancy. Usually resolves after birth but increases future risk.<br><br>
⚠️ <i>Always consult your doctor for proper diagnosis and treatment.</i>"""
    },

    # ── SYMPTOMS ──────────────────────────────────────────────
    {
        'keywords': ['symptoms', 'signs of diabetes', 'how do i know',
                     'diabetes symptoms', 'warning signs'],
        'answer': """🔍 <b>Common Diabetes Symptoms:</b><br><br>
<b>Early Warning Signs:</b><br>
• Frequent urination (especially at night)<br>
• Excessive thirst and dry mouth<br>
• Unexplained weight loss<br>
• Extreme fatigue and weakness<br>
• Blurry or impaired vision<br>
• Slow healing of cuts and wounds<br>
• Tingling or numbness in hands and feet<br>
• Frequent infections (skin, gum, bladder)<br>
• Dark patches on skin (neck, armpits)<br><br>
<b>Type 1 Specific:</b> Sudden onset, nausea, vomiting<br>
<b>Type 2 Specific:</b> Often no symptoms for years<br><br>
⚠️ <i>If you experience these symptoms, please consult a doctor immediately for proper testing.</i>"""
    },

    # ── NORMAL BLOOD SUGAR LEVELS ─────────────────────────────
    {
        'keywords': ['normal blood sugar', 'normal glucose', 'blood sugar levels',
                     'glucose levels', 'sugar range', 'normal range',
                     'fasting sugar', 'pp sugar'],
        'answer': """📊 <b>Normal Blood Sugar Levels:</b><br><br>
<table style="width:100%;border-collapse:collapse;">
<tr style="background:#EFF6FF;"><th style="padding:8px;text-align:left;">Test</th><th style="padding:8px;">Normal</th><th style="padding:8px;">Prediabetes</th><th style="padding:8px;">Diabetes</th></tr>
<tr><td style="padding:8px;">Fasting (8hr fast)</td><td style="padding:8px;color:#10B981;">70–99</td><td style="padding:8px;color:#F59E0B;">100–125</td><td style="padding:8px;color:#EF4444;">126+</td></tr>
<tr style="background:#EFF6FF;"><td style="padding:8px;">After 2hr meal</td><td style="padding:8px;color:#10B981;">Below 140</td><td style="padding:8px;color:#F59E0B;">140–199</td><td style="padding:8px;color:#EF4444;">200+</td></tr>
<tr><td style="padding:8px;">Random test</td><td style="padding:8px;color:#10B981;">Below 140</td><td style="padding:8px;color:#F59E0B;">140–199</td><td style="padding:8px;color:#EF4444;">200+</td></tr>
<tr style="background:#EFF6FF;"><td style="padding:8px;">HbA1c test</td><td style="padding:8px;color:#10B981;">Below 5.7%</td><td style="padding:8px;color:#F59E0B;">5.7–6.4%</td><td style="padding:8px;color:#EF4444;">6.5%+</td></tr>
</table><br>
All values in mg/dL unless noted.<br><br>
⚠️ <i>Get tested by a certified lab for accurate results. Consult your doctor for interpretation.</i>"""
    },

    # ── HbA1c ─────────────────────────────────────────────────
    {
        'keywords': ['hba1c', 'a1c', 'glycated hemoglobin', 'hemoglobin a1c',
                     'average blood sugar', 'three month sugar'],
        'answer': """🧪 <b>What is HbA1c?</b><br><br>
HbA1c (Glycated Hemoglobin) measures your <b>average blood sugar over the past 3 months</b>. It is the most important test for monitoring diabetes.<br><br>
<b>HbA1c Ranges:</b><br>
• <span style="color:#10B981;">Below 5.7%</span> → Normal — No diabetes<br>
• <span style="color:#F59E0B;">5.7% to 6.4%</span> → Prediabetes — At risk<br>
• <span style="color:#EF4444;">6.5% and above</span> → Diabetes — Needs treatment<br>
• <span style="color:#EF4444;">Above 8%</span> → Poorly controlled — High risk of complications<br><br>
<b>Target for Diabetics:</b> Keep HbA1c below 7% to prevent complications.<br><br>
<b>How to Lower HbA1c:</b><br>
• Exercise regularly<br>
• Follow a low GI diet<br>
• Take prescribed medications<br>
• Monitor blood sugar regularly<br><br>
⚠️ <i>Get HbA1c tested every 3 months if you have diabetes.</i>"""
    },

    # ── DIET ──────────────────────────────────────────────────
    {
        'keywords': ['diet', 'food', 'what to eat', 'diabetic diet',
                     'meal plan', 'eating', 'nutrition', 'diet plan'],
        'answer': """🥗 <b>Diabetes Diet Guide:</b><br><br>
<b>✅ Foods to Eat Freely:</b><br>
• All non-starchy vegetables (spinach, broccoli, karela, okra)<br>
• Whole grains (oats, brown rice, quinoa, barley)<br>
• Lean proteins (fish, chicken, eggs, dal, lentils, tofu)<br>
• Low GI fruits (guava, apple, orange, berries)<br>
• Nuts and seeds (almonds, walnuts, flaxseeds)<br>
• Low fat dairy (curd, paneer, buttermilk)<br><br>
<b>⚠️ Eat in Moderation:</b><br>
• Banana, mango, grapes (high sugar fruits)<br>
• Chapati, brown rice, sweet potato<br>
• Honey, dark chocolate (70%+ cocoa)<br><br>
<b>❌ Avoid Completely:</b><br>
• White rice, maida, white bread<br>
• Sugary drinks (cola, juice, milkshakes)<br>
• Sweets, biscuits, cakes, pastries<br>
• Deep fried foods (samosa, vada, pakoda)<br>
• Jaggery, sugar, corn syrup<br><br>
💡 <b>Tip:</b> Use our <b>Food Checker</b> tab to check any specific food!<br><br>
⚠️ <i>Consult a registered dietitian for a personalized meal plan.</i>"""
    },

    # ── FOODS TO AVOID ────────────────────────────────────────
    {
        'keywords': ['avoid', 'not eat', 'bad food', 'foods to avoid',
                     'dangerous food', 'harmful food', 'restrict'],
        'answer': """❌ <b>Foods Diabetics Should Avoid:</b><br><br>
<b>High Sugar Foods:</b><br>
• Sugar, jaggery, honey (in large amounts)<br>
• Soft drinks, cola, fruit juices<br>
• Sweets, mithai, gulab jamun, kheer<br>
• Cakes, pastries, cookies, biscuits<br><br>
<b>High GI Carbs:</b><br>
• White rice (switch to brown rice or cauliflower rice)<br>
• White bread, maida products<br>
• Potato (especially fried)<br>
• Cornflakes, puffed rice<br><br>
<b>Unhealthy Fats:</b><br>
• Deep fried foods (samosa, vada, chips)<br>
• Full fat dairy in excess<br>
• Processed and packaged foods<br><br>
<b>Alcohol:</b><br>
• Avoid completely — disrupts blood sugar control<br><br>
💡 Use our <b>Food Checker</b> tab to check any specific food!<br><br>
⚠️ <i>Always follow your doctor's specific dietary recommendations.</i>"""
    },

    # ── EXERCISE ──────────────────────────────────────────────
    {
        'keywords': ['exercise', 'workout', 'physical activity', 'yoga',
                     'walking', 'gym', 'fitness', 'sport'],
        'answer': """🏃 <b>Exercise Guide for Diabetics:</b><br><br>
<b>Best Exercises for Diabetics:</b><br>
• <b>Walking</b> — 30 min daily walk after meals lowers blood sugar<br>
• <b>Swimming</b> — Low impact, excellent for blood sugar control<br>
• <b>Cycling</b> — Great cardio without joint stress<br>
• <b>Yoga</b> — Reduces stress and improves insulin sensitivity<br>
• <b>Strength Training</b> — Builds muscle, improves glucose uptake<br><br>
<b>Recommended Schedule:</b><br>
• At least <b>150 minutes per week</b> of moderate exercise<br>
• 30 minutes per day, 5 days a week<br>
• Include both cardio and strength training<br><br>
<b>Exercise Tips for Diabetics:</b><br>
• Always check blood sugar before exercise<br>
• If sugar is below 100 mg/dL — eat a small snack first<br>
• Carry glucose tablets or juice for emergencies<br>
• Stay hydrated — drink water before, during and after<br>
• Wear proper footwear to protect feet<br>
• Start slow and gradually increase intensity<br><br>
⚠️ <i>Consult your doctor before starting a new exercise program.</i>"""
    },

    # ── CAUSES ────────────────────────────────────────────────
    {
        'keywords': ['cause', 'reason', 'why diabetes', 'risk factor',
                     'how diabetes', 'diabetes cause'],
        'answer': """🔬 <b>Causes and Risk Factors of Diabetes:</b><br><br>
<b>Type 1 Diabetes Causes:</b><br>
• Autoimmune reaction (body attacks insulin cells)<br>
• Genetic factors<br>
• Environmental triggers (viral infections)<br><br>
<b>Type 2 Diabetes Risk Factors:</b><br>
• <b>Overweight or obesity</b> — especially belly fat<br>
• <b>Physical inactivity</b> — sedentary lifestyle<br>
• <b>Family history</b> — parent or sibling with diabetes<br>
• <b>Age</b> — risk increases after 45 years<br>
• <b>High blood pressure</b> — above 140/90 mmHg<br>
• <b>High cholesterol</b> — low HDL, high triglycerides<br>
• <b>Unhealthy diet</b> — high sugar and processed foods<br>
• <b>Stress</b> — raises cortisol and blood sugar<br>
• <b>Poor sleep</b> — less than 6 hours increases risk<br>
• <b>Smoking</b> — increases insulin resistance<br><br>
⚠️ <i>You can reduce your risk by maintaining a healthy weight, exercising regularly and eating well.</i>"""
    },

    # ── COMPLICATIONS ─────────────────────────────────────────
    {
        'keywords': ['complication', 'damage', 'effect of diabetes',
                     'diabetes problem', 'long term', 'organ damage'],
        'answer': """⚠️ <b>Diabetes Complications (if uncontrolled):</b><br><br>
<b>Short Term Complications:</b><br>
• <b>Hypoglycemia</b> — dangerously low blood sugar (below 70)<br>
• <b>Hyperglycemia</b> — dangerously high blood sugar<br>
• <b>DKA</b> — diabetic ketoacidosis (Type 1 emergency)<br><br>
<b>Long Term Complications:</b><br>
• <b>Eyes</b> — Diabetic retinopathy → blindness risk<br>
• <b>Kidneys</b> — Diabetic nephropathy → kidney failure<br>
• <b>Nerves</b> — Diabetic neuropathy → tingling, pain, numbness<br>
• <b>Heart</b> — 2-4x higher risk of heart disease and stroke<br>
• <b>Feet</b> — Poor circulation → wounds that won't heal → amputation risk<br>
• <b>Skin</b> — Frequent infections, slow healing<br>
• <b>Gums</b> — Severe gum disease<br><br>
<b>How to Prevent Complications:</b><br>
• Keep blood sugar in target range<br>
• Regular checkups with doctor<br>
• HbA1c test every 3 months<br>
• Eye exam yearly<br>
• Kidney function test yearly<br>
• Regular foot inspection daily<br><br>
⚠️ <i>Good blood sugar control prevents most complications. Stay in touch with your healthcare team.</i>"""
    },

    # ── LOW BLOOD SUGAR ───────────────────────────────────────
    {
        'keywords': ['low sugar', 'hypoglycemia', 'sugar low', 'blood sugar low',
                     'glucose low', 'sugar drop', 'feeling dizzy', 'shaking'],
        'answer': """🚨 <b>Low Blood Sugar (Hypoglycemia) — EMERGENCY INFO:</b><br><br>
<b>Signs of Low Blood Sugar (below 70 mg/dL):</b><br>
• Shaking or trembling<br>
• Sweating suddenly<br>
• Dizziness or lightheadedness<br>
• Rapid heartbeat<br>
• Extreme hunger<br>
• Confusion or irritability<br>
• Blurred vision<br><br>
<b>⚡ Immediate Action — Rule of 15:</b><br>
1. Eat 15g of fast-acting sugar IMMEDIATELY:<br>
   • 4 glucose tablets, OR<br>
   • 150ml fruit juice, OR<br>
   • 3-4 teaspoons of sugar in water<br>
2. Wait 15 minutes<br>
3. Recheck blood sugar<br>
4. If still below 70 — repeat step 1<br>
5. Once stable — eat a proper meal<br><br>
🚨 <b>If unconscious — CALL EMERGENCY SERVICES IMMEDIATELY</b><br><br>
⚠️ <i>This is emergency guidance only. Always consult your doctor about managing hypoglycemia.</i>"""
    },

    # ── HIGH BLOOD SUGAR ──────────────────────────────────────
    {
        'keywords': ['high sugar', 'hyperglycemia', 'sugar high', 'blood sugar high',
                     'glucose high', 'sugar spike', 'sugar increased'],
        'answer': """🚨 <b>High Blood Sugar (Hyperglycemia):</b><br><br>
<b>Signs of High Blood Sugar (above 180 mg/dL):</b><br>
• Frequent urination<br>
• Extreme thirst<br>
• Headache<br>
• Blurred vision<br>
• Fatigue<br>
• Fruity breath (in severe cases)<br><br>
<b>What To Do:</b><br>
• Drink plenty of water immediately<br>
• Check blood sugar with glucometer<br>
• Avoid sugary foods and drinks<br>
• Light walk can help lower sugar<br>
• Take prescribed medication if directed<br>
• Contact your doctor if above 300 mg/dL<br><br>
<b>When to Go to Hospital IMMEDIATELY:</b><br>
• Sugar above 400 mg/dL<br>
• Vomiting that won't stop<br>
• Difficulty breathing<br>
• Extreme confusion<br>
• Loss of consciousness<br><br>
⚠️ <i>This is educational guidance only. Consult your doctor for your specific management plan.</i>"""
    },

    # ── PREVENTION ────────────────────────────────────────────
    {
        'keywords': ['prevent', 'prevention', 'avoid diabetes', 'reduce risk',
                     'stop diabetes', 'how to prevent'],
        'answer': """🛡️ <b>How to Prevent Type 2 Diabetes:</b><br><br>
<b>Lifestyle Changes That Work:</b><br><br>
✅ <b>Lose excess weight</b> — Even 5-7% weight loss reduces risk by 58%<br><br>
✅ <b>Exercise regularly</b> — 150 minutes per week of moderate activity<br><br>
✅ <b>Eat healthy</b><br>
• Choose low GI foods<br>
• Increase fiber intake<br>
• Reduce sugar and processed foods<br>
• Eat more vegetables and whole grains<br><br>
✅ <b>Quit smoking</b> — Smoking increases diabetes risk by 30-40%<br><br>
✅ <b>Manage stress</b> — Practice yoga, meditation or deep breathing<br><br>
✅ <b>Sleep well</b> — 7-8 hours per night<br><br>
✅ <b>Regular checkups</b> — Blood sugar test once a year after age 35<br><br>
✅ <b>Stay hydrated</b> — Drink 8-10 glasses of water daily<br><br>
⚠️ <i>Type 1 diabetes cannot be prevented. Type 2 risk can be significantly reduced with lifestyle changes.</i>"""
    },

    # ── BMI ───────────────────────────────────────────────────
    {
        'keywords': ['bmi', 'body mass index', 'weight', 'obesity',
                     'overweight', 'healthy weight'],
        'answer': """⚖️ <b>BMI and Diabetes:</b><br><br>
<b>BMI Categories:</b><br>
• <span style="color:#3B82F6;">Below 18.5</span> → Underweight<br>
• <span style="color:#10B981;">18.5 to 24.9</span> → Normal weight ✅<br>
• <span style="color:#F59E0B;">25 to 29.9</span> → Overweight — increased risk<br>
• <span style="color:#EF4444;">30 and above</span> → Obese — high diabetes risk<br><br>
<b>BMI Formula:</b> Weight (kg) ÷ Height² (m²)<br><br>
<b>Why BMI Matters for Diabetes:</b><br>
• Each BMI unit above 25 increases diabetes risk by 20%<br>
• Belly fat (waist above 90cm men, 80cm women) is most dangerous<br>
• Losing just 5-10% body weight improves insulin sensitivity significantly<br><br>
<b>How to Reduce BMI:</b><br>
• Create a calorie deficit of 500 cal/day<br>
• Exercise 150+ minutes per week<br>
• Eat more protein and fiber<br>
• Reduce sugar and processed foods<br><br>
⚠️ <i>Consult a doctor or dietitian for a safe weight loss plan.</i>"""
    },

    # ── INSULIN ───────────────────────────────────────────────
    {
        'keywords': ['insulin', 'what is insulin', 'insulin resistance',
                     'insulin deficiency', 'how insulin works'],
        'answer': """💉 <b>About Insulin:</b><br><br>
<b>What is Insulin?</b><br>
Insulin is a hormone produced by the pancreas that acts like a key, allowing glucose from food to enter your body's cells for energy.<br><br>
<b>In Diabetes:</b><br>
• <b>Type 1</b> — Pancreas produces little or no insulin<br>
• <b>Type 2</b> — Body doesn't use insulin effectively (insulin resistance)<br><br>
<b>What is Insulin Resistance?</b><br>
When cells stop responding to insulin properly. Glucose stays in blood instead of entering cells. This leads to high blood sugar and eventually Type 2 diabetes.<br><br>
<b>How to Improve Insulin Sensitivity:</b><br>
• Exercise regularly — muscles absorb glucose directly<br>
• Lose excess belly fat<br>
• Eat low GI foods<br>
• Sleep 7-8 hours<br>
• Reduce stress<br>
• Avoid smoking and alcohol<br><br>
⚠️ <i>Never take insulin without a doctor's prescription. Dosage requires careful medical supervision.</i>"""
    },

    # ── STRESS ────────────────────────────────────────────────
    {
        'keywords': ['stress', 'anxiety', 'mental health', 'depression',
                     'stress and diabetes', 'emotional'],
        'answer': """🧘 <b>Stress and Diabetes:</b><br><br>
<b>How Stress Affects Blood Sugar:</b><br>
Stress releases hormones (cortisol, adrenaline) that raise blood sugar levels. Chronic stress makes diabetes harder to manage.<br><br>
<b>Signs of Diabetes-Related Stress:</b><br>
• Consistently high blood sugar despite medication<br>
• Feeling overwhelmed about managing diabetes<br>
• Skipping meals or medications<br>
• Sleep problems<br>
• Anxiety about complications<br><br>
<b>Ways to Manage Stress:</b><br>
• <b>Yoga and meditation</b> — proven to lower blood sugar<br>
• <b>Deep breathing</b> — 10 minutes daily<br>
• <b>Regular exercise</b> — natural stress reliever<br>
• <b>Adequate sleep</b> — 7-8 hours per night<br>
• <b>Social support</b> — talk to family and friends<br>
• <b>Journaling</b> — write down feelings<br>
• <b>Professional help</b> — counselor or psychologist<br><br>
⚠️ <i>Mental health is as important as physical health. Don't hesitate to seek professional support.</i>"""
    },

    # ── WATER & HYDRATION ─────────────────────────────────────
    {
        'keywords': ['water', 'hydration', 'drink water', 'how much water',
                     'fluids', 'dehydration'],
        'answer': """💧 <b>Hydration and Diabetes:</b><br><br>
<b>Why Water is Critical for Diabetics:</b><br>
• High blood sugar causes frequent urination and dehydration<br>
• Dehydration raises blood sugar further — dangerous cycle<br>
• Water helps kidneys flush out excess glucose<br><br>
<b>How Much to Drink:</b><br>
• <b>Minimum 8-10 glasses (2-2.5 liters) per day</b><br>
• More if exercising or in hot weather<br>
• Spread throughout the day — don't wait until thirsty<br><br>
<b>Best Drinks for Diabetics:</b><br>
• ✅ Plain water — best choice<br>
• ✅ Lemon water (no sugar)<br>
• ✅ Green tea or herbal tea<br>
• ✅ Black coffee (no sugar)<br>
• ✅ Buttermilk (chaas) — no added sugar<br><br>
<b>Drinks to Avoid:</b><br>
• ❌ Soft drinks and cola<br>
• ❌ Fruit juices (eat whole fruit instead)<br>
• ❌ Sweetened tea or coffee<br>
• ❌ Energy drinks<br>
• ❌ Alcohol<br><br>
⚠️ <i>Staying well hydrated is one of the simplest ways to support blood sugar management.</i>"""
    },

    # ── SLEEP ─────────────────────────────────────────────────
    {
        'keywords': ['sleep', 'rest', 'insomnia', 'sleep and diabetes',
                     'how much sleep', 'sleep quality'],
        'answer': """😴 <b>Sleep and Diabetes:</b><br><br>
<b>How Poor Sleep Affects Diabetes:</b><br>
• Less than 6 hours of sleep increases diabetes risk by 28%<br>
• Poor sleep raises cortisol → raises blood sugar<br>
• Increases hunger hormones → leads to overeating<br>
• Reduces insulin sensitivity<br><br>
<b>Recommended Sleep:</b><br>
• Adults: <b>7-9 hours per night</b><br>
• Consistent sleep and wake times are important<br><br>
<b>Tips for Better Sleep:</b><br>
• Sleep and wake at the same time daily<br>
• Keep bedroom cool, dark and quiet<br>
• Avoid screens 1 hour before bed<br>
• No caffeine after 2pm<br>
• Light walk after dinner — not intense exercise<br>
• Manage blood sugar before bed (target 100-140 mg/dL at bedtime)<br><br>
<b>Warning Signs at Night:</b><br>
• Waking frequently to urinate — may indicate high sugar<br>
• Night sweats — may indicate low sugar<br>
• Snoring or sleep apnea — worsens diabetes significantly<br><br>
⚠️ <i>Tell your doctor if you have persistent sleep problems — sleep apnea is very common in diabetics.</i>"""
    },

    # ── FOOT CARE ─────────────────────────────────────────────
    {
        'keywords': ['foot', 'feet', 'foot care', 'diabetic foot',
                     'wound', 'ulcer', 'neuropathy feet'],
        'answer': """👣 <b>Diabetic Foot Care:</b><br><br>
<b>Why Foot Care is Critical:</b><br>
High blood sugar damages nerves (neuropathy) and blood vessels in feet, causing loss of sensation. Small injuries can become serious infections without being felt.<br><br>
<b>Daily Foot Care Routine:</b><br>
• Inspect both feet every single day<br>
• Wash feet with lukewarm water (not hot — test with elbow)<br>
• Dry carefully between toes<br>
• Apply moisturizer (not between toes)<br>
• Cut toenails straight across<br>
• Never walk barefoot — indoors or outdoors<br>
• Wear well-fitting, comfortable shoes<br>
• Check inside shoes before wearing<br><br>
<b>Warning Signs — See Doctor Immediately:</b><br>
• Any cut, blister or wound that isn't healing<br>
• Redness, swelling or warmth<br>
• Numbness or tingling<br>
• Skin color changes<br>
• Foul smell from feet<br><br>
⚠️ <i>See a podiatrist (foot doctor) at least once a year. Never ignore foot injuries if you have diabetes.</i>"""
    },

    # ── PREGNANCY ─────────────────────────────────────────────
    {
        'keywords': ['pregnancy', 'gestational', 'pregnant', 'baby',
                     'diabetes pregnancy', 'gestational diabetes'],
        'answer': """🤱 <b>Diabetes and Pregnancy:</b><br><br>
<b>Gestational Diabetes:</b><br>
• Develops during pregnancy (usually 24-28 weeks)<br>
• Occurs when pregnancy hormones cause insulin resistance<br>
• Affects 2-10% of pregnancies<br>
• Usually resolves after delivery<br>
• But 50% chance of developing Type 2 diabetes later in life<br><br>
<b>Risks of Uncontrolled Gestational Diabetes:</b><br>
• Large baby (macrosomia) — difficult delivery<br>
• Premature birth<br>
• Baby's low blood sugar at birth<br>
• Increased C-section risk<br>
• Preeclampsia in mother<br><br>
<b>Management:</b><br>
• Blood sugar monitoring 4 times daily<br>
• Healthy diet — low GI foods<br>
• Regular gentle exercise (walking)<br>
• Insulin if diet is not sufficient<br>
• Regular prenatal checkups<br><br>
⚠️ <i>Always follow your obstetrician and endocrinologist's guidance during pregnancy. This is for educational purposes only.</i>"""
    },

    # ── MONITORING ────────────────────────────────────────────
    {
        'keywords': ['monitor', 'check sugar', 'glucometer', 'blood test',
                     'how to check', 'testing sugar', 'measure glucose'],
        'answer': """🔬 <b>Monitoring Blood Sugar:</b><br><br>
<b>How to Use a Glucometer:</b><br>
1. Wash hands with soap and dry well<br>
2. Insert test strip into glucometer<br>
3. Prick side of fingertip with lancet<br>
4. Touch drop of blood to test strip<br>
5. Read result in 5 seconds<br>
6. Record in your sugar tracker diary<br><br>
<b>When to Check:</b><br>
• Fasting — first thing in morning before eating<br>
• Before meals<br>
• 2 hours after meals<br>
• Before exercise<br>
• Before sleep (target 100-140 mg/dL)<br>
• When you feel symptoms of low or high sugar<br><br>
<b>Target Blood Sugar for Diabetics:</b><br>
• Fasting: 80-130 mg/dL<br>
• 2 hours after meal: Below 180 mg/dL<br>
• Before bed: 100-140 mg/dL<br><br>
💡 <b>Use our Sugar Tracker tab to log your readings daily!</b><br><br>
⚠️ <i>Your doctor will set individual targets based on your condition.</i>"""
    },

    # ── GREETING ──────────────────────────────────────────────
    {
        'keywords': ['hello', 'hi', 'hey', 'good morning', 'good evening',
                     'good afternoon', 'namaste', 'vanakkam'],
        'answer': """👋 <b>Hello! Welcome to VitaSense AI Chatbot!</b><br><br>
I am your personal diabetes health assistant. I can help you with:<br><br>
🔬 Information about diabetes types and symptoms<br>
📊 Blood sugar levels and HbA1c explained<br>
🥗 Diet and food advice for diabetics<br>
🏃 Exercise recommendations<br>
💧 Hydration and sleep tips<br>
🚨 Emergency guidance for low/high sugar<br>
⚠️ Diabetes complications and prevention<br><br>
<b>Quick Questions to Ask:</b><br>
• "What are diabetes symptoms?"<br>
• "What is normal blood sugar?"<br>
• "What foods should I avoid?"<br>
• "How to prevent diabetes?"<br>
• "What is HbA1c?"<br><br>
⚠️ <i>I provide educational information only. Always consult your doctor for medical advice.</i>"""
    },

    # ── THANK YOU ─────────────────────────────────────────────
    {
        'keywords': ['thank you', 'thanks', 'thank', 'helpful',
                     'great', 'awesome', 'good bot'],
        'answer': """😊 <b>You're welcome!</b><br><br>
I'm glad I could help!<br><br>
Remember — managing diabetes is a journey, not a destination. Small daily steps make a big difference:<br><br>
✅ Check blood sugar regularly<br>
✅ Exercise daily<br>
✅ Eat low GI foods<br>
✅ Stay hydrated<br>
✅ Sleep well<br>
✅ Visit your doctor regularly<br><br>
💡 Use our other features too:<br>
• <b>Predict tab</b> — Check your diabetes risk<br>
• <b>Food Checker</b> — Check if food is safe<br>
• <b>Sugar Tracker</b> — Log daily blood sugar<br><br>
Stay healthy! 🏥💙"""
    },

    # ── DEFAULT ───────────────────────────────────────────────
    {
        'keywords': ['__default__'],
        'answer': """🤔 <b>I'm not sure about that specific question.</b><br><br>
I specialize in diabetes-related topics. Here are things I can help with:<br><br>
• What is diabetes and its types?<br>
• Diabetes symptoms and warning signs<br>
• Normal blood sugar and HbA1c levels<br>
• Diet and foods to eat or avoid<br>
• Exercise recommendations<br>
• Preventing diabetes<br>
• Managing low or high blood sugar<br>
• Diabetes complications<br>
• Foot care, sleep, stress management<br><br>
💡 Try asking one of these topics!<br><br>
⚠️ <i>For specific medical questions, please consult a qualified healthcare professional.</i>"""
    }
]

# ══════════════════════════════════════════════════════════════
# MAIN CHATBOT FUNCTION
# ══════════════════════════════════════════════════════════════
def get_response(user_message):
    if not user_message:
        return {'status': 'error', 'message': 'Please type a message'}

    msg = user_message.lower().strip()

    # Search knowledge base
    for item in KNOWLEDGE_BASE:
        if item['keywords'] == ['__default__']:
            continue
        for keyword in item['keywords']:
            if keyword in msg:
                return {
                    'status':  'success',
                    'reply':    item['answer'],
                    'matched':  keyword
                }

    # Return default response
    for item in KNOWLEDGE_BASE:
        if item['keywords'] == ['__default__']:
            return {
                'status': 'success',
                'reply':   item['answer'],
                'matched': 'default'
            }

# ══════════════════════════════════════════════════════════════
# QUICK REPLY SUGGESTIONS
# ══════════════════════════════════════════════════════════════
QUICK_REPLIES = [
    "What is diabetes?",
    "Normal blood sugar levels",
    "Foods to avoid",
    "What is HbA1c?",
    "Diabetes symptoms",
    "How to prevent diabetes?",
    "Exercise for diabetics",
    "Low blood sugar emergency",
]

def get_quick_replies():
    return QUICK_REPLIES

# ══════════════════════════════════════════════════════════════
# TEST
# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Testing chatbot_model.py...\n")
    tests = [
        "hello",
        "what is diabetes",
        "normal blood sugar levels",
        "what foods should I avoid",
        "what is hba1c",
        "low blood sugar emergency",
        "how to prevent diabetes",
        "random question xyz",
    ]
    for q in tests:
        result = get_response(q)
        preview = result['reply'][:60].replace('<br>', ' ').replace('<b>','').replace('</b>','')
        print(f"  Q: {q[:40]:<40} → {preview}...")
    print(f"\n  Total topics in knowledge base : {len(KNOWLEDGE_BASE)-1}")
    print(f"  Quick replies available        : {len(QUICK_REPLIES)}")