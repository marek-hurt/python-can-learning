Small eclipse pydev project for a job interview.

To run it you need to install python can:
**pip install python-can**
see also [python-can documentation](https://python-can.readthedocs.io/en/stable/)

Description in czech lenguage:

Zadání úkolu:
- [x] Ke splnění úkolu použijte knihovnu python-can a jiné nativní knihovny jazyka Python.
- [x] Dokumentaci knihovny python-can naleznete v souboru python-can.pdf
- [x] V jazyce Python vytvořte virtuální simulaci sběrnice CAN Bus.
- [x] Na této sběrnici vytvořte hlavní jednotku, která načte zprávy ze souboru input.blf a každých 100 ms je postupně odešle na sběrnici.
- [x] Ve 2 vedlejších vláknech poté sestrojte 2 jednotky, které přijímají zprávy na sběrnici:
    -první jednotka přijímá pouze zprávy s id 0xC0FFEE nebo 0xCACA0 nebo 0xFF
    -druhá jednotka přijímá pouze zprávy s id 0xBEEF nebo 0xFF
    -zprávy neodpovídající výše zmíněným filterům ignorujte
    -každá tato jednotka zapisuje přijaté zprávy do svého souboru typu .asc
    -při přijetí zprávy s id 0xFF na jednotce:
- [x]     -jednotka přestává přijímat nové zprávy
- [x]      -pro každé id (s výjimkou 0xFF), které vedlejší jednotka do této chvíle přijala, odešle odpověď obsahující počet přijatých zpráv s daným id zpět na sběrnici
Po odeslání všech zpráv z hlavního vlákna jednotka v hlavním vlákně přijme odpovědi z vedlejších jednotek a počty zpráv s jednotlivými id vypíše do konzole.
