import smtplib, ssl # Importiert die Bibliothek smtplib und die Verschlüsselung ssl
import os # Wählt das Betriebssystem aus

# Hier wird ein SMTP Server erstellt, genauer gesagt SMTPlib. Welcher in der Lage sein wird über den erstellten Google Account
# eine E-Mail an der eingetragenen Empfängeradresse zu senden.
# Sinn und zweck des ganzen Programms ist es, das wir wir eine Verbindung zwischen Chia-Blockchain auf dem Raspberry Pi und dem SMTP
# herstellen. Wir leiten mit Python, eine Chia abfrage weiter an eine Log Datei. Dann findet ein Abgleich statt. Hat es eine Veränderung
# mit der vorherigen Datei gegeben oder existierte vorher noch keine Datei, so wird entweder eine neue Datei mit der Abfrage erstellt
# oder aber die neue Datei mit der alten ersetzt. Ist dem so, so wird der Inhalt dieser neuen log Datei in eine E-Mail gepackt und an dem
# Empfänger gesendet.
# Findet keine Veränderung statt, so wird auch nichts überschrieben und auch keine E-mail gesendet.
# Ich habe den Code so geschrieben, dass auch ein kleiner positiver Nebeneffekt eintritt. Sollte es z.B. bei der Chia Abfrage zu einem Fehler
# bekommen so bekommen wir auch darüber eine Nachricht per E-Mail gesandt und auch Meldung darüber, ob wieder alles funktioniert.
# Das liegt daran, dass bei einer Veränderung, das immer die E-Mail mit dem neuen Inhalt versendet wird, nicht der alte.
# In Verbindung mit crontab auf Linux gibt so etliche Möglichkeiten die sich dadurch ergeben. 



if os.path.isdir('/home/sendmail'):
    if os.path.isfile('/home/sendmail/status_1.txt') == False: # Ist die Datei status_1.txt schon vorhanden wird die Datei geöffnet
        os.system('touch /home/sendmail/status_1.txt') # Ist die Datei status_1.txt noch nicht vorhanden, so wird diese vor dem öffnen erstellt.
else:
    os.system('mkdir /home/sendmail')
    os.system('touch /home/sendmail/status_1.txt')

show_list_1 = []
with  open('/home/sendmail/status_1.txt', 'r') as show_file_1:
    if os.stat('/home/sendmail/status_1.txt').st_size != 0:
        for show_line in show_file_1:
            show_list_1 += [show_line.strip()]

show_list_2 = []

os.system('chia wallet show > /home/sendmail/status_2.txt') # Die Ausgabe der Chia Abfrage wird in die Datei status_2.txt geleitet

with open('/home/sendmail/status_2.txt', 'r') as show_file_2:
    for show_line in show_file_2:
        show_list_2 += [show_line.strip()]

if len(show_list_2) > 0:
    del show_list_2[0]
if len(show_list_1) > 0:
    del show_list_1[0]

switch = True

show_file_1 = open('/home/sendmail/status_1.txt', 'r')
show_file_2 = open('/home/sendmail/status_2.txt', 'r')

if len(show_list_1) > 0:
    a = 0
    for i in show_list_2:
        if i != show_list_1[a]:
            status2 = show_file_2.read() # In der Variable status2 wird der Inhalt der Datei status_2.txt gespeichert
            port = 587 # Portnummer für den SMTP
            smtp_server = "smtp.gmail.com" # Googles smtp Server
            sender_email = "DEINE-SENDER-EMAIL" # Sender Adresse
            receiver_email = "DEINE-EMPFÄNGER-EMAIL" # Empfänger Adresse
            pw = open('/root/google_pw/pw.txt','r') # Öffnet die Datei, die das Passwort zum Google Account enthält. Diese ist im root Verzeichnis hinterlegt
            password = pw.read()  # Speichert den Inhalt der Passwort Datei
            SUBJECT = "Chia-Status" # Betreff
            TEXT = status2 # Inhalt von Status2
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT) # Hier wird in der Variable message die Reihenfolge und das Format der Mail gespeichert.
            context = ssl.create_default_context() # Verschlüsselung
            with smtplib.SMTP(smtp_server, port) as server: # Hier wird der SMTP Server erstellt und nutzt die Angegebene Portnummer
                                                            # anschließend startet die Verschlüsselung, es wird sich in den Google Account eingeloggt
                                                            # dann wird eine Mail erstellt und an den Empfänger gesendet.
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            show_file_1.close() # Die Datei status_1.txt wird wieder geschlossen
            show_file_2.close() # Die Datei status_2.txt wird wieder geschlossen
            os.system('mv /home/sendmail/status_2.txt /home/sendmail/status_1.txt') # Die Datei status_2.txt wird Unbenannt und ersetzt dadurch status_1.txt
            switch = False
            break
        else:
            a += 1
else:
    status2 = show_file_2.read() # In der Variable status2 wird der Inhalt der Datei status_2.txt gespeichert
    port = 587 # Portnummer für den SMTP
    smtp_server = "smtp.gmail.com" # Googles smtp Server
    sender_email = "DEINE-SENDER-EMAIL" # Sender Adresse
    receiver_email = "DEINE-EMPFÄNGER-EMAIL" # Empfänger Adresse
    pw = open('/root/google_pw/pw.txt','r') # Öffnet die Datei, die das Passwort zum Google Account enthält. Diese ist im root Verzeichnis hinterlegt
    password = pw.read()  # Speichert den Inhalt der Passwort Datei
    SUBJECT = "Chia-Status" # Betreff
    TEXT = status2 # Inhalt von Status2
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT) # Hier wird in der Variable message die Reihenfolge und das Format der Mail gespeichert.
    context = ssl.create_default_context() # Verschlüsselung
    with smtplib.SMTP(smtp_server, port) as server: # Hier wird der SMTP Server erstellt und nutzt die Angegebene Portnummer
                                                    # anschließend startet die Verschlüsselung, es wird sich in den Google Account eingeloggt
                                                    # dann wird eine Mail erstellt und an den Empfänger gesendet.
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    show_file_1.close() # Die Datei status_1.txt wird wieder geschlossen
    show_file_2.close() # Die Datei status_2.txt wird wieder geschlossen
    os.system('mv /home/sendmail/status_2.txt /home/sendmail/status_1.txt') # Die Datei status_2.txt wird Unbenannt und ersetzt dadurch status_1.txt
    switch = False

if switch == True:
    show_file_1.close()
    show_file_2.close()
    os.system('rm /home/sendmail/status_2.txt') # Die Datei status_2.txt wird gelöscht