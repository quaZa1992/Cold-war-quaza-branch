"""Era-specific labels for every MD political slot; no modern-party leakage."""
import re

IDEOLOGIES=['Western_Autocracy','conservatism','liberalism','socialism','communist_state','anarchist_communism','Conservative','Autocracy',
    'Mod_Vilayat_e_Faqih','Vilayat_e_Faqih','Kingdom','Caliphate','Neutral_Muslim_Brotherhood','Neutral_Autocracy','Neutral_conservatism',
    'oligarchism','Neutral_Libertarian','Neutral_green','neutral_Social','Neutral_Communism','Nat_Populism','Nat_Fascism','Nat_Autocracy','Monarchist']

FALLBACK=['Atlanticist Administrators','Traditional Conservatives','Liberal Independents','Social Democrats','Communists','Libertarian Left',
    'Eastern-Aligned Conservatives','Eastern-Aligned Authoritarians','Reformist Shiite Circles','Shiite Clerical Circles','Religious Royalists',
    'Caliphate Supporters','Islamist Circles','Non-Aligned Authoritarians','Non-Aligned Conservatives','Business Notables',
    'Classical Liberals','Environmentalists','Non-Aligned Social Democrats','Non-Aligned Marxists','National Populists','Ultranationalists',
    'Military Officers','Monarchists']

# Each later variant precedes its base in MD's first-match defined_text registry.
# Slot mappings preserve the existing tree/programme gates. They are gameplay
# slots, not claims that Makarios was a Western-aligned party politician.
CYP={
 1:[('','Presidential Coalition — Makarios','An independent presidency backed by changing parliamentary allies, united around Makarios and the defence of the republic.'),
    ('date > 1976.5.11','Presidential Coalition / Democratic Alignment','Spyros Kyprianou announced the Democratic Alignment on 12 May 1976 to support Makarios. The presidency and the new parliamentary organization remain distinct offices.'),
    ('date > 1976.12.3','Presidential Coalition / DIKO','The Democratic Alignment adopted the Democratic Party name on 4 December 1976. Makarios remains the independent president while Spyros Kyprianou leads DIKO.'),
    ('date > 1977.8.2','DIKO — Democratic Party','The Democratic Party represents the presidential centre under Spyros Kyprianou, seeking continuity, international support and a settlement of the Cyprus dispute.')],
 2:[('','Eniaion — United Party','Glafkos Clerides leads the United Party, formed in 1969. The party brings together the republican right of the early 1970s.'),
    ('date > 1976.7.3','DISY — Democratic Rally','Glafkos Clerides founded Democratic Rally on 4 July 1976. The party brings together the republican right around Clerides and a negotiated settlement.')],
 3:[('','EDEK — United Democratic Union of Centre','Vassos Lyssarides\'s movement emerged in 1969 and held its founding congress on 3 May 1970. The contemporary EDEK name predates the later Movement for Social Democracy name.'),
    ('date > 1974.4.30','EDEK — Socialist Party','EDEK adopted socialist terminology at its second congress in April 1974, combining democratic socialism with resistance to the coup and the partition of Cyprus.')],
 4:[('','AKEL — Progressive Party of Working People','AKEL is the established Cypriot communist party, led by Ezekias Papaioannou. Its programme emphasizes organized labour, public services and Cypriot independence.')],
 20:[('','Progressive Front — Proodeftiki Parataxis','Nikos Sampson\'s nationalist electoral organization is distinct from the underground armed organizations and from the National Guard.')],
 21:[('','Armed Enosis Movement','Armed opponents of Makarios include the National Front. Their pursuit of Enosis challenges presidential authority and divides the security forces.'),
     ('date > 1971.8.31','EOKA B / Enosis Hardliners','The later armed Enosis underground includes EOKA B following Grivas\'s 1971 return. This is an armed political current, not a normal parliamentary party; its later government is alternate history.')],
 22:[('','National Guard Officers','National Guard officers occupy a powerful position between the elected presidency, mainland military influence and competing visions of the island\'s future.'),
     ('has_country_flag = COLDWAR_CYP_1970_coup_regime_active','National Guard Coup Regime','An actually established military coup administration. Officer politics, the Greek sponsor\'s choices and the results of a coup remain separate from this displayed name.')]
}

NCY={
 1:[('','Turkish Cypriot Communal Executive','The communal executive is led by Fazıl Küçük at the 1970 starting point. This is a separate administration within the divided constitutional framework, not a pre-existing sovereign Northern Cyprus.'),
    ('date > 1973.2.27','Turkish Cypriot Communal Administration','Rauf Denktaş took the vice-presidential oath and the leadership of the Turkish Cypriot administration on 28 February 1973. A local administration is not equivalent to international recognition.'),
    ('date > 1975.10.10','UBP — National Unity Party','Ulusal Birlik Partisi was founded on 11 October 1975. Rauf Denktaş\'s presidency is distinct from the successive party chairmanships and premierships of Konuk, Örek, Çağatay and Eroğlu.')],
 2:[('','Liberal Constitutional Independents','Independent constitutional reformers seek representative government, civil liberties and a negotiated communal framework.')],
 3:[('','Turkish Cypriot Democratic Opposition','The opposition tendency predates an organized CTP. Ahmet Mithat Berberoğlu\'s Republican Turkish Party is founded only on 27 December 1970.'),
    ('date > 1970.12.26','CTP — Republican Turkish Party','Cumhuriyetçi Türk Partisi was founded on 27 December 1970. Ahmet Mithat Berberoğlu is its first chair; Özker Özgür leads the later 1976–1996 period. The party advocates democratic representation, workers\' rights and a negotiated settlement.')],
 18:[('','Communal Social-Democratic Independents','The social-democratic opposition is represented as independent currents before the creation of TKP.'),
     ('date > 1976.3.17','TKP — Communal Liberation Party','Toplumcu Kurtuluş Partisi was founded on 18 March 1976 under Alpay Durduran. Later leaders include İsmail Bozkurt and Mustafa Akıncı. The party draws on communal social democracy and support for a federal settlement.')],
 22:[('','TMT — Resistance Organization Command','The Turkish Resistance Organization has Turkish officers serving as Bayraktars and local Turkish Cypriot forces. It is distinct from Turkey\'s invasion corps and from the later Security Forces Command.'),
     ('date > 1976.7.31','GKK — Security Forces Command','Güvenlik Kuvvetleri Komutanlığı was established on 1 August 1976. Its dated commander roster is separate from the Turkish army\'s intervention command; military rule remains an alternate political outcome.')]
}


def variants(tag,index):
    authored=(CYP if tag=='CYP' else NCY).get(index)
    if authored:return authored
    country='Cypriot' if tag=='CYP' else 'Turkish Cypriot'
    return [('',country+' '+FALLBACK[index],
        'A loosely organized alternate political current seeking influence within the community and a platform of its own.')]


def integrate_party_names(c,text):
    text=re.sub(r'(?m)^.*# COLDWAR (?:CYP1970|CYPRUS PARTY)[^\n]*\n','',text)
    native=(c.ROOT/'localisation/english/0_political_system_l_english.yml').read_text(encoding='utf-8-sig')
    icons={m[1]:m[2] for m in re.finditer(r'generic\.([^\s:]+)_icon:\s*"([^"]*)"',native)}
    catalog=[]
    for tag in ('CYP','NCY'):
        for index,ideology in enumerate(IDEOLOGIES):
            assert ideology in icons,ideology
            rows=variants(tag,index);catalog.append({'tag':tag,'index':index,'ideology':ideology,'variants':rows})
            for suffix in ('','_desc','_icon'):
                needle='name = '+ideology+'_L'+suffix+'\n';assert needle in text,needle
                lines=[]
                for variant,(extra,label,desc) in reversed(list(enumerate(rows))):
                    key=f'COLDWAR_{tag}_1970_party_{index}'+('' if variant==0 else '_v'+str(variant))+suffix
                    value=desc if suffix=='_desc' else icons[ideology] if suffix=='_icon' else icons[ideology]+' '+label
                    c.loc(key,value)
                    trigger='original_tag = '+tag+' IMP_is_1970_scenario = yes'+(' '+extra if extra else '')
                    lines.append('\ttext = { trigger = { '+trigger+' } localization_key = '+key+' } # COLDWAR CYPRUS PARTY')
                text=text.replace(needle,needle+'\n'.join(lines)+'\n',1)
    c.write('tools/cyprus_1970/party_catalog.json',__import__('json').dumps(catalog,indent=2,ensure_ascii=False)+'\n')
    return text
