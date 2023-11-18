

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
DIGITS = "1234567890"
PRONOUNS = [ "he", "she", "they", "it" ] #"xe", 
NOUN_PREFIX = [ "own", "a", "the", "some", "this" ]

TENSES=['past','past_active','conditional','negative', 'present','pres_active','future_active','future', 'future_negative']

GENDER_AGREEMENT_MAP = {
  "he" : { "own":"his", "obj":"his", "self":"himself"  },
  "she" : { "own":"her", "obj":"plural" },
  #"xe" : { "own":"xeir", "obj":"plural"  },
  "they" : { "own":"their", "obj":"plural", "self":"themselves"  },
  "you" : { "own":"your", "obj":"plural" },
  "it"  : { "own":"its", "obj":"its" },
  "other"  : { "own":"its", "obj":"other" },
  "I" : { "own":"my", "obj":"mine" }
}
