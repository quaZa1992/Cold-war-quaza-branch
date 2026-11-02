IMPERIA COLD WAR: Greek political candidates and portraits.

The player selects Greek political representatives with the same native decision pattern used by Sheep's US Republican/Democratic and German CDU/SPD candidate tools. Categories belong to the governing native MD party. Each candidate has a portrait icon, zero selection cost and repeatable access. The effect checks the real country, 1970 campaign, human controller and party again when it executes. Selecting the incumbent is a no-op.

All political candidates are available from the start, including the roster's politicians of the 1990s. There are no political date, retirement, death or term windows. Historical dates are research context only. Dates never appoint a government or force a coup, election or succession. Existing army, navy and air-service recruitment windows are separate from this political selector and are retained.

There are 36 character definitions, 20 additions to the earlier Greek roster, 29 distinct selectable representatives and 31 party/candidate choices. All twenty additions have new portraits restored from identified photographs using the built-in image_gen tool and the requested phone-photo prompt. The separate modern-bookmark textures remain unchanged. Tsatsos and Sartzetakis are constitutional advisers; the regent Zoitakis and president Gizikis retain their separate adviser roles.

Candidates by native political family:

- Conservatives: Panagiotis Kanellopoulos, Konstantinos Karamanlis, Georgios Rallis, Evangelos Averoff, Konstantinos Mitsotakis, Miltiadis Evert, Tzannis Tzannetakis, Konstantinos Stephanopoulos and Kostas Karamanlis.
- Liberal Centre: Georgios Mavros and Konstantinos Mitsotakis.
- Socialists: Andreas Papandreou and Costas Simitis.
- Communist and democratic left: Kostas Koligiannis, Charilaos Florakis, Grigoris Farakos, Babis Drakopoulos, Leonidas Kyrkos, Maria Damanaki, Nikos Konstantopoulos and Aleka Papariga.
- Military government: Georgios Papadopoulos, Dimitrios Ioannidis, Odysseas Angellis, Grigorios Bonanos, Spyros Markezinis, Adamantios Androutsopoulos and Stylianos Pattakos.
- Royalists: Constantine II.
- Independent caretaker: Xenophon Zolotas.
- Civilian administration: Spyros Markezinis.

These native MD slots represent selectable political affiliations. Markezinis and Androutsopoulos were civilian prime ministers under military rule; their selection does not claim that they were the junta's de facto commanders. The left branch already includes renewal and broad-front alternatives. Selecting Drakopoulos/Kyrkos displays the renewal tradition; selecting Damanaki/Konstantopoulos displays Synaspismos. No invented religious party or extra focus branch is added.

The earlier generic party programmes accept any selected representative of their own party. Personal Papadopoulos, Ioannidis and royal conditions remain personal. An immediate existing programme-owner callback reconciles a leader change; the new tree remains the separate approval-stage concept. No focus rewards, assets, setup fees or budgets were rebalanced by this leadership change.

The current choice is saved separately for each party, including candidates with multiple affiliations. Legacy focus/event selected-person flags are adopted. No daily or weekly roster observer is used: startup and one local Greek monthly reconciliation suffice, alongside the existing native leader dispatcher. No country/state scans are added.

Build and validate from the mod root:

```powershell
python tools/greece_1970_leaders/build.py
python tools/greece_1970_leaders/validate.py
```

The regional compiler delegates its Greek output to this owner. The old regional asset builder restores these additions after its default production build. The old Greek tree compiler applies only the small party-representative compatibility adapter when generating its own runtime. Running either broad compiler is unnecessary for this scoped update.

`VALIDATION.json` contains the actual static and interpreted-script results. It does not establish live portrait rendering, MD trait execution, multiplayer synchronization or save/rehost behavior. `PORTRAIT_REVIEW.png` is a technical asset contact sheet, not a game screenshot. Full image prompts, source metadata, unknown permissions and credits are recorded in `generation.json`, `source_inventory.json` and `ASSET_NOTICE.md`.

Historical references, consulted 30 October 2026:

- [New Democracy's own history](https://nd.gr/politikos-organismos/istoria/): conservative leadership and political context.
- [Greek Prime Minister's Office: Mitsotakis](https://www.primeminister.gr/prime-minister/konstantinos-mitsotakis): Centre background, later ND leadership and premiership.
- [Greek Prime Minister's Office: Tzannetakis](https://www.primeminister.gr/prime-minister/tzannis-tzannetakis): anti-dictatorship record and coalition premiership.
- [Hellenic Parliament's illustrated institutional history](https://www.hellenicparliament.gr/UserFiles/8c3e9046-78fb-48f4-bd82-bbba28ca1ef5/vouli_en_low_28_1_09.pdf): presidents and prime ministers, PDF pages 26-29.
- [Presidency: Stephanopoulos](https://www.presidency.gr/en/konstantinos-stephanopoulos/): ND, DIANA and constitutional office.
- [European Parliament: Damanaki's CV](https://www.europarl.europa.eu/meetdocs/2009_2014/documents/pech/dv/damanaki_cv_/damanaki_cv_en.pdf): anti-dictatorship, parliamentary and Synaspismos roles.
- [European Parliament: Kyrkos](https://www.europarl.europa.eu/meps/en/1677/LEONIDAS_KYRKOS/history/2): identified MEP and contemporary portrait.
- [SearchCulture: Babis Drakopoulos](https://www.searchculture.gr/aggregator/edm/pandektis_prosopa/000085-10442_58993?language=en): KKE Interior secretary identity.
- [KKE press: the 1989-1991 leadership changes](https://www.rizospastis.gr/page.do?pageNo=20&publDate=27%2F2%2F2021): Farakos and Papariga succession context. These dates are not runtime restrictions.
- [Farakos's captioned Budapest photograph](https://www.efsyn.gr/arheio/fantasma-tis-istorias/51650_i-agnosti-allagi-igesias-toy-kke/): the rightmost man is Farakos, not Koligiannis.

The selection policy deliberately permits alternate histories, including the early selection of politicians associated with later decades. Research identifies each person and political tradition; it does not impose their historical tenure on the player.
