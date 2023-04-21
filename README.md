# Edukační scénář do Kybernetické arény

## Zadání

Vytvořte edukační scénář na vybraná témata z aplikované kryptografie, které odpovídají náplní předmětu MPC-KRY. Úloha by měla obsahovat textové zadání (podle potřeby může být doplněno přílohou, např. PDF, ZIP, obrázky apod.), nápovědy k řešení a jednu správnou odpověď. Celý scénář by měl být časově stanoven na 90 minut a zakončen kontrolním testem na 5 minut.

V případě potřeby připravte pro prostředí praktické části scénáře vlastní virtuální stroj(e). Všechny úlohy nemusí nutně vyžadovat virtualizované prostředí a softwarové nástroje, ale k jejich plnění lze využít i otevřené zdroje z internetu nebo mohou být např. výpočetního charakteru. Výsledné řešení bude integrováno do Kybernetické arény.

Projekt naprogramujte ve Vámi zvoleném programovacím jazyku s využitím dostupných knihoven. Podmínkou pro realizaci je návrh scénáře (jednotlivé kroky scénáře a co v nich bude náplní) již v rámci studie projektu, která se odevzdává 6. týden semestru.

## Úkol na RSA
Program realizující tuto úlohu vygeneruje dvě prvočísla, každé o velikosti 4096 bitů, z nich je následně vypočítán modulus. Alice a Bob si zvolí veřejné klíče, jako veřejné klíče byla zvolena dvě Fermatova prvočísla - 65537 a 257. Pro Alici a Boba je následně vytvořen i privátní klíč. Privátní klíče nejsou využity, jejich generování v programu však není nadbytečné. Pro řešitele se jedná o jasnou indíciji, že se jedná o RSA. Vlajka je poté zašifrována veřejným klíčem Alice i Boba, řešitel obdrží modulus, veřejné klíče Alice a Boba, šifrové texty Alice a Boba.

Zranitelnost programu spočívá v tom, že Alice a Bob používají stejný modulus a odesílají stejnou zprávu, díky této skutečnosti a také díky tomu, že veřejné klíče Alice a Boba jsou nesoudělná, je možné pomocí rozšířeného Euklidova algoritmu získat zprávu v otevřeném textu.

### Důkaz zranitelnosti

Mějme tajnou zprávu $M$, veřejné klíče $e_1$, $e_2$ a šifrové texty $c_1 = M^{e_1}$, $c_2 = M^{e_2}$.
Pokud $e_1$ a $e_2$ jsou nesoudělná, tedy gcd($e_1$, $e_2$) = 1.

Pak platí:
$$xe_1 + ye_2 = 1$$
Potom:
$$c_1^x \cdot c_2^y = (M^{e_1})^x \cdot (M^{e_2})^y = M^{e_1x} \cdot M^{e_2y}=M^{e_1x + e_2y} = M^1$$

## Úkol na DH
Program realizující tuto úlohu vygeneruje prvočíslo ($p$) o velikosti 2048 bitů, zvolí generátor ($g = 7$), náhodně zvolí tajný DH parametr ($a$) a vypočítá veřejný parametr ($A = g^a$). Od řešitele obdrží veřejný parametr ($B$). Následně vypočítá hodnotu tajného klíče $k = B^a$. Všechny výpočty jsou modulo ($p$). Tajným klíčem pak zašifruje vlajku a odešle ji řešiteli.

Zranitelnost programu spočívá v tom, že program neověřuje hodnotu $B$. Řešitel může odeslat takové $B$, aby hodnota $k$ byla taková, kterou bude schopen získat bez znalosti $A$ nebo $a$. Odeslat může $B = 0$, pak $k = B^a = 0^a = 0$, nebo $B = 1$, pak  k = B^a = 1^a = 1$. Pomocí $k$ pak může dešifrovat obdrženou zprávu a získat tak vlajku.

## Závěr
Cílem projektu bylo vytvořit edukační scénář na vybraná témata z aplikované kryptografie, které odpovídají náplni předmětu MPC-KRY. Tohoto cíle bylo dosaženo. Součástí řešení je textové zadání úloh, programy realizující jednotlivé úlohy, nápovědy k řešení, jedno správné řešení a závěrečný test.
