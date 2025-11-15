import os
from datetime import datetime
from imapclient import IMAPClient
from email import policy
import email

# ===========
# Konfigurace
# ===========

EMAIL = input("Zadejte emailovou adresu: ")
PASSWORD = input("Zadejte heslo: ")
IMAP_SERVER = "imap.seznam.cz"
SUBJECT_KEYWORD = input("Zadejte klíčové slovo v předmětu emailu: ")
OUTPUT_FOLDER = "E:/práce/firmy/cafe slavia/analysis/data_raw/output_data"


# ===========
# Připojení k emailovému serveru
# ===========

print("Připojování k emailovému serveru...")
with IMAPClient(IMAP_SERVER) as server:
    server.login(EMAIL, PASSWORD)
    server.select_folder("HLÁVKY|TRŽBY VILA SLAVIA")

    # folders = server.list_folders()
    # for folder in folders:
    #   print(f"Folder: {folder}")

    # Hledání emailů s daným klíčovým slovem v předmětu
    print(f"Hledání emailů s předmětem obsahujícím '{SUBJECT_KEYWORD}'...")

    messages = server.search(["TEXT", SUBJECT_KEYWORD.lower()])
    for msgid in messages:
        raw_message = server.fetch(msgid, ["RFC822"])[msgid][b"RFC822"]
        subject = (
            email.message_from_bytes(raw_message, policy=policy.default)["subject"]
            .strip(" ")
            .lower()
        )
        print(f" - Nalezen email s předmětem: {subject}")
    print(f"Nalezeno {len(messages)} emailů.")

    server.logout()


"""
    for msgid, data in server.fetch(messages, ['RFC822']).items():
        email_message = policy.default.parsebytes(data[b'RFC822'])

        # Uložení příloh
        for part in email_message.iter_attachments():
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                print(f"Příloha '{filename}' uložena do '{OUTPUT_FOLDER}'.")
"""
