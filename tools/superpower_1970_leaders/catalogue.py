# IMPERIA COLD WAR — Researched USA and Soviet political candidate catalogue.
"""Historical identities and native MD affiliations, with explicit requested exceptions."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def person(tag, key, name, slots, note, title=None, profile=None, standin=False, aliases=()):
    return dict(tag=tag, key=key, name=name, slots=list(slots), description=note,
                wikipedia_title=title or name, profile=profile, standin=standin,
                aliases=list(aliases), source_urls=['https://en.wikipedia.org/wiki/' + (title or name).replace(' ', '_')])


PEOPLE = []
def usa(key, name, slots, note, title=None):
    PEOPLE.append(person('USA', key, name, slots, note, title))
def sov(key, name, slots, note, title=None, profile=None, standin=False, aliases=()):
    PEOPLE.append(person('SOV', key, name, slots, note, title, profile, standin, aliases))

# Republicans, their principal presidential challengers and alternatives.
usa('richard_nixon', 'Richard Nixon', (1,), 'Republican president associated with detente, executive government and the Watergate crisis.')
usa('gerald_ford', 'Gerald Ford', (1,), 'Republican congressional leader and president, associated with institutional continuity after Watergate.')
usa('ronald_reagan', 'Ronald Reagan', (1,), 'California governor and Republican president, representing the conservative movement.')
usa('george_h_w_bush', 'George H. W. Bush', (1,), 'Republican diplomat, intelligence director, vice president and president.')
usa('bob_dole', 'Bob Dole', (1,), 'Republican Senate leader, vice-presidential nominee and presidential challenger.')
usa('nelson_rockefeller', 'Nelson Rockefeller', (1,), 'New York governor and vice president, representing the liberal Republican tradition.')
usa('barry_goldwater', 'Barry Goldwater', (1,), 'Arizona senator and an influential leader of Republican conservatism.')
usa('john_anderson', 'John B. Anderson', (1,), 'Republican congressman who later mounted an independent presidential campaign.', 'John B. Anderson')
usa('howard_baker', 'Howard Baker', (1,), 'Tennessee senator and Republican Senate leader, associated with congressional negotiation.')
usa('jack_kemp', 'Jack Kemp', (1,), 'Republican congressman, supply-side tax advocate and vice-presidential nominee.')
usa('pat_buchanan', 'Pat Buchanan', (1, 20), 'Republican presidential challenger and Reform Party candidate, associated with economic nationalism.')
usa('colin_powell', 'Colin Powell', (1,), 'Senior military officer and national political figure considered for a Republican presidential campaign. This selection grants no military command.')

# Democrats, opposition figures, presidential nominees and primary alternatives.
usa('hubert_humphrey', 'Hubert Humphrey', (2,), 'Democratic senator, vice president and presidential nominee, associated with liberal reform and civil rights.')
usa('george_mcgovern', 'George McGovern', (2,), 'Democratic senator and presidential nominee, associated with opposition to the Vietnam War.')
usa('edmund_muskie', 'Edmund Muskie', (2,), 'Maine senator, Democratic vice-presidential nominee and presidential contender.')
usa('henry_jackson', 'Henry M. Jackson', (2,), 'Democratic senator combining domestic liberalism with a firm position toward the Soviet Union.', 'Henry M. Jackson')
usa('ted_kennedy', 'Ted Kennedy', (2,), 'Massachusetts senator and Democratic presidential challenger, associated with social legislation.')
usa('eugene_mccarthy', 'Eugene McCarthy', (2,), 'Democratic senator and anti-war presidential challenger, later an independent candidate.')
usa('shirley_chisholm', 'Shirley Chisholm', (2,), 'Congresswoman, civil-rights advocate and Democratic presidential contender.')
usa('mo_udall', 'Mo Udall', (2,), 'Arizona congressman and Democratic presidential contender, associated with conservation and political reform.')
usa('jimmy_carter', 'Jimmy Carter', (2,), 'Georgia governor and Democratic president, associated with human rights and energy policy.')
usa('walter_mondale', 'Walter Mondale', (2,), 'Democratic senator, vice president and presidential nominee.')
usa('gary_hart', 'Gary Hart', (2,), 'Colorado senator and Democratic presidential contender associated with a younger reform current.')
usa('jesse_jackson', 'Jesse Jackson', (2,), 'Civil-rights leader and Democratic presidential contender associated with the Rainbow Coalition.')
usa('michael_dukakis', 'Michael Dukakis', (2,), 'Massachusetts governor and Democratic presidential nominee.')
usa('jerry_brown', 'Jerry Brown', (2,), 'California governor and Democratic presidential challenger with an independent reform reputation.')
usa('paul_tsongas', 'Paul Tsongas', (2,), 'Massachusetts senator and Democratic presidential contender associated with fiscal and industrial policy.')
usa('bill_clinton', 'Bill Clinton', (2,), 'Arkansas governor and Democratic president associated with the New Democrat current.')
usa('al_gore', 'Al Gore', (2,), 'Democratic senator, presidential contender and vice president, associated with environmental and technology policy.')

# Significant independent, communist and libertarian alternatives.
usa('george_wallace', 'George Wallace', (2, 20), 'Alabama governor, segregationist politician and independent presidential candidate who also contested Democratic primaries.')
usa('ross_perot', 'Ross Perot', (20,), 'Independent presidential challenger and Reform Party founder associated with deficit reduction and trade policy.')
usa('gus_hall', 'Gus Hall', (4,), 'Communist Party USA leader and recurring presidential candidate.')
usa('angela_davis', 'Angela Davis', (4,), 'Communist activist and vice-presidential candidate, associated with civil rights and prison reform.')
usa('john_hospers', 'John Hospers', (16,), 'Philosopher and the first Libertarian Party presidential nominee.')
usa('ed_clark', 'Ed Clark', (16,), 'Lawyer and Libertarian Party presidential nominee.')
usa('david_bergland', 'David Bergland', (16,), 'Libertarian activist and presidential nominee.')
usa('ron_paul', 'Ron Paul', (1, 16), 'Congressman and Libertarian presidential nominee, associated with constitutional limits and monetary policy.')
usa('andre_marrou', 'Andre Marrou', (16,), 'Former Alaska legislator and Libertarian presidential nominee.')
usa('harry_browne', 'Harry Browne', (16,), 'Writer and Libertarian presidential nominee associated with smaller federal government.')
usa('ralph_nader', 'Ralph Nader', (17,), 'Consumer-rights advocate and Green presidential candidate during the 1990s.')
usa('bernie_sanders', 'Bernie Sanders', (3,), 'Independent democratic socialist, Burlington mayor and member of the House of Representatives during the 1990s. This selection represents the socialist current, not a Democratic presidential primary campaign.')

# Every named general-secretary path and its existing stand-in, kept distinct.
sov('leonid_brezhnev', 'Leonid Brezhnev', (4,), 'General Secretary and representative of the stability-of-cadres leadership.', profile='bre')
sov('alexei_kosygin', 'Alexei Kosygin', (4,), 'Chairman of the Council of Ministers and advocate of economic reform.', profile='kos')
sov('nikolai_ryzhkov', 'Nikolai Ryzhkov', (4,), 'Industrial administrator and Chairman of the Council of Ministers during perestroika.', profile='kos', standin=True)
sov('nikolai_podgorny', 'Nikolai Podgorny', (4,), 'Chairman of the Presidium of the Supreme Soviet and senior party figure.', profile='pod')
sov('vasily_kuznetsov', 'Vasily Kuznetsov', (4,), 'Diplomat and senior Presidium official, associated with continuity in the state apparatus.', profile='pod', standin=True)
sov('mikhail_suslov', 'Mikhail Suslov', (4, 6), 'Senior party ideologue associated with orthodox communist doctrine.', profile='sus')
sov('mikhail_zimyanin', 'Mikhail Zimyanin', (4,), 'Pravda editor and Central Committee secretary responsible for ideological work.', profile='sus', standin=True)
sov('alexander_shelepin', 'Alexander Shelepin', (4, 7), 'Former Komsomol and KGB leader associated with the party control apparatus.', profile='she')
sov('yuri_andropov', 'Yuri Andropov', (4,), 'KGB chairman and General Secretary associated with discipline and administrative renewal.', profile='and')
sov('heydar_aliyev', 'Heydar Aliyev', (4,), 'Azerbaijani party leader and senior Union official with a security-service background.', profile='and', standin=True)
sov('andrei_grechko', 'Andrei Grechko', (4, 22), 'Marshal and defence minister associated with the military establishment.', profile='gre')
sov('nikolai_ogarkov', 'Nikolai Ogarkov', (4, 22), 'Marshal and Chief of the General Staff associated with military modernization.', profile='gre', standin=True)
sov('dmitry_ustinov', 'Dmitry Ustinov', (4,), 'Defence-industry administrator and defence minister.', profile='ust')
sov('leonid_smirnov', 'Leonid Smirnov', (4, 13), 'Senior defence-industry administrator and head of the Military-Industrial Commission.', 'Leonid Smirnov', profile='ust', standin=True)
sov('grigory_romanov', 'Grigory Romanov', (4,), 'Leningrad party leader and conservative candidate within the Soviet leadership.', profile='gro')
sov('konstantin_chernenko', 'Konstantin Chernenko', (4,), 'General Secretary associated with the central party apparatus.', profile='che')
sov('viktor_grishin', 'Viktor Grishin', (4,), 'Moscow party leader and senior Politburo figure.', profile='che', standin=True)
sov('mikhail_gorbachev', 'Mikhail Gorbachev', (4, 18), 'General Secretary and Soviet president associated with perestroika and political reform.', profile='gor')

# Existing non-CPSU path representatives. Their hypothetical governments are RP alternatives.
sov('dzhermen_gvishiani', 'Dzhermen Gvishiani', (0,), 'Science administrator and systems-analysis specialist. A technocratic political alternative is hypothetical.')
sov('vladimir_poremsky', 'Vladimir Poremsky', (1,), 'Leader of the anti-Soviet exile organization NTS. His return to government is an alternate-history outcome.')
sov('andrei_sakharov', 'Andrei Sakharov', (2,), 'Physicist, human-rights dissident and democratic opposition deputy.')
sov('roy_medvedev', 'Roy Medvedev', (3,), 'Dissident historian associated with democratic socialist criticism of Soviet rule.')
sov('pyotr_siuda', 'Pyotr Siuda', (5,), 'Worker activist, Novocherkassk eyewitness and anarcho-syndicalist. Distinct from the modern Polish sociologist Piotr Siuda.', 'Pyotr Siuda')
sov('sergei_trapeznikov', 'Sergei Trapeznikov', (6,), 'Central Committee science and education official associated with ideological conservatism.')
sov('nikolai_baibakov', 'Nikolai Baibakov', (13,), 'Long-serving Gosplan chairman and representative of the planning administration.')
sov('aleksandr_solzhenitsyn', 'Aleksandr Solzhenitsyn', (14,), 'Writer, dissident and critic of communist rule. A government under his leadership is hypothetical.')
sov('nikolai_shchelokov', 'Nikolai Shchelokov', (15,), 'Interior minister and a figure of the late Soviet administrative establishment.')
sov('nikolai_shmelyov', 'Nikolai Shmelyov', (16,), 'Economist and writer associated with market-oriented criticism of the Soviet economy.')
sov('grigory_galazy', 'Grigory Galazy', (17,), 'Limnologist and campaigner for Lake Baikal. An ecological government under his leadership is hypothetical.', 'Grigory Galaziy')
sov('alexander_yakovlev', 'Alexander Yakovlev', (18,), 'Diplomat and senior reformer associated with glasnost and political renewal.', 'Alexander Yakovlev (Russian politician)')
sov('pyotr_shelest', 'Pyotr Shelest', (19,), 'Ukrainian party leader associated with republican economic and cultural interests.', 'Petro Shelest')
sov('dmitry_polyansky', 'Dmitry Polyansky', (20,), 'Senior party and agricultural administrator associated with the Soviet conservative establishment.')
sov('vladimir_kirillovich', 'Grand Duke Vladimir Kirillovich', (23,), 'Romanov claimant living in exile. The succession claim was contested; restoration is an alternate-history choice.', 'Grand Duke Vladimir Kirillovich of Russia', aliases=('Emperor Vladimir III', 'Vladimir Kirillovich'))

# Reformers, opposition politicians and challengers through the 1990s.
sov('boris_yeltsin', 'Boris Yeltsin', (2,), 'Soviet reform opposition figure and later Russian president.')
sov('yegor_ligachev', 'Yegor Ligachev', (4, 6), 'Senior party secretary and opponent of the direction taken by perestroika.')
sov('yegor_gaidar', 'Yegor Gaidar', (16,), 'Economist and Russian reform-government leader associated with rapid market transformation.')
sov('grigory_yavlinsky', 'Grigory Yavlinsky', (2, 16), 'Economist, Yabloko leader and liberal opposition presidential candidate.')
sov('boris_nemtsov', 'Boris Nemtsov', (2,), 'Regional governor, reform politician and liberal opposition figure.')
sov('anatoly_sobchak', 'Anatoly Sobchak', (2,), 'Democratic reform deputy and mayor of Saint Petersburg.')
sov('gavriil_popov', 'Gavriil Popov', (2,), 'Economist, democratic opposition deputy and mayor of Moscow.')
sov('vladimir_zhirinovsky', 'Vladimir Zhirinovsky', (20,), 'LDPR leader and nationalist opposition presidential candidate.')
sov('gennady_zyuganov', 'Gennady Zyuganov', (4, 6), 'Communist opposition leader and presidential candidate during the 1990s.')
sov('alexander_rutskoy', 'Alexander Rutskoy', (20, 22), 'Military aviator, Russian vice president and opponent of Yeltsin during the constitutional crisis.')
sov('alexander_lebed', 'Alexander Lebed', (20, 22), 'General and presidential candidate associated with order, security and opposition to the political establishment.')
sov('vladimir_kryuchkov', 'Vladimir Kryuchkov', (4, 22), 'KGB chairman and participant in the State Committee on the State of Emergency.')
sov('gennady_yanayev', 'Gennady Yanayev', (4, 22), 'Soviet vice president and leading participant in the August emergency committee.')
sov('yevgeny_primakov', 'Yevgeny Primakov', (13,), 'Diplomat, intelligence official and later Russian prime minister associated with state-centered pragmatism.')
sov('maria_vladimirovna', 'Maria Vladimirovna', (23,), 'Romanov claimant whose position is disputed by other members of the dynasty. A restoration remains a political choice.', 'Grand Duchess Maria Vladimirovna of Russia')
sov('viktor_anpilov', 'Viktor Anpilov', (6,), 'Hardline communist activist and leader of Labour Russia.')
sov('viktor_tyulkin', 'Viktor Tyulkin', (6,), 'Communist Workers Party leader associated with orthodox communist opposition.')
sov('yury_luzhkov', 'Yury Luzhkov', (15,), 'Moscow mayor and leader of a political and administrative opposition coalition during the 1990s.')
sov('vladimir_putin', 'Vladimir Putin', (13,), 'Security-service director and Russian prime minister in 1999, followed by the acting presidency. This alternative represents the state-administrative current. It grants no intelligence operative.')

# IMPERIA COLD WAR — User-requested Lukashenko exception to undated selections.
sov('alexander_lukashenko', 'Alexander Lukashenko', (4, 6), 'Belarusian Soviet political organizer and agricultural administrator, later a parliamentary deputy and advocate of state-led economic policy. His appointment to Union leadership is an alternative political outcome.')
PEOPLE[-1]['available_from']=json.loads((HERE.parent/'lukashenko_1970/config.json').read_text(encoding='utf8'))['available_from']
PEOPLE[-1]['source_urls']=['https://president.gov.by/en/president/biography/full']


def main():
    assert len({(r['tag'], r['key']) for r in PEOPLE}) == len(PEOPLE)
    (HERE / 'catalogue.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR',
        'policy': 'Candidates have no calendar or tenure locks unless the user explicitly requested an exception. Lukashenko has an available_from year; all earlier entries retain their undated policy.',
        'people': PEOPLE}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print({tag: len([r for r in PEOPLE if r['tag'] == tag]) for tag in ('USA', 'SOV')})


if __name__ == '__main__':
    main()
