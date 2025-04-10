from flask import Flask, render_template, request, url_for

app = Flask(__name__)

first_aid_guides = {
  'bleeding': {
        'title': 'Controlling Bleeding',
        'description': 'Steps to take when someone is bleeding.',
        'steps': [
            'Apply direct pressure to the wound with a clean cloth or bandage.',
            'If the bleeding is severe or doesn\'t stop, elevate the injured limb.',
            'Seek immediate medical attention if bleeding is profuse or from an artery.',
        ],
        'keywords': ['cut', 'wound', 'blood', 'hemorrhage']
    },
    'burns': {
        'title': 'Treating Burns',
        'description': 'How to care for different types of burns.',
        'steps': [
            'For minor burns, cool the area with running cool water for 10-15 minutes.',
            'Do not apply ice, butter, or ointments to severe burns.',
            'Cover the burn with a sterile, non-adhesive bandage.',
            'Seek medical attention for large or deep burns.',
        ],
        'keywords': ['fire', 'heat', 'scald', 'sunburn']
    },
    'choking': {
        'title': 'Helping a Choking Person',
        'description': 'Actions to help someone who is choking.',
        'steps': [
            'Ask the person if they can cough or speak. If they can, encourage them to cough.',
            'If they cannot speak, cough, or breathe, perform the Heimlich maneuver (abdominal thrusts).',
            'For infants, use back blows and chest thrusts.',
            'Seek emergency medical help immediately.',
        ],
        'keywords': ['obstructed airway', 'cannot breathe', 'coughing', 'Heimlich']
    },
    'cpr': {
        'title': 'Cardiopulmonary Resuscitation (CPR)',
        'description': 'Steps for performing CPR on an adult.',
        'steps': [
            'Ensure the person is lying on a firm, flat surface.',
            'Call for emergency medical help immediately.',
            'If trained, perform chest compressions at a rate of 100-120 per minute.',
            'If trained, give rescue breaths after every 30 compressions (2 breaths).',
            'Continue until help arrives or the person shows signs of life.',
        ],
        'keywords': ['cardiac arrest', 'no breathing', 'unconscious', 'chest compressions']
    },
    'fractures': {
        'title': 'Dealing with Fractures',
        'description': 'Initial care for a suspected broken bone.',
        'steps': [
            'Do not try to straighten the injured limb.',
            'Immobilize the limb with a splint or sling.',
            'Apply ice packs to reduce swelling.',
            'Seek immediate medical attention.',
        ],
        'keywords': ['broken bone', 'pain', 'swelling', 'immobilize']
    },
    'sprains': {
        'title': 'Treating Sprains',
        'description': 'How to manage a sprained joint.',
        'steps': [
            'Rest the injured joint.',
            'Apply ice packs to reduce swelling.',
            'Compress the area with a bandage.',
            'Elevate the injured limb.',
        ],
        'keywords': ['twisted ankle', 'joint pain', 'swelling', 'RICE']
    },
    'head_injury': {
        'title': 'Responding to Head Injury',
        'description': 'Initial steps after a head trauma.',
        'steps': [
            'Assess the person\'s level of consciousness.',
            'Apply gentle pressure to any bleeding.',
            'Do not move the person unnecessarily.',
            'Seek immediate medical attention, especially if there is loss of consciousness, vomiting, or confusion.',
        ],
        'keywords': ['concussion', 'head trauma', 'dizziness', 'unconscious']
    },
    'heart_attack': {
        'title': 'Recognizing a Heart Attack',
        'description': 'What to do if someone is having a heart attack.',
        'steps': [
            'Recognize the signs: chest pain, shortness of breath, pain radiating to the arm or jaw.',
            'Call for emergency medical help immediately.',
            'Have the person sit down and rest.',
            'If prescribed, help them take aspirin.',
        ],
        'keywords': ['chest pain', 'heart trouble', 'angina', 'cardiac']
    },
    'stroke': {
        'title': 'Recognizing a Stroke (FAST)',
        'description': 'How to identify the signs of a stroke quickly.',
        'steps': [
            '**F**ace: Ask the person to smile. Does one side of the face droop?',
            '**A**rms: Ask the person to raise both arms. Does one arm drift downward?',
            '**S**peech: Ask the person to repeat a simple sentence. Does their speech sound slurred or strange?',
            '**T**ime: If you observe any of these signs, call emergency medical help immediately.',
        ],
        'keywords': ['brain attack', 'slurred speech', 'weakness', 'FAST']
    },
    'hypothermia': {
        'title': 'Treating Hypothermia (Low Body Temperature)',
        'description': 'Steps to warm someone with dangerously low body temperature.',
        'steps': [
            'Move the person to a warm place.',
            'Remove any wet clothing and replace it with dry layers.',
            'Warm the person gradually with blankets.',
            'Offer warm, sweet drinks if the person is conscious.',
            'Seek emergency medical help if symptoms are severe.',
        ],
        'keywords': ['cold', 'shivering', 'confusion', 'low temperature', 'fever', 'high temperature', ]
    },
    'heatstroke': {
        'title': 'Treating Heatstroke (High Body Temperature)',
        'description': 'Emergency care for dangerously high body temperature.',
        'steps': [
            'Move the person to a cool, shaded area.',
            'Remove excess clothing.',
            'Cool the person quickly by applying cool water to the skin or using ice packs.',
            'Encourage them to drink cool fluids if conscious.',
            'Seek emergency medical help immediately.',
        ],
        'keywords': ['hot', 'sweating', 'confusion', 'high temperature']
    },
    'poisoning': {
        'title': 'Responding to Poisoning',
        'description': 'Immediate actions if someone has ingested poison.',
        'steps': [
            'Call your local poison control center or emergency medical help immediately.',
            'Follow their instructions carefully.',
            'Do not induce vomiting unless instructed to do so.',
            'If possible, have the container or label of the poison available.',
        ],
        'keywords': ['swallowed', 'ingested', 'toxic', 'antidote', 'snake bite', 'scorpion bite']
    },
    'allergic_reaction': {
        'title': 'Managing Allergic Reactions',
        'description': 'Steps to take when someone is having an allergic reaction.',
        'steps': [
            'Identify the allergen if possible.',
            'If the person has an epinephrine auto-injector (EpiPen), help them use it.',
            'Call for emergency medical help immediately, especially if there is difficulty breathing or swelling of the face or throat.',
            'Keep the person calm and lying down if they are feeling faint.',
        ],
        'keywords': ['allergy', 'rash', 'itching', 'swelling', 'anaphylaxis', 'EpiPen']
    },
    'nosebleed': {
        'title': 'Managing a Nosebleed',
        'description': 'Steps to stop a nosebleed.',
        'steps': [
            'Have the person sit upright and lean slightly forward.',
            'Pinch the soft part of the nose just below the bony bridge for 10-15 minutes.',
            'Advise the person to breathe through their mouth.',
            'Do not tilt the head back.',
            'If bleeding continues, seek medical attention.',
        ],
        'keywords': ['nasal bleeding', 'bloody nose', 'epistaxis']
    },
    'fainting': {
        'title': 'Responding to Fainting',
        'description': 'What to do if someone faints.',
        'steps': [
            'Help the person lie down on their back.',
            'Elevate their legs slightly.',
            'Loosen any tight clothing.',
            'Check for responsiveness and breathing.',
            'If they don\'t recover quickly, call for medical help.',
        ],
        'keywords': ['syncope', 'passing out', 'lightheaded', 'unconscious']
    },
    'insect_stings': {
        'title': 'Treating Insect Stings',
        'description': 'How to care for bee, wasp, or hornet stings.',
        'steps': [
            'If a stinger is visible (especially from a bee), gently scrape it out with a credit card or fingernail.',
            'Wash the area with soap and water.',
            'Apply a cold compress to reduce swelling and pain.',
            'Watch for signs of an allergic reaction (difficulty breathing, swelling, hives).',
            'Seek immediate medical help if an allergic reaction occurs.',
        ],
        'keywords': ['bee sting', 'wasp sting', 'hornet sting', 'swelling', 'pain', 'allergy']
    },
    'animal_bites': {
        'title': 'Caring for Animal Bites',
        'description': 'Initial steps after an animal bite.',
        'steps': [
            'Wash the wound thoroughly with soap and water for several minutes.',
            'Apply a sterile bandage.',
            'Seek medical attention, especially if the bite broke the skin, is deep, or if the animal is unknown or acting strangely.',
            'Report the bite to animal control if necessary.',
        ],
        'keywords': ['dog bite', 'cat bite', 'scratch', 'infection', 'rabies']
    },
    'eye_injury': {
        'title': 'Responding to Eye Injury',
        'description': 'Immediate care for an injury to the eye.',
        'steps': [
            'Do not rub the eye.',
            'If there is a foreign object, do not try to remove it yourself.',
            'Seek immediate medical attention for any significant eye injury, pain, or vision changes.',
            'For chemical splashes, flush the eye with plenty of clean water for at least 15 minutes.',
        ],
        'keywords': [' травма глаза', 'foreign object', 'chemical splash', 'vision']
    },
    'toothache': {
        'title': 'Managing a Toothache',
        'description': 'Temporary relief for tooth pain.',
        'steps': [
            'Rinse your mouth with warm salt water.',
            'Gently floss to remove any food particles.',
            'Apply a cold compress to the outside of your cheek.',
            'Take over-the-counter pain medication if needed.',
            'See a dentist as soon as possible.',
        ],
        'keywords': ['dental pain', 'tooth pain', 'cavity', 'gum pain']
    },
    'muscle_cramps': {
        'title': 'Relieving Muscle Cramps',
        'description': 'How to stop a sudden muscle cramp.',
        'steps': [
            'Gently stretch and massage the affected muscle.',
            'Apply heat or cold to the area.',
            'Drink plenty of fluids, especially those containing electrolytes.',
        ],
        'keywords': ['spasm', 'tight muscle', 'painful contraction', 'leg cramp']
    },
    'minor_cuts_and_scrapes': {
        'title': 'Caring for Minor Cuts and Scrapes',
        'description': 'Steps for cleaning and bandaging small wounds.',
        'steps': [
            'Wash your hands thoroughly with soap and water.',
            'Gently clean the wound with mild soap and water.',
            'Apply a thin layer of antibiotic ointment.',
            'Cover the wound with a clean bandage.',
        ],
        'keywords': ['small cut', 'scratch', 'abrasion', 'superficial wound']
    }
}

@app.route('/')
def index():
    return render_template('index.html', guides=first_aid_guides.keys(), first_aid_guides=first_aid_guides)

@app.route('/guide/<aid_type>')
def guide(aid_type):
    if aid_type in first_aid_guides:
        return render_template('guide.html', aid=first_aid_guides[aid_type], aid_type=aid_type)
    else:
        return render_template('404.html', message=f"First-aid guide for '{aid_type}' not found.")

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query').lower()
    results = {}
    for key, details in first_aid_guides.items():
        if query in key.lower() or query in details['title'].lower() or any(query in step.lower() for step in details['steps']) or query in details.get('keywords', []):
            results[key] = details['title']
    return render_template('search_results.html', query=query, results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)