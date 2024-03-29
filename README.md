# Edukační scénář do Kybernetické arény

## Zadání

Vytvořte edukační scénář na vybraná témata z aplikované kryptografie, které odpovídají náplní předmětu MPC-KRY. Úloha by měla obsahovat textové zadání (podle potřeby může být doplněno přílohou, např. PDF, ZIP, obrázky apod.), nápovědy k řešení a jednu správnou odpověď. Celý scénář by měl být časově stanoven na 90 minut a zakončen kontrolním testem na 5 minut.

V případě potřeby připravte pro prostředí praktické části scénáře vlastní virtuální stroj(e). Všechny úlohy nemusí nutně vyžadovat virtualizované prostředí a softwarové nástroje, ale k jejich plnění lze využít i otevřené zdroje z internetu nebo mohou být např. výpočetního charakteru. Výsledné řešení bude integrováno do Kybernetické arény.

Projekt naprogramujte ve Vámi zvoleném programovacím jazyku s využitím dostupných knihoven. Podmínkou pro realizaci je návrh scénáře (jednotlivé kroky scénáře a co v nich bude náplní) již v rámci studie projektu, která se odevzdává 6. týden semestru.

## Úkol 1
Tato úloha se zaměřuje na známé útoky na RSA. Jedním takovým útokem je tzv. 'common modulus attack' - útok na společný modulus. Úkolem řešitele bude analyzovat zdojový kód aplikace, naleznout slabinu v implementaci RSA a následně tuto zranitelnost využít k získání vlajky.

Detailní popis úlohy je k nalezení [zde](RSA-challenge/README.md)

## Úkol 2
Tato úloha se zaměřuje na pochopení Diffie-Helman protokolu. Úkolem řešitele bude analyzovat zdrojový kód aplikace, naleznout slabinu v implementaci DH protokolu a následně ji využít k získání vlajky.

Detailní popis úlohy je k nalezení [zde](DH-challenge/README.md)

## Úkol 3

Táto úloha sa zameriava na problematiku slovníkových útokov. Nakoľko je princíp slovníkových útokov relatívne jednoznačný, úloha poukazuje na jednu z mnohých neštandardných implementácii ukladania hesiel užívateľov do databází (solenie hesiel hodnotou známou len servrom, rôzny počet iterácii a pod.). Úlohou riešiteľa bude vyčítať zo zdrojového kódu metódu hashovania hesiel a použiť ju pri realizácii slovníkového útoku voči dostupnému súboru s uniknutými hashmi z databázy. Cracknutie hesla mu umožní sa prihlásiť do webovej aplikácie, kde získa vlajku.

Detailný popis ulohy je možné nájsť [tu](Hash-Cracking/README.md)

## Úkol 4
Tato úloha se zaměřuje na bezpečné generování náhodných čísel. Cílem řešitele je zanalyzovat zdrojový kód aplikace a odhalit únik hodnoty "seed", použité pro generování náhodného názvu souboru s vlajkou. Se znalostí hodnoty seed bude řešitel schopen získat vlajku.

Detailní popis úlohy je k nalezení [zde](RNG-seed/README.md)

## Závěr
Cílem projektu bylo vytvořit edukační scénář na vybraná témata z aplikované kryptografie, které odpovídají náplni předmětu MPC-KRY. Tohoto cíle bylo dosaženo. Součástí řešení je textové zadání úloh, programy realizující jednotlivé úlohy, nápovědy k řešení, jedno správné řešení a závěrečný test.
