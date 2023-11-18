
import random

from ..dict.names import american_male_names, spanish_male_names, all_names
from ..dict.nouns import food_nouns, digital_nouns, animal_nouns, all_nouns
from ..dict.verbs import internet_verbs, relationship_verbs, all_verbs
from ..dict.adjs import all_adjs

from ..dict.const import *

from keeji.utils.__ import info, warn, silly, trace, error, set_printer_level, get_printer_level


#----------------------------------------------#


# class Entity():
#   def __init__(self,**opts):
#     self.name=opts.get('name','I')
#     self.pronoun=opts.get('obj','I')
#     self.noun=opts.get('noun','apple')
#     self.obj=opts.get('obj','mine')
#     self.ent_type=opts.get('entity','object') 
#     self.own=opts.get('his','its')
#     self.rel=opts.get('rel','self')
    
# this_self=Entity()
# other_self=Entity()

#----------------------------------------------#


#set_printer_level(0)


#----------------------------------------------#
def royal_we(pronoun):
  if pronoun == "I": 
    pres='am'
    past='was'
  elif pronoun in ['they','we','you']: 
    pres='are'
    past='were'
  else: 
    pres='is'
    past='was'
  return pres,past
  
  
def conjugate_verb(verb,tense='', pronoun=''):
  base_verb=""

  tense = random.choice(TENSES) if tense == "" else tense


  base_verb = verb
  
  # Check if the verb ends with a consonant or a vowel
  if tense in [ 'past', 'past_active', 'pres_active' ]:
    if verb[-1] in VOWELS:
      base_verb = verb[:-1]
    else:
      base_verb = verb
    
  base_verb = str(base_verb)


  r_pres,r_past=royal_we(pronoun)
  
  past = base_verb[:-1] + "ied" if base_verb.endswith('y') else base_verb + "ed"
  
  past_active = f"{r_past} {base_verb}ing" 
  conditional = "might " + base_verb
  negative = f"do not {base_verb}" if pronoun in ['I','they','we','you'] else f"does not {base_verb}"
  
  pres_active = f"{r_pres} {base_verb}ing"
  
  next_base = base_verb + "es" if base_verb.endswith('h') else base_verb + "s"
  present = base_verb if pronoun in ['I','they','we','you'] else next_base
  
  future_active = f"{r_pres} going to {base_verb}"
  future = "will " + base_verb  
  future_negative = "will not " + base_verb
   
  tense_list = {
      "past": past,
      "past_active": past_active,
      "conditional":conditional,
      "present": present,
      "pres_active": pres_active,
      "negative" : negative,
      "future_active": future_active,
      "future": future,
      "future_negative" : future_negative
  }
  

  
  res=tense_list.get(tense,verb) #+f" [{tense}]"
  trace(f"..tense > {pronoun} | {verb} | {tense} => {res}")
    
  return res



#----------------------------------------------#


def pick_from_lists(*args):
    """
    Accepts either multiple lists as arguments or a single list of lists.
    Randomly selects one list and then randomly selects an item from that list.
    Returns the index of the selected list and the selected item.
    """
    if not args:
        return None, None

    # Determine if the first argument is a list of lists or if args are individual lists
    if len(args) == 1 and isinstance(args[0], list) and isinstance(args[0][0], list):
        lists = args[0]
    else:
        lists = args

    # Randomly select a list and get its index
    list_index = random.randrange(len(lists))

    # Get the selected list using the index
    selected_list = lists[list_index]

    # Check if the selected list is empty
    if not selected_list:
        return list_index, None

    # Randomly select an item from the list
    selected_item = random.choice(selected_list)

    return list_index, selected_item

  
#----------------------------------------------#

def gen_prefix(noun,adj=''):
  
  prefix = random.choice(NOUN_PREFIX)
  
  if prefix == 'a':
    
    if adj != '' and adj[0] in VOWELS or \
       adj == '' and noun[0] in VOWELS:
      return "an"
    else:
      return "a"  
  return prefix

  
#----------------------------------------------#



def pronoun_agreement(pronoun, **kwargs):
  
  if not pronoun:
    raise KeyError("Pronoun key requires for agreement lookup")
  #a the this that  
  gmap = GENDER_AGREEMENT_MAP.get(pronoun,{})
  
  own = gmap.get('own','')
  own_obj = gmap.get('obj','')
  own_self = gmap.get('self','')

  error(repr(own_self),repr(own))
  
  if own_self == '':
    
    if own.endswith('s'):
      own = own[:-1]
      
    own_self = f"{own}self"          
    
  #info(f"agree ->  self: {own_self} own: {own}")
                
  if own_obj == 'plural':
    own_obj = own + "s"
    
  elif own_obj == 'other':
    ref = kwargs.get('noun','')
    own_obj = "the {ref}'s"
    
  #silly(f"agree? [{pronoun}]->  {own} {own_obj} {own_self}")  
  return own,own_obj,own_self


  
#----------------------------------------------#


  
def gen_entity(actor_type='',ref=''):
  actor=''
  choices=['entity','person','group', 'object'] #no self
  
  if ref=='self':
    choices.append('self')
    #trace(f"random can select self now")
  else:
    pass
    #trace(f"other_type : {actor_type}")
    
  actor_choice = random.choice(choices)
    
  if actor_type == '':
    actor_type=actor_choice

  
  if actor_type=='self':
    
    actor='self'
    pronoun='self'
    
  else:
    
    if actor_type == 'group':
      pronoun='they'
      this_list=all_nouns
    elif actor_type in ['object']:
      pronoun='it'
      this_list=all_nouns
      
    else:
      actor_type='person'
      pronoun = random.choice(['he','she']) #'xe'
      this_list=all_names
      
    _, actor = pick_from_lists(this_list)

    if actor_type == 'person' or  actor_type == 'entity':
      actor = f"{actor}".capitalize()
      
    #poormans plurals
    if actor_type == 'group':  
      if actor and "f{actor}".endswith('y'): 
        actor = actor[:-1]
        actor = f"{actor}ies"
      elif f"{actor}".endswith(('s','x')):
        actor = f"{actor}es"     
      else: 
        actor = f"{actor}s"
      
      
  trace(f"random chose [{actor}] {pronoun} {actor_type} [{actor_choice}]")    
  # if actor_type=='self':
  #   silly(f"--> last entity shall self refer ↩︎")
  # else:
  #   trace(f"[entity] --> new [{actor_type} : {actor} or {ref}?]  {pronoun}") 
    
  
    
  return actor, pronoun, actor_type
    
  
  
  
#----------------------------------------------#


def simple_sentence(name_list, verb_list, noun_list, **kwargs):
    # Randomly select a name, verb, and noun from the specified lists
    pronoun = kwargs.get('pronoun','')
    
    if pronoun:
      person = pronoun
    else:
      person = random.choice(name_list)
    
    verb = random.choice(verb_list)
    noun = random.choice(noun_list)
    
    noun_prefix = random.choice(NOUN_PREFIX)
    
    
    if noun_prefix == 'own':
      actor_type='person'
      _, pronoun, actor_type = gen_entity(actor_type)

    if pronoun:
      own, own_obj, own_self = pronoun_agreement(pronoun)
      info(f"[{noun}] {pronoun} {own} {own_obj} {own_self}")    
      #person=f"{person}({pronoun})"
      
      if noun_prefix == 'own' and own != '':
        noun_prefix=own
  
    trace(f"{person} {pronoun} {verb} {noun}")
    
    if noun_prefix == 'a':
      if noun[0] in VOWELS:
        noun_prefix = "an"
      else:
        noun_prefix = "a"
    
    tense = kwargs.get('tense','')
    verb = conjugate_verb(verb,tense,pronoun=pronoun)
    # Create a sentence based on the pattern template
    
    
    sentence = f"{person} {verb} {noun_prefix} {noun}. "
    sentence = sentence.capitalize()
    
    return sentence
  
  
#------------------------------------------------------------------------>

  
def smarter_sentence(**kwargs):

  ref = kwargs.get('ref','')

  actor_type = kwargs.get('actor','')
  actor, actor_pronoun, actor_type = gen_entity(actor_type)
  actor_own, actor_own_obj, actor_self = pronoun_agreement(actor_pronoun) 
  
  target_type = kwargs.get('target','')
  target, target_pronoun, target_type = gen_entity(target_type,'self')
  target_own, target_own_obj, target_self = pronoun_agreement(target_pronoun)      


  subphrase=''

  if target in  ['self','self_s']: #she
    target_own_obj=actor_own_obj #her
    target_self=actor_self #herself
    target_type=actor_type
    target_pronoun=actor_pronoun
    

  if target not in ['person','self']:
    
    _, adj  = pick_from_lists(all_adjs)

    
    if target_type != "group":
      prefix=gen_prefix(target,adj)
      
      #print(repr(prefix))
      
      if prefix == "own":
        prefix = actor_own

      subphrase+=prefix + " "

    subphrase=f"{subphrase}{adj} "
    
  elif target == 'self':
    target=actor
    target=target_self
    
  else: #person
    adj=""
    prefix=""
  
  
  trace(f"focus -> actor:{actor} target:{target} type:{target_type}")
      
  _, verb = pick_from_lists(all_verbs)
  tense = kwargs.get('tense','')
  verb = conjugate_verb(verb,tense,pronoun=actor_pronoun)
  
  #name = actor_pronoun if ref=='self' else name
  actor = f"{actor}".capitalize()
  sentence = f"{actor} {verb} {subphrase}{target}. "
  #sentence = sentence.capitalize()
  
  return sentence




#------------------------------------------------------------------------>



  
def next_simple_sentence():

  name_list = []
  name_list.extend(american_male_names)
  name_list.extend(spanish_male_names)  
  pronoun = random.choice(PRONOUNS)
  # own, own_obj, own_self = pronoun_agreement(pronoun)
  # #info(f"{pronoun} {own} {own_obj} {own_self}")
  
  s1 = simple_sentence(name_list, internet_verbs, digital_nouns )
  s2 = simple_sentence(name_list, internet_verbs, digital_nouns, pronoun=pronoun)
  print(s1)
  print(s2)

  
def next_smart_sentence():
  
  s1= smarter_sentence()
  print(s1)
  
  
  
def sentence_driver():
  set_printer_level(0)
  
  name_list = []
  name_list.extend(american_male_names)
  name_list.extend(spanish_male_names)
  
  pronoun = random.choice(PRONOUNS)
  own, own_obj, own_self = pronoun_agreement(pronoun)
  
  info(pronoun)

  s1 = simple_sentence(name_list, internet_verbs, digital_nouns )
  s2 = simple_sentence(name_list, internet_verbs, digital_nouns, pronoun=pronoun)
  s3 = simple_sentence(name_list, relationship_verbs, animal_nouns, pronoun=pronoun)

  info('Generating sentence examples')
  print(s1)
  print(s2)
  print(s3)

  s4= smarter_sentence()
  s5= smarter_sentence()
  s6= smarter_sentence()

  print(s4)
  print(s5)
  print(s6)
# _list = [ american_male_first_names, american_first_names, mexican_male_names, african_names, japanese_names ]

# def create_unique_list(input_lists):
#     unique_items = []
#     for input_list in input_lists:
#         for item in input_list:
#             if item not in unique_items:
#                 unique_items.append(item)
#     return unique_items

# def output_unique_list():
#   unique_names = create_unique_list(_list)
#   with open("unique.py", "w") as file:
#     file.write("unique_names = [\n")
#     for name in unique_names:
#         file.write(f'    "{name}",\n')
#     file.write("]\n")
