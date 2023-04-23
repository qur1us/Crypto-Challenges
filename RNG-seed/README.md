# Popis úlohy

Úloha se skládá z analýzy síťové aplikace a následné rekonstrukce pseudonáhodného názvu souboru obsahujícího vlajku.

Před zpřístupněním aplikace [rng-seed-app](rng-seed-app/) studentovi bude pomocí aplikace [rng-seed-flag](rng-seed-flag/) do aplikace zavedena vlajka a další informace potřebné k jejímu získání.

Student dostane přístup k síťové aplikaci a jejímu zdrojovému kódu. Úkolem bude prozkoumat její funkce a všimnout si možnosti zobrazit její logovací záznamy. V logovacích záznamech se bude nacházet záznam (vytvořený předešlým spuštěním aplikace [rng-seed-flag](rng-seed-flag/)) obsahující informaci o exportování hesel jiného uživatele.

Po zjištění této informace by student měl důkladně zanalyzovat poskytnutý zdrojový kód aplikace a nalézt v něm funkci `generate_secure_filename`, která je odpovědná za vytvoření logovacího záznamu `Random filename generated`. Tato funkce kompromituje bezpečnost generování náhodných názvů souborů tím, že do logu aplikace zaznamenává timestamp použitý jako RNG seed.

Po zjištění této zranitelnosti může student z logu aplikace vyčíst timestamp, který byl použit pro export hesel jiného uživatele. S jeho znalostí může název exportovaného souboru zrekonstruovat a stáhnout si jeho obsah, kterým bude vlajka.

# Nápovědy

1. Prozkoumejte všechny funkcionality aplikace.
2. Využijte poskytnutý zdrojový kód aplikace a podívejte se, jak byly vytvořeny logovací záznamy (MENU volba 9).
3. Funkce generate_secure_filename loguje timestamp, který zároveň používá jako seed pro generování náhodného názvu souboru. Vyčtěte z logu aplikace timestamp "Random filename generated" příslušící uživateli admin. Zjištěné datum a čas převeďte na UNIX timestamp a s pomocí výsledné hodnoty znovu vytvořte název souboru uživatele admin a tento soubor následně z aplikace stáhněte.
4. Bude obsahovat text vlajky.

# Řešení

1. Nalézt možnost výpisu logů aplikace, povšimnout si předešlého exportu hesel uživatele admin
2. Analýzou zdrojového kódu aplikace nalézt funkci `generate_secure_filename`
3. Objevit zranitelnost logování hodnoty timestamp a jejího použití pro RNG seed
4. Vyčíst z logu aplikace datum a čas tvorby náhodného názvu souboru uživatele admin a převést na UNIX timestamp
5. Pomocí získaného UNIX timestamp zrekonstruovat název souboru - lze využít existující kód aplikace `ChaCha20Rng::seed_from_u64(timestamp).next_u64()`
6. Stáhnout obsah daného souboru a tím získat vlajku

Testovací automatizované řešení poskytuje aplikace [rng-seed-solve](rng-seed-solve/).

# Popis aplikací

## rng-seed-app

**Hlavní aplikace úlohy**

Síťová aplikace představující dočasný správce hesel. Uživateli nabízí:
1. Uložení hesel pro danou doménu
2. Export hesel do textového souboru
3. Stažení textového souboru
4. Zobrazení logů aplikace

Po jejím spuštění se spustí `std::net::TcpListener` a vyčkává na připojení klienta. Aplikace podporuje připojení více klientů zároveň - pro každého připojeného klienta je vytvořeno samostatné vlákno vykonávající funkci `handle_client`.

```rust
loop {
	match listener.accept() {
		Ok((socket, addr)) => {
			let logs = Arc::clone(&logs);

			thread::spawn(move || {
				handle_client(socket, addr, logs);
			});
		}
		Err(_) => (),
	}
}
```

Každému připojenému klientovi je vytvořena struktura `ClientSession` obsahující všechny informace potřebné pro obsluhu daného klienta.

```rust
struct ClientSession {
    socket: TcpStream,
    addr: SocketAddr,
    passwords: HashMap<String, HashSet<String>>,
    logs: Arc<Mutex<Vec<String>>>,
}
```

Všechna vlákna společně sdílí proměnnou obsahující vektor textových řetězců, do kterého jsou postupně přidávány logovací záznamy aplikace. Sdílení dat mezi více vlákny je zajištěno pomocí struktury `Arc` a synchronizaci přístupu k těmto datům zajišťuje struktura `Mutex`.

```rust
// Logs shared among all client threads
let logs = Arc::new(Mutex::new(Vec::<String>::new()));
```

V rámci funkce `handle_client` jsou zpracovávány všechny požadavky klienta.

```rust
match &request[..] {
	"1" => client.add_password(),
	"2" => client.export_passwords(),
	"3" => client.download_exported_passwords(),
	"9" => client.download_app_log(),
	"4" => {
		client.send(b"[+] Terminating connection");
		break;
	}
	_ => {
		client.send(b"[!] Unknown option!");
	}
}
```

Funkce `add_password` ukládá hesla pro libovolné domény.
Funkce `export_passwords` exportuje uložená hesla do textového souboru s pseudonáhodným název.
Funkce `download_exported_passwords` umožňuje stáhnout libovolný textový soubor vyskytující se v pracovním adresáři aplikace.
Funkce `download_app_log` klientovi zobrazí logovací záznamy z běhu aplikace.

Cílená zranitelnost aplikace se nachází ve funkci `generate_secure_filename`. Funkce používá aktuální systémový čas ve formátu UNIX timestamp jakožto seed pro generování náhodného názvu souboru. Stejný timestamp ovšem použije i pro logovací zprávu "Random filename generated" a tím jej odhalí všem klientům aplikace.

```rust
fn generate_secure_filename(client: &ClientSession) -> String {
    let timestamp = get_timestamp();

    // Reuse the log timestamp to save resources
    let random = ChaCha20Rng::seed_from_u64(timestamp).next_u64();
    let filename = format!("{random:x}.txt");

    log(
        LogLevel::DEBUG,
        client,
        timestamp,
        String::from("Random filename generated"),
    );

    return filename;
}
```

## rng-seed-flag

**Zavedení vlajky do hlavní aplikace**

Jedná se o pomocnou aplikaci, která dynamicky zavede vlajku do hlavní aplikace [rng-seed-app](rng-seed-app/). Je tedy nutné tuto aplikaci spustit ihned po úspěšném spuštění hlavní aplikace.

Aplikace naváže spojení s hlavní aplikací, vloží do ní nové heslo pro doménu `_FLAG_` obsahující vlajku a provede export hesel.

Mezi jednotlivými žádostmi aplikace jsou vloženy proměnlivě dlouhé intervaly spánku (2,5 až 6 sekund), a to z důvodu simulace chování skutečného člověka. Časové prodlevy jsou totiž následně viditelné řešitelům v záznamech logů aplikace.

Po dokončení  procesu se bude vlajka nacházet v pracovním adresáři hlavní aplikaci, v exportovaném textovém souboru.

## rng-seed-solve

**Automatizované řešení úlohy**

Skrze TCP spojení si vyžádá log záznamy aplikace ve kterých nalezne záznam odpovídající tvorbě náhodného názvu souboru uživatele admin.

Z nalezeného záznamu pomocí regulárního výrazu extrahuje datum a čas, který následně převede na UNIX timestamp.

Získaný timestamp použije pro rekonstrukci názvu souboru uživatele admin.

Následně si od aplikace vyžádá stažení daného souboru a opět s využitím regulárního výrazu extrahuje z odpovědi vlajku.