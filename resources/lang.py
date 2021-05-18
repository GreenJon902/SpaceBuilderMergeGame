from kivy.event import EventDispatcher
from kivy.properties import OptionProperty

from configurables import userSettings
from lib.betterLogger import BetterLogger

#  All locale codes
# noinspection SpellCheckingInspection
language_codes: list[str] = ['af-za', 'am-et', 'ar-ae', 'ar-bh', 'ar-dz', 'ar-eg', 'ar-iq', 'ar-jo', 'ar-kw', 'ar-lb',
                             'ar-ly', 'ar-ma', 'arn-cl', 'ar-om', 'ar-qa', 'ar-sa', 'ar-sy', 'ar-tn', 'ar-ye', 'as-in',
                             'az-cyrl-az', 'az-latn-az', 'ba-ru', 'be-by', 'bg-bg', 'bn-bd', 'bn-in', 'bo-cn', 'br-fr',
                             'bs-cyrl-ba', 'bs-latn-ba', 'ca-es', 'co-fr', 'cs-cz', 'cy-gb', 'da-dk', 'de-at', 'de-ch',
                             'de-de', 'de-li', 'de-lu', 'dsb-de', 'dv-mv', 'el-gr', 'en-029', 'en-au', 'en-bz', 'en-ca',
                             'en-gb', 'en-ie', 'en-in', 'en-jm', 'en-my', 'en-nz', 'en-ph', 'en-sg', 'en-tt', 'en-us',
                             'en-za', 'en-zw', 'es-ar', 'es-bo', 'es-cl', 'es-co', 'es-cr', 'es-do', 'es-ec', 'es-es',
                             'es-gt', 'es-hn', 'es-mx', 'es-ni', 'es-pa', 'es-pe', 'es-pr', 'es-py', 'es-sv', 'es-us',
                             'es-uy', 'es-ve', 'et-ee', 'eu-es', 'fa-ir', 'fi-fi', 'fil-ph', 'fo-fo', 'fr-be', 'fr-ca',
                             'fr-ch', 'fr-fr', 'fr-lu', 'fr-mc', 'fy-nl', 'ga-ie', 'gd-gb', 'gl-es', 'gsw-fr', 'gu-in',
                             'ha-latn-ng', 'he-il', 'hi-in', 'hr-ba', 'hr-hr', 'hsb-de', 'hu-hu', 'hy-am', 'id-id',
                             'ig-ng', 'ii-cn', 'is-is', 'it-ch', 'it-it', 'iu-cans-ca', 'iu-latn-ca', 'ja-jp', 'ka-ge',
                             'kk-kz', 'kl-gl', 'km-kh', 'kn-in', 'kok-in', 'ko-kr', 'ky-kg', 'lb-lu', 'lo-la', 'lt-lt',
                             'lv-lv', 'mi-nz', 'mk-mk', 'ml-in', 'mn-mn', 'mn-mong-cn', 'moh-ca', 'mr-in', 'ms-bn',
                             'ms-my', 'mt-mt', 'nb-no', 'ne-np', 'nl-be', 'nl-nl', 'nn-no', 'nso-za', 'oc-fr', 'or-in',
                             'pa-in', 'pl-pl', 'prs-af', 'ps-af', 'pt-br', 'pt-pt', 'qut-gt', 'quz-bo', 'quz-ec',
                             'quz-pe', 'rm-ch', 'ro-ro', 'ru-ru', 'rw-rw', 'sah-ru', 'sa-in', 'se-fi', 'se-no', 'se-se',
                             'si-lk', 'sk-sk', 'sl-si', 'sma-no', 'sma-se', 'smj-no', 'smj-se', 'smn-fi', 'sms-fi',
                             'sq-al', 'sr-cyrl-ba', 'sr-cyrl-cs', 'sr-cyrl-me', 'sr-cyrl-rs', 'sr-latn-ba',
                             'sr-latn-cs', 'sr-latn-me', 'sr-latn-rs', 'sv-fi', 'sv-se', 'sw-ke', 'syr-sy', 'ta-in',
                             'te-in', 'tg-cyrl-tj', 'th-th', 'tk-tm', 'tn-za', 'tr-tr', 'tt-ru', 'tzm-latn-dz', 'ug-cn',
                             'uk-ua', 'ur-pk', 'uz-cyrl-uz', 'uz-latn-uz', 'vi-vn', 'wo-sn', 'xh-za', 'yo-ng', 'zh-cn',
                             'zh-hk', 'zh-mo', 'zh-sg', 'zh-tw', 'zu-za']



def convert(array: {str: str}):
    path: {str: str} = {}

    def loop_inner(a: {str: str}, p: str):  # array, path
        for i in a:
            if isinstance(a[i], dict):
                loop_inner(a[i], p + str(i) + ".")

            else:
                path[p + str(i)] = a[i]

    loop_inner(array, "")
    BetterLogger(name="lang_converter").log_deep_debug("Converted", array)
    BetterLogger(name="lang_converter").log_deep_debug("to", path)
    return path



class Lang(BetterLogger, EventDispatcher):
    language_code: OptionProperty = OptionProperty("en-gb", options=language_codes)
    languages: {str: {str: str}} = {}

    def __init__(self):
        BetterLogger.__init__(self)
        EventDispatcher.__init__(self)
        self.language_code = userSettings.get("UI", "language")

    def register_array(self, array: {str: str}, language_code: str):
        self.log_deep_debug("Registering array for", language_code)

        self.languages[language_code] = array

    def get_all(self, language_code: str) -> {str}:
        return self.languages[str(language_code)]

    def get(self, text_id: str) -> str:
        try:
            return self.languages[self.language_code][str(text_id)]
        except KeyError:
            self.log_critical("No text found for id", text_id, "in language", self.language_code)
            return self.languages[self.language_code]["General.InvalidTextId"]


Lang: Lang = Lang()
