# chia_send_mail
 Chia-Email-Benachrichtigung

Achtung, dieses Tool funktioniert nur mit Linux!

Mit diesem Tool ist es möglich, sich automatisiert mithilfe von crontab sich E-Mail Benachrichtigungen über neu eingangene TXCH Coins senden zu lassen.

Anleitung:

- Packe diese Datei auf deinem Linux Gerät am besten im Home Verzeichnis.
- Erstelle wenn noch nicht vorhanden dir ein Google Mail Account.
- Speichere das Passwort dieses Mail Accounts in eine Datei Namens pw.txt packe diese in ein Verzeichnis Namens google_pw welches wiederum im root Verzeichnis ist.
(/root/google_pw/pw.txt)
- Öffne dieses Tool mit einem Editor deiner Wahl, suche und ersetze dort DEINE-SENDER_EMAIL und DEINE-EMPFÄNGER-EMAIL jeweils 2x
- Als letztes erstelle dir ein crontab, welches regelmäßig, z.b. alle 10 min. dieses Tool ausführt.