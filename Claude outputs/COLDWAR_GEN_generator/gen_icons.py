# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | icon choice for new foci and pictures for new national spirits.

Existing ids keep their icon. New foci get a generic MD/vanilla sprite (folders gfx/interface/goals/00_*) chosen by
keyword score from the focus name and its effects; every icon once in the tree; no photos, no country-specific art.
Overrides (hand picks) go into ICON_OVERRIDE / PICTURE_OVERRIDE.
"""
import json, os, re, math
from collections import Counter
from gen_common import IDX_DIR

from icon_picks import ICONS as ICON_OVERRIDE   # design id -> sprite name (hand picks)
from icon_picks import PICTURES as PICTURE_OVERRIDE   # idea id (without prefix) -> picture name (hand picks)

PHOTOS = {'STALIN_PLAN', 'ABMT_1'}
EXCL_FOLDERS = ('00_flag_groups', '00_regions', '00_cities', 'companies', '00_alliance', '00_organizations',
                'attack_x', '00_align', '00_terrorism')
BAD_TOKENS = {'gay', 'nazi', 'hitler', 'swastika', 'reich', 'kkk', 'hamas', 'hezbollah', 'taliban', 'isis', 'qaeda',
              'alqaeda', 'jihad', 'jihadist', 'terror', 'terrorist', 'terrorism', 'genocide', 'zombie', 'zombies',
              'meme', 'troll', 'putin', 'stalin', 'lenin', 'mao', 'trump', 'obama', 'biden', 'kim', 'assad', 'saddam',
              'gaddafi', 'castro', 'che', 'nuke', 'nukes', 'bomb', 'bombs', 'molotov', 'execution', 'sooty', 'champagne',
              'wine', 'coffee', 'sheep', 'horse', 'covid', 'drone', 'drones', 'internet', 'cyber', 'crypto', 'bitcoin',
              'smartphone', 'eaf', 'mlw'}
RELIGION_WORDS = {'hindu', 'buddha', 'buddhism', 'buddhist', 'catholic', 'catholicism', 'orthodox', 'orthodoxy', 'protestantism',
                  'pope', 'papacy', 'vatican', 'bible', 'judaism', 'jewish', 'crusader', 'cruader', 'shintoism', 'taoism', 'kali',
                  'miaphysite', 'patriarchate', 'islamophobia', 'christianophobia', 'maria', 'sikh'}
COUNTRY_WORDS = set('''russian russia soviet sovet american america chinese china german germany french france british
britain english japan japanese india indian african africa iran iranian iraq iraqi syria syrian turkish turkey israel
israeli arab arabian saudi egypt egyptian cuba cuban korea korean vietnam vietnamese ukraine ukrainian belarus polish poland
italian italy spanish spain mexico mexican brazil brazilian argentina argentinian australia australian canada canadian europe
european asia asian nato warsaw ussr usa uk eu taiwan palestine palestinian kurdish kurd kurds afghan afghanistan pakistan
bosnian serbian serbia greek greece swiss swedish sweden dutch norwegian finnish danish irish scottish chilean venezuelan
colombian thai burmese ethiopian nigerian libyan algerian moroccan yemeni chechen georgian armenian azerbaijani kazakh
mongolian tibetan roman rome byzantine ottoman persian aztec inca viking crimea kuban ural tatar bashkir siberian moscow
kremlin texas california bavaria prussia austria austrian hungarian romanian bulgarian czech slovak slovenian croatian
albanian macedonian portuguese belgian lebanese jordanian kuwaiti qatari emirati omani sudanese somali kenyan
indonesian malaysian filipino singapore hongkong cambodian laotian burma nepal bhutan lanka sahrawi abkhaz ossetian
transnistria donbass donetsk luhansk wagner pla nkvd kgb cia mossad'''.split())
EN3 = {'the', 'new', 'war', 'red', 'air', 'oil', 'big', 'sea', 'tax', 'law', 'one', 'two', 'buy', 'end', 'our', 'all',
       'map', 'set', 'pro', 'eco', 'gun', 'arm', 'net', 'old', 'car', 'man', 'aid', 'and', 'for', 'non', 'anti', 'job',
       'fob', 'raf', 'tnt', 'gas', 'ice', 'sun', 'act', 'day', 'joy', 'top', 'low', 'key', 'way', 'gdp', 'its', 'own',
       'out', 'run', 'fly', 'sky', 'cap', 'hub', 'eye', 'arc', 'era', 'war'}

SYN = {
    'army': 'army military soldier soldiers troops infantry general', 'military': 'military army soldier general troops',
    'officer': 'officers general army military academy', 'officers': 'officers general army military academy',
    'general': 'general army military', 'generals': 'general army military', 'barracks': 'army military soldier',
    'guard': 'guard army soldier security', 'guards': 'guard army soldier security', 'militia': 'militia soldier army partisan',
    'militias': 'militia soldier army partisan', 'conscription': 'army recruiting soldier conscription',
    'air': 'air aircraft fighters jet airforce', 'aircraft': 'aircraft air fighters jet', 'pilots': 'air fighters jet',
    'navy': 'navy naval fleet ship', 'naval': 'naval navy fleet ship', 'fleet': 'fleet navy naval ship', 'sea': 'sea naval navy ship',
    'police': 'police security secret', 'security': 'security secret police espionage', 'secret': 'secret espionage intelligence security',
    'order': 'order security police law', 'surveillance': 'surveillance espionage secret security',
    'intelligence': 'intelligence espionage secret', 'counter': 'security espionage', 'subversion': 'security espionage',
    'industry': 'industry factory production industrial', 'industrial': 'industry factory production industrial',
    'factory': 'factory industry production', 'factories': 'factory industry production', 'steel': 'steel industry factory',
    'heavy': 'industry heavy factory', 'arms': 'arms gun weapons military', 'weapons': 'weapons arms gun',
    'construction': 'construction construct build roads', 'build': 'build construction construct', 'roads': 'roads construction infrastructure',
    'infrastructure': 'infrastructure roads construction', 'housing': 'construction housing build',
    'economy': 'economy economic market money', 'economic': 'economic economy market', 'market': 'market trade economy',
    'finance': 'money market economic', 'money': 'money economic', 'bank': 'money market bank', 'banks': 'money market bank',
    'budget': 'money economic budget', 'tax': 'tax money', 'taxes': 'tax money', 'fund': 'money investments fund',
    'investment': 'investments money', 'capital': 'money market capitalism', 'private': 'market money business',
    'privatise': 'market money business', 'business': 'business smb market money', 'enterprise': 'business production industry',
    'enterprises': 'business production industry', 'trade': 'trade export deal market', 'export': 'export trade market',
    'exports': 'export trade market', 'import': 'import trade', 'free': 'free freedom liberty',
    'farm': 'farming agriculture agrarianism land', 'farmers': 'farming agriculture agrarianism land', 'land': 'land agriculture farming',
    'agrarian': 'agrarianism agriculture farming', 'peasant': 'farming agriculture land', 'peasants': 'farming agriculture land',
    'village': 'farming agriculture village', 'villages': 'farming agriculture village', 'rural': 'farming agriculture',
    'countryside': 'farming agriculture', 'harvest': 'farming agriculture rice', 'food': 'food agriculture farming',
    'oil': 'oil energy', 'petroleum': 'oil energy', 'energy': 'energy power electricity', 'power': 'power energy',
    'electricity': 'power energy electricity', 'dam': 'water energy power', 'water': 'water', 'nuclear': 'nuclear uranium atom',
    'atomic': 'nuclear uranium atom', 'atom': 'nuclear atom', 'science': 'science research', 'research': 'research science',
    'technology': 'science research technology', 'technocrats': 'science research technocrats', 'university': 'university education science',
    'universities': 'university education science', 'school': 'education school university', 'schools': 'education school',
    'education': 'education university school', 'literacy': 'education school', 'students': 'education university student',
    'health': 'health social hospital', 'welfare': 'social welfare health', 'social': 'social welfare', 'pension': 'social welfare',
    'workers': 'workers worker labour proletarian union', 'labour': 'labour workers worker union', 'union': 'union workers labour',
    'unions': 'union workers labour', 'strike': 'strike workers', 'party': 'party politics political', 'vanguard': 'communist communism party',
    'cadres': 'communist party cadres', 'communist': 'communist communism red', 'communism': 'communism communist red',
    'socialism': 'socialism socialist red', 'socialist': 'socialist socialism', 'revolution': 'revolution revolutionary red',
    'revolutionary': 'revolution revolutionary', 'marxism': 'marxism communism', 'collective': 'collective communism workers',
    'democracy': 'democracy democratic liberal', 'democratic': 'democratic democracy', 'election': 'election elections democracy',
    'elections': 'elections election democracy', 'vote': 'election elections democracy', 'parliament': 'parliament democracy government',
    'constitution': 'constitution laws law', 'liberal': 'liberal liberty freedom', 'freedom': 'freedom liberty free', 'rights': 'freedom liberty rights',
    'press': 'press media newspaper', 'islam': 'islam islamic muslim', 'islamic': 'islamic islam muslim', 'muslim': 'muslim islam islamic',
    'faith': 'faith religion islamic', 'mosque': 'mosque islam', 'sharia': 'islamic islam law', 'ulema': 'islamic islam clergy',
    'jurist': 'islamic clergy law', 'clergy': 'clergy religion church', 'clerics': 'clergy religion', 'religious': 'religion religious',
    'caliphate': 'islamic islam caliphate', 'holy': 'holy religion', 'church': 'church christian clergy',
    'king': 'king monarchy royal crown', 'royal': 'royal monarchy crown king', 'crown': 'crown monarchy king', 'monarchy': 'monarchy monarchism crown',
    'throne': 'throne monarchy crown', 'dynasty': 'monarchy crown', 'prince': 'monarchy royal', 'palace': 'monarchy palace government',
    'nation': 'nation national nationalism', 'national': 'national nationalism nation', 'nationalist': 'nationalism nationalist national',
    'patriotic': 'patriotism national', 'fatherland': 'national nationalism', 'unity': 'unity national', 'fascist': 'fascist fascism',
    'corporate': 'corporatism fascism', 'green': 'green environment nature', 'environment': 'environment green nature',
    'nature': 'nature green environment', 'conservation': 'environment green nature', 'pollution': 'environment green',
    'landscapes': 'nature green environment', 'propaganda': 'propaganda media', 'media': 'media propaganda television',
    'television': 'television media', 'radio': 'radio media', 'broadcasting': 'media radio television', 'culture': 'culture art',
    'cultural': 'culture art', 'diplomacy': 'diplomacy relations treaty', 'alliance': 'alliance treaty', 'treaty': 'treaty agreement deal',
    'foreign': 'foreign diplomacy international', 'neutral': 'neutrality peace', 'neutrality': 'neutrality peace',
    'peace': 'peace diplomacy', 'summit': 'diplomacy conference', 'conference': 'diplomacy conference',
    'women': 'women woman female', 'youth': 'youth student', 'corruption': 'corruption', 'purge': 'purge',
    'repression': 'repression purge', 'plan': 'plan planning', 'planning': 'planning plan', 'reform': 'reform improve modern',
    'reforms': 'reform improve modern', 'modernise': 'modern reform upgrade', 'modernisation': 'modern reform upgrade',
    'oligarchs': 'oligarch money business', 'state': 'state government', 'government': 'government state politics',
    'administration': 'government bureaucracy', 'bureaucracy': 'bureaucracy government', 'decree': 'law laws government',
    'law': 'law laws justice', 'laws': 'laws law', 'courts': 'justice law courts', 'justice': 'justice law',
    'tank': 'tank tanks armor', 'tanks': 'tanks tank armor', 'border': 'border fort', 'defence': 'defense fort', 'defense': 'defense fort',
    'helicopters': 'helicopter', 'missiles': 'missile', 'mobilise': 'mobilization army', 'volunteers': 'volunteers',
    'immigrants': 'immigration', 'workers_abroad': 'immigration', 'guest': 'immigration workers', 'migration': 'immigration',
    'ports': 'port navy trade', 'shipyards': 'shipyard navy ship', 'railways': 'railway rail', 'railway': 'railway rail',
    'mines': 'mining mine', 'mining': 'mining mine', 'coal': 'coal mining', 'gold': 'gold money', 'aid': 'aid help',
}
STOP = set('a an the of and or to in on for by with from our its their his her be is are as at into new first great one two three '
           'number not no every each own all'.split())

EFFECT_THEME = {
    'industrial_complex': 'industry factory production', 'arms_factory': 'arms military production', 'dockyard': 'navy ship naval',
    'office': 'economy money market', 'infrastructure': 'construction roads infrastructure', 'agriculture': 'agriculture farming',
    'energy': 'energy power', 'powerplant': 'energy power', 'renewable': 'energy green', 'nuclear': 'nuclear', 'refinery': 'oil',
    'air_base': 'air airforce', 'anti_air': 'air defense', 'radar': 'radar air', 'fuel': 'oil', 'land_facility': 'army research',
    'air_facility': 'air research', 'naval_facility': 'navy research', 'nuclear_facility': 'nuclear research',
}
CAT_THEME = {'CAT_aircraft': 'air aircraft fighters', 'CAT_helicopters': 'helicopter', 'CAT_armor': 'tank tanks armor',
             'CAT_main_battle_tanks': 'tank tanks', 'CAT_surface_ships': 'naval ship navy', 'CAT_submarines': 'submarine navy',
             'CAT_small_arms': 'infantry gun rifle', 'CAT_nuclear': 'nuclear', 'CAT_nuclear_reactors': 'nuclear',
             'CAT_computing': 'science computer research', 'CAT_agriculture': 'agriculture farming', 'CAT_encryption': 'espionage secret',
             'CAT_decryption': 'espionage secret', 'CAT_satellites': 'space science', 'CAT_corvettes': 'naval ship',
             'CAT_destroyers': 'naval ship', 'CAT_heavy_aircraft': 'air aircraft', 'CAT_light_aircraft': 'air aircraft'}
KEY_THEME = {'drift_defence_factor': 'security', 'intel_network_gain_factor': 'espionage intelligence', 'research_speed_factor': 'science research',
             'stability_factor': 'unity', 'political_power_factor': 'government', 'conscription_factor': 'army recruiting',
             'trade_opinion_factor': 'trade', 'tax_gain_multiplier_modifier': 'tax money', 'production_speed_buildings_factor': 'construction',
             'industrial_capacity_factory': 'factory industry', 'agricolture_productivity_modifier': 'agriculture farming',
             'mdcw_cw_ideological_defence': 'propaganda security', 'mdcw_cw_support_effectiveness': 'propaganda diplomacy',
             'foreign_influence_modifier': 'diplomacy', 'war_support_factor': 'propaganda', 'police_cost_multiplier_modifier': 'police security',
             'army_org_factor': 'army', 'army_morale_factor': 'army soldier', 'experience_gain_army_factor': 'army training',
             'social_cost_multiplier_modifier': 'social welfare', 'health_cost_multiplier_modifier': 'health', 'education_cost_multiplier_modifier': 'education',
             'energy_gain_multiplier': 'energy power', 'resource_export_multiplier_modifier': 'mining export trade',
             'productivity_growth_modifier': 'economic production', 'receiving_investment_cost_modifier': 'investments market',
             'return_on_investment_modifier': 'investments money', 'interest_rate_multiplier_modifier': 'money bank',
             'population_tax_income_multiplier_modifier': 'tax money', 'corporate_tax_income_multiplier_modifier': 'tax business',
             'office_park_income_tax_modifier': 'business money', 'agriculture_tax_modifier': 'agriculture farming',
             'military_industry_tax_modifier': 'arms military', 'production_speed_industrial_complex_factor': 'industry factory',
             'production_speed_arms_factory_factor': 'arms military', 'production_speed_infrastructure_factor': 'construction roads',
             'production_speed_agriculture_district_factor': 'agriculture farming', 'production_speed_offices_factor': 'business construction',
             'industrial_capacity_dockyard': 'navy ship', 'production_factory_max_efficiency_factor': 'factory production',
             'production_factory_efficiency_gain_factor': 'factory production', 'monthly_population': 'population family',
             'literacy_rate_education_modifier': 'education school', 'globalism_equilibrium': 'trade market',
             'imp_sanction_resistance': 'economy', 'mdcw_cw_market_exposure': 'trade market', 'mdcw_cw_assistance_limit': 'aid',
             'mdcw_cw_assistance_capacity': 'aid diplomacy', 'mdcw_cw_military_programme_cost': 'military aid',
             'foreign_influence_defense_modifier': 'security', 'intelligence_agency_defense': 'espionage security',
             'encryption_factor': 'espionage', 'decryption_factor': 'espionage', 'required_garrison_factor': 'police security',
             'bureaucracy_cost_multiplier_modifier': 'government bureaucracy', 'corruption_cost_factor': 'corruption',
             'party_popularity_stability_factor': 'party election', 'democratic_drift': 'democracy', 'communism_drift': 'communism',
             'fascism_drift': 'islamic', 'nationalist_drift': 'nationalism', 'neutrality_drift': 'neutrality',
             'army_attack_factor': 'army attack', 'army_defence_factor': 'army defense', 'army_core_defence_factor': 'defense fort',
             'special_forces_cap': 'special forces', 'command_power_gain': 'general command', 'military_factories_productivity': 'arms factory',
             'equipment_conversion_speed': 'equipment', 'defensive_war_stability_factor': 'defense', 'weekly_manpower': 'army recruiting',
             'training_time_army_factor': 'army training', 'personnel_cost_multiplier_modifier': 'army',
             'army_personnel_cost_multiplier_modifier': 'army', 'buildings_worker_requirement_modifier': 'workers construction',
             'consumer_goods_factor': 'consumer goods', 'imp_oil_price_resistance': 'oil', 'experience_gain_navy_factor': 'navy',
             'experience_gain_air_factor': 'air'}
FAC_THEME = {'the_military': 'army military', 'intelligence_community': 'espionage secret', 'labour_unions': 'workers labour',
             'farmers': 'farming agriculture', 'landowners': 'land agriculture', 'the_clergy': 'church clergy', 'the_ulema': 'islamic',
             'the_wahabi_ulema': 'islamic', 'the_priesthood': 'religion', 'industrial_conglomerates': 'industry business',
             'small_medium_business_owners': 'smb business', 'international_bankers': 'money market', 'wall_street': 'money market',
             'defense_industry': 'arms military', 'communist_cadres': 'communist party', 'oligarchs': 'money business',
             'fossil_fuel_industry': 'oil'}
PARTY_THEME = {'W': 'democracy democratic liberal', 'E': 'communism communist socialist red', 'S': 'islamic islam muslim',
               'N': 'neutrality peace', 'R': 'nationalism national'}
PARTY_KEY_THEME = {'wa': 'government general', 'con': 'conservatism', 'lib': 'liberal', 'sd': 'social', 'cs': 'communist',
                   'ac': 'anarchism', 'ce': 'socialist', 'ea': 'revolution', 'mvf': 'islamic', 'vf': 'islamic', 'sk': 'monarchy islamic',
                   'cal': 'islamic', 'mb': 'islamic', 'na': 'government', 'ncon': 'conservatism', 'oli': 'money', 'nlib': 'market',
                   'gr': 'green environment', 'ns': 'socialism', 'nc': 'communism', 'rwp': 'national', 'fas': 'fascist',
                   'jun': 'army general military', 'mon': 'monarchy crown'}


def toks(name):
    parts = re.split(r'[_\W\d]+|(?<=[a-z])(?=[A-Z])', name)
    return [p.lower() for p in parts if p]


def stem(w):
    for suf in ('isation', 'ization', 'ation', 'ings', 'ing', 'ies', 'es', 's'):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)]
    return w


UPPER_OK = {'UN', 'AI', 'TV', 'GDP', 'OK'}


def upper_tag(name):
    parts = [p for p in re.split(r'[_\W\d]+', name) if p]
    if not parts:
        return False
    first = parts[1] if parts[0].lower() in ('focus', 'goal') and len(parts) > 1 else parts[0]
    return first.isupper() and 2 <= len(first) <= 4 and first not in UPPER_OK


def tag_tokens(sprites):
    c = Counter()
    for n, p in sprites:
        if '/goals/00_' in p:
            continue
        t = toks(n)
        if not t:
            continue
        first = t[1] if t[0] in ('focus', 'goal') and len(t) > 1 else t[0]
        if len(first) in (2, 3, 4):
            c[first] += 1
    return {k for k, v in c.items() if v >= 3 and k not in EN3}


def sprite_pool(reserved):
    g = json.load(open(os.path.join(IDX_DIR, 'goal_sprites.json')))
    tags = tag_tokens(g)
    pool = {}
    for n, p in g:
        if n.startswith('GFX_') or n in PHOTOS or n in reserved:
            continue
        if '/goals/00_' not in p or any(x in p for x in EXCL_FOLDERS):
            continue
        t = toks(n)
        if not t or set(t) & BAD_TOKENS or set(t) & COUNTRY_WORDS or set(t) & RELIGION_WORDS:
            continue
        first = t[1] if t[0] in ('focus', 'goal') and len(t) > 1 else t[0]
        if first in tags or upper_tag(n) or any(x in tags for x in t[:3] if len(x) == 3 and x not in EN3):
            continue
        pool[n] = {stem(x) for x in t if x not in ('focus', 'goal', 'generic', 'icon')}
    return pool


def picture_pool(reserved):
    names = [l.strip() for l in open(os.path.join(IDX_DIR, 'idea_gfx.txt')) if l.strip()]
    g = json.load(open(os.path.join(IDX_DIR, 'goal_sprites.json')))
    tags = tag_tokens(g)
    pool = {}
    for n in names:
        if n in reserved:
            continue
        t = toks(n)
        if not t or set(t) & BAD_TOKENS or set(t) & COUNTRY_WORDS or set(t) & RELIGION_WORDS:
            continue
        if t[0] in tags or upper_tag(n) or any(x in tags for x in t[:3] if len(x) == 3 and x not in EN3):
            continue
        if any(x in n for x in ('frame', 'strip', 'layer', 'advisor', 'portrait')):
            continue
        pool[n] = {stem(x) for x in t if x not in ('idea', 'generic', 'spirit')}
    return pool


def keywords(name, fx, outlook, party):
    kw = Counter()
    words = [w for w in toks(name) if w not in STOP]
    for w in words:
        kw[stem(w)] += 3
        for s in SYN.get(w, '').split():
            kw[stem(s)] += 2
    for e in fx:
        t = e[0]
        if t == 'build':
            for k, th in EFFECT_THEME.items():
                if k in e[1]:
                    for s in th.split():
                        kw[stem(s)] += 1
        elif t == 'tech':
            for c in e[1]:
                for s in CAT_THEME.get(c, '').split():
                    kw[stem(s)] += 1
        elif t == 'xp':
            kw[{'army': 'army', 'air': 'air', 'navy': 'navy'}[e[1]]] += 1
        elif t == 'fac' and e[2] > 0:
            for s in FAC_THEME.get(e[1], '').split():
                kw[stem(s)] += 0.8
        elif t == 'prog' and KEY_THEME.get(e[1]) and (e[2] > 0):
            for s in KEY_THEME[e[1]].split():
                kw[stem(s)] += 1.0
        elif t in ('money', 'debt'):
            kw['money'] += 0.5
        elif t == 'tension':
            kw['diplomacy'] += 0.3
    for s in PARTY_THEME.get(outlook, '').split():
        kw[stem(s)] += 0.3
    for s in PARTY_KEY_THEME.get(party or '', '').split():
        kw[stem(s)] += 0.4
    return kw


# sprite words that turn a picture against its subject or are too specific; allowed only if the focus asks for them
NEGATIVE = {'anti', 'attack', 'ban', 'purge', 'arrest', 'arrests', 'drug', 'drugs', 'laundering', 'fueled', 'drinks', 'canned',
            'fish', 'tobacco', 'tea', 'lumber', 'fertiliser', 'lion', 'kaiser', 'wedding', 'female', 'cia', 'mercenary',
            'colonial', 'invasion', 'crisis', 'fire', 'burn', 'dead', 'death', 'kill', 'massacre', 'collapse', 'fall',
            'destroy', 'end', 'against', 'down', 'dangerous', 'gunpoint', 'paradise', 'helicopter', 'npz', 'marnix', 'balken',
            'ultranationalist', 'zombie', 'f', 'mig', 'su', 'mercenaries', 'smuggling', 'black', 'blackmarket'}
IDEOLOGY = {'communist': 'E', 'communism': 'E', 'socialist': 'E', 'socialism': 'E', 'red': 'E', 'marxism': 'E', 'proletarian': 'E',
            'bolshevik': 'E', 'soviet': 'E', 'fascist': 'R', 'fascism': 'R', 'monarchism': 'R', 'monarchy': 'R', 'royal': 'R',
            'crown': 'R', 'king': 'R', 'democracy': 'W', 'democratic': 'W', 'liberal': 'W', 'liberalism': 'W',
            'islamic': 'S', 'islam': 'S', 'muslim': 'S', 'sharia': 'S', 'islamist': 'S', 'christian': 'W', 'church': 'W'}
# which ideology words a party may show (besides its own outlook)
PARTY_IDEOLOGY = {'sd': 'WE', 'ns': 'NE', 'nc': 'NE', 'ac': 'E', 'mb': 'NS', 'mvf': 'ES', 'vf': 'ES', 'sk': 'SR', 'mon': 'R',
                  'jun': 'R', 'fas': 'R', 'rwp': 'R', 'gr': 'NW', 'nlib': 'NW', 'ncon': 'NW', 'na': 'N', 'oli': 'N',
                  'wa': 'W', 'con': 'W', 'lib': 'W', 'cs': 'E', 'ce': 'E', 'ea': 'E', 'cal': 'S'}


def score(kw, tokset, name, party=None, outlook=None):
    s = sum(kw.get(t, 0) for t in tokset)
    if s <= 0:
        return 0
    for t in tokset:
        if t in NEGATIVE and kw.get(t, 0) < 2:
            s -= 6
        o = IDEOLOGY.get(t)
        if o and outlook and o not in (outlook + PARTY_IDEOLOGY.get(party or '', '')) and kw.get(t, 0) < 2:
            s -= 6
        if o == 'R' and t in ('monarchism', 'monarchy', 'royal', 'crown', 'king') and party not in ('mon', 'sk') and kw.get(t, 0) < 2:
            s -= 6
        if o == 'R' and t in ('fascist', 'fascism') and party != 'fas':
            s -= 6
    if s <= 0:
        return 0
    bonus = 0.3 if name.lower().startswith(('focus_generic', 'generic')) else 0
    return s / math.sqrt(max(1, len(tokset))) + bonus


def assign(items, pool, overrides):
    """items: list of (key, Counter keywords, party, outlook). Greedy: most specific first; every sprite once."""
    used = set(overrides.values())
    res = dict(overrides)
    scored = []
    for key, kw, party, outlook in items:
        if key in res:
            continue
        cands = sorted(((score(kw, ts, n, party, outlook), n) for n, ts in pool.items() if n not in used), reverse=True)[:40]
        scored.append((cands[0][0] if cands else 0, key, kw, party, outlook))
    scored.sort(key=lambda x: -x[0])
    for _, key, kw, party, outlook in scored:
        best = None
        bs = -1
        for n, ts in pool.items():
            if n in used:
                continue
            s = score(kw, ts, n, party, outlook)
            if s > bs or (s == bs and n < best):
                best, bs = n, s
        res[key] = best
        used.add(best)
    return res
