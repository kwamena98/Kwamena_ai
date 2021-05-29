from translate import Translator
translator= Translator(from_lang="English",to_lang="Korean")
translation = translator.translate("How are you ?")
print (translation)
