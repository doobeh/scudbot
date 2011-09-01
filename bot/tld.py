#!/usr/bin/env python
#
#-----------------------------------------------
# Top Level Domain by wx [wx@codeslum.org]
#-----------------------------------------------
# This module is for working with TLDs and 
# confirms a TLD is legitimate or not as well
# as provides information about the TLD.
#-----------------------------------------------
# Notes:
# TLD.Validate("tld") - Confirms a legit TLD.
# TLD.Association("tld") - Country association.
#-----------------------------------------------

import sys
from optparse import OptionParser

class TLD(object):
  '''Top Level Domain Names'''
  valid_tlds = ('com', 'org', 'nu', 'info', 'net', 'us', 'jp', 'net', 'biz', 'tv', 'asia', 'bv', 'bw',
                'aero', 'cat', 'coop', 'edu', 'gov', 'int', 'jobs', 'mil', 'mobi', 'museum', 'mil', 'name',
                'pro', 'tel', 'travel', 'ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq',
                'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'bf', 'bg', 'bh', 'bi', 'bj',
                'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci',
                'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm',
                'do', 'dz', 'ec', 'eg', 'ee', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fm', 'fo', 'fr', 'ga',
                'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 
                'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io',
                'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr',
                'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma',
                'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt',
                'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np',
                'nr', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt',
                'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg',
                'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sy', 'sz', 'tc',
                'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tr', 'tt', 'tw', 'tz',
                'ua', 'ug', 'uk', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye',
                'yt', 'yu', 'za', 'zm', 'zw', 'arpa')
  def __init__(self):
    pass
  def __str__(self):
    return " Class:\t ValidTLD('your string')\n Search String:\t %s\n" % (self.search_string)
  def Validate(self, domain=""):
    '''Checks if the TLD is good or bad'''
    self.domain = domain
    if self.domain in self.valid_tlds:
      return True
    else:
      return False
  def Association(self, check_tld=""):
    self.check_tld = check_tld
    self.check_validity = self.Validate(self.check_tld)
    if self.check_validity == False:
      return "%s is not a vaild TLD." % (self.check_tld)
    else:
      self.TLD_dict = { "aero" : "Air-Transport Industry.", "asia" : "Asia-Pacific", "biz" : "Business", "cat" : "Catalan",
                        "com" : "Commerical", "coop" : "Cooperatives", "edu" : "Educational", "gov" : "U.S. Governmental",
                        "info" : "Information", "int" : "International Organizations", "jobs" : "Companies", "mil" : "U.S. Military",
                        "mobi" : "Mobile Devices", "museum" : "Museums", "name" : "Individuals", "net" : "Network", "org" : "Organization",
                        "pro" : "Professions", "tel" : "Internet Communication Services", "travel" : "Travel and Tourism",
                        "ac" : "Ascension Island", "ad" : "Andorra", "ae" : "United Arab Emirates", "af" : "Afganistan",
                        "ag" : "Antigua and Barbuda", "ai" : "Anguilla", "al" : "Albania", "am" : "Armenia", "an" : "Netherlands Antilles",
                        "ao" : "Angola", "aq" : "Antarctica", "ar" : "Argentina", "as" : "American Samoa", "at" : "Austria",
                        "au" : "Australia including Ashmore, Cartier Islands, and Coral Sea Islands", "aw" : "Aruba", "ax" : "Aland",
                        "az" : "Azerbaijan", "ba" : "Bosnia and Herzegovina", "bb" : "Barbados", "bd" : "Bangladesh", "be" : "Belgium",
                        "bf" : "Burkina Faso", "bg" : "Burlgaria", "bh" : "Bahrain", "bi" : "Burundi", "bm" : "Bermuda",
                        "bn" : "Brunei Darussalam", "bo" : "Boliva", "br" : "Brazil", "bs" : "Bahamas", "bt" : "Bhutan",
                        "bv" : "Bouvet Island", "bw" : "Botswana", "by" : "Belarus", "bz" : "Belize", "ca" : "Canada",
                        "cc" : "Cocos Islands", "cd" : "Democratic Republic of the Congo Formerly Zaire", "cf" : "Central African Republic",
                        "cg" : "Republic of the Congo", "ch" : "Switzerland",
                        "ci" : "Cote d'Ivoire", "ck" : "Cook Islands", "cl" : "Chile", "cm" : "Cameroon", "cn" : "People's Republic of China",
                        "co" : "Colombia", "cr" : "Costa Rica", "cu" : "Cuba", "cv" : "Cape Verde", "cx" : "Christmas Island",
                        "cy" : "Cyprus", "cz" : "Czech Republic", "de" : "Germany (Deutschland)", "dj" : "Djibouti", "dk" : "Denmark",
                        "dm" : "Dominica", "do" : "Dominican Republic", "dz" : "Algeria (Dzayer)", "ec" : "Ecuador", "ee" : "Estonia (Eesti)",
                        "eg" : "Egypt", "er" : "Eritrea", "es" : "Spain", "et" : "Ethiopia", "eu" : "European Union",
                        "fi" : "Finland", "fj" : "Fiji", "fk" : "Falkland Islands", "fm" : "Federated States of Micronesia",
                        "fo" : "Faroe Islands", "fr" : "France", "ga" : "Gabon", "gb" : "United Kingdom", "gb" : "Grenada",
                        "ge" : "Georgia (Country)", "gf" : "French Guiana", "gg" : "Guernsey", "gh" : "Ghana", "gi" : "Gibraltar",
                        "gl" : "Greenland", "gm" : "The Gambia", "gn" : "Guinea", "gp" : "Guadeloupe", "gq" : "Equatorial Guinea",
                        "gr" : "Greece", "gs" : "South Georgia and the South Sandwich Islands", "gt" : "Guatemala", "gu" : "Guam",
                        "gw" : "Guinea-Bissau", "gy" : "Guyana", "hk" : "Hong Kong", "hm" : "Heard Island and McDonald Islands",
                        "hn" : "Honduras", "hr" : "Croatia (Hrvatska)", "ht" : "Haiti", "hu" : "Hungary", "id" : "Indoesia",
                        "ie" : "Republic of Ireland", "il" : "Israel", "im" : "Isle of Man", "in" : "India", "io" : "British Indian Ocean Territory",
                        "iq" : "Iraq", "is" : "Iceland", "ir" : "Iran", "it" : "Italy", "je" : "Jersey", "jm" : "Jamaica",
                        "jo" : "Jordan", "jp" : "Japan", "ke" : "kenya", "kg" : "Kyrgyzstan", "kh" : "Cambodia",
                        "ki" : "kiribati", "km" : "Comoros", "kn" : "Saint Kitts and Nevis", "kp" : "Democratic People's of Korea",
                        "kr" : "Republic of Korea", "kw" : "Kuwait", "ky" : "Cayman Islands", "kz" : "Kazakhstan", "la" : "Laos",
                        "lb" : "Lebanon", "lc" : "Saint Lucia", "li" : "Liechtenstein", "lk" : "Sri Lanka", "lr" : "Liberia", "ls" : "Lesotho",
                        "lt" : "Lithuania", "lu" : "Luxembourg", "lv" : "Latvia", "ly" : "Libya", "ma" : "Morocco", "mc" : "Monaco",
                        "md" : "Moldova", "me" : "Montenegro", "mg" : "Madagascar", "mh" : "Marshall Islands",
                        "mk" : "Republic of Macedonia the former Yugoslav Republic of Macedonia", "ml" : "Mali", "mm" : "Myanmar",
                        "mn" : "Mongolia", "mo" : "Macau", "mp" : "Northern Mariana Islands", "mq" : "Martinique", "mr" : "Maurtania",
                        "ms" : "Montserrat", "mt" : "Malta", "mu" : "Mauritius", "mv" : "Maldives", "mw" : "Malawi", "mx" : "Mexico",
                        "my" : "Malaysia", "mz" : "Mozambique", "na" : "Namibia", "nc" : "New Caledonia", "ne" : "Niger", "nf" : "Norfolk Island",
                        "ng" : "Nigeria", "ni" : "Nicaragua", "nl" : "Netherlands", "no" : "Norway", "np" : "Nepal", "nr" : "Nauru",
                        "nu" : "Niue", "nz" : "New Zealand", "om" : "Oman", "pa" : "Panama", "pe" : "Peru", "pf" : "French Polynesia with Clipperton Island",
                        "pg" : "Papua New Guinea", "ph" : "Philippines", "pk" : "Pakistan", "pl" : "Poland", "pm" : "Saint-Pierre and Miquelon",
                        "pn" : "Pitcairn Islands", "pr" : "Puerto Rico", "ps" : "Palestinian Territories", "pt" : "Portugal", "pw" : "Palau",
                        "py" : "Paraguay", "qa" : "Qatar", "re" : "Reunion", "ro" : "Romania", "rs" : "Serbia", "ru" : "Russia",
                        "rw" : "Rwanda", "sa" : "Saudi Arabia", "sb" : "Solomon Islands", "sc" : "Seychelles", "sd" : "Sudan", "se" : "Sweden",
                        "sg" : "Singapore", "sh" : "Saint Helena", "si" : "Slovenia", "sj" : "Svalbard and Jan Mayen Islands",
                        "sk" : "Slovakia", "sl" : "Sierra Leone", "sm" : "San Marino", "sn" : "Senegal", "so" : "Somalia",
                        "sr" : "Suriname", "st" : "Sao Tome and Principe", "su" : "Former Soviet Union", "sv" : "El Salvador", "sy" : "Syria",
                        "sz" : "Swaziland", "tc" : "Turks and Caicos Island", "td" : "Chad", "tf" : "French Southern and Antarctic Lands",
                        "tg" : "Togo", "th" : "Thailand", "tj" : "Tajikistan", "tk" : "Tokelau", "tl" : "East Timor", "tm" : "Turkmenistan",
                        "tn" : "Tunisia", "to" : "Tonga", "tp" : "East Timor", "tr" : "Turkey", "tt" : "Trinidad and Tobago", 
                        "tv" : "Tuvalu. Also used by Television Broadcasters.", "tw" : "Republic of China (Taiwan)", "tz" : "Tanzania",
                        "ua" : "Ukraine", "ug" : "Uganda", "uk" : "United Kingdom", "us" : "United States of America", "uy" : "Uruguay",
                        "uz" : "Uzbekistan", "va" : "Vatican City", "vc" : "Saint Vincent and the Grenadines", "ve" : "Venezuela",
                        "vg" : "British Virgin Islands", "vi" : "U.S. Virgin Islands", "vn" : "Vietnam", "vu" : "Vanuatu",
                        "wf" : "Wallis and Futuna", "ws" : "Samoa", "ye" : "Yemen", "yt" : "Mayotte", "yu" : "Yugoslavi, Now used for Serbia and Montenegro",
                        "za" : "South Africa (Zuid-Afrika)", "zm" : "Zabmbia", "zw" : "Zimbabwe", "arpa" : "Address and Routing Parameter Area." }
      return self.TLD_dict[self.check_tld]
