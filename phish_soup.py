import os
from emailgenerator import EmailGenerator
from landingpagegenerator import LandingPageGenerator
from dotenv import load_dotenv
import getpass
import datetime

load_dotenv()

TEMPLATE_DIR = 'templates'
LANDING_DIR = 'landings'
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(LANDING_DIR, exist_ok=True)

LOG_FILE = "phish_soup.log"

def log_action(action):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.datetime.now().isoformat()} - {action}\n")

class PhishSoulCLI:
    LANDING_NAME_PROMPT = "Landing name: "
    SUBJECT_PROMPT = "Subject: "
    BODY_PROMPT = "Body: "

    def __init__(self):
        self.emailgen = EmailGenerator()
        self.landinggen = LandingPageGenerator()

    def print_ascii_logo(self):
        print(r"""

 ██▓███   ██░ ██  ██▓  ██████  ██░ ██      ██████  ▒█████   █    ██  ██▓███  
▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒   ▒██    ▒ ▒██▒  ██▒ ██  ▓██▒▓██░  ██▒
▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░   ░ ▓██▄   ▒██░  ██▒▓██  ▒██░▓██░ ██▓▒
▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██      ▒   ██▒▒██   ██░▓▓█  ░██░▒██▄█▓▒ ▒
▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓   ▒██████▒▒░ ████▓▒░▒▒█████▓ ▒██▒ ░  ░
▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒   ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░
░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░   ░ ░▒  ░ ░  ░ ▒ ▒░ ░░▒░ ░ ░ ░▒ ░     
░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░   ░  ░  ░  ░ ░ ░ ▒   ░░░ ░ ░ ░░       
          ░  ░  ░ ░        ░   ░  ░  ░         ░      ░ ░     ░              

 """)

    def main_menu(self):
        while True:
            self.print_ascii_logo()
            print("Welcome to PHISH_SOUP!")
            print("1. Manage email templates")
            print("2. Manage landing pages")
            print("3. Send email")
            print("4. Exit")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.manage_email_templates()
            elif choice == '2':
                self.manage_landing_pages()
            elif choice == '3':
                self.send_email_cli()
            elif choice == '4':
                print("Bye!")
                break
            else:
                print("Invalid option.\n")

    def manage_email_templates(self):
        print("\n--- Manage Email Templates ---")
        print("1. Create new template")
        print("2. List templates")
        print("3. Delete template")
        print("4. Edit template")
        print("5. Preview template")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            name = input("Template name: ").strip()
            subject = input(self.SUBJECT_PROMPT).strip()
            body = input(self.BODY_PROMPT).strip()
            self.emailgen.generate_email_template(name, subject, body)
            print("Template created.\n")
            log_action(f"Created template '{name}'")
        elif choice == '2':
            templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
            if not templates:
                print("No templates found.\n")
            else:
                print("Available templates:")
                for t in templates:
                    print(f"- {t}")
                print()
        elif choice == '3':
            templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
            if not templates:
                print("No templates to delete.\n")
                return
            print("Available templates:")
            for idx, t in enumerate(templates):
                print(f"{idx+1}. {t}")
            sel = input("Choose the template number to delete: ").strip()
            try:
                sel_idx = int(sel) - 1
                confirm = input(f"Are you sure you want to delete '{templates[sel_idx]}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    os.remove(os.path.join(TEMPLATE_DIR, templates[sel_idx]))
                    print("Template deleted.\n")
                    log_action(f"Deleted template '{templates[sel_idx]}'")
                else:
                    print("Deletion cancelled.\n")
            except Exception as e:
                print(f"Error deleting template: {e}\n")
        elif choice == '4':
            templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
            if not templates:
                print("No templates to edit.\n")
                return
            print("Available templates:")
            for idx, t in enumerate(templates):
                print(f"{idx+1}. {t}")
            sel = input("Choose the template number to edit: ").strip()
            try:
                sel_idx = int(sel) - 1
                template_path = os.path.join(TEMPLATE_DIR, templates[sel_idx])
                with open(template_path, 'r') as f:
                    lines = f.readlines()
                old_subject = lines[0].strip() if lines else ""
                old_body = "".join(lines[1:]).strip() if len(lines) > 1 else ""
                print(f"Current subject: {old_subject}")
                subject = input("New subject (leave blank to keep current): ").strip() or old_subject
                print(f"Current body:\n{old_body}")
                body = input("New body (leave blank to keep current): ").strip() or old_body
                with open(template_path, 'w') as f:
                    f.write(subject + "\n" + body)
                print("Template updated.\n")
                log_action(f"Edited template '{templates[sel_idx]}'")
            except Exception as e:
                print(f"Error editing template: {e}\n")
        elif choice == '5':
            templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
            if not templates:
                print("No templates to preview.\n")
                return
            print("Available templates:")
            for idx, t in enumerate(templates):
                print(f"{idx+1}. {t}")
            sel = input("Choose the template number to preview: ").strip()
            try:
                sel_idx = int(sel) - 1
                template_path = os.path.join(TEMPLATE_DIR, templates[sel_idx])
                with open(template_path, 'r') as f:
                    lines = f.readlines()
                subject = lines[0].strip() if lines else ""
                body = "".join(lines[1:]).strip() if len(lines) > 1 else ""
                print(f"\n--- Template Preview: {templates[sel_idx]} ---")
                print(f"Subject: {subject}")
                print("Body:")
                print(body)
                print("--- End Preview ---\n")
            except Exception as e:
                print(f"Error previewing template: {e}\n")
        else:
            print("Invalid option.\n")

    def manage_landing_pages(self):
        print("\n--- Manage Landing Pages ---")
        print("1. Create custom landing page")
        print("2. Create Instagram clone landing page")
        print("3. Create Facebook clone landing page")
        print("4. Open a landing page in browser")
        print("5. Delete a landing page")
        print("6. Edit a landing page")
        print("7. Preview a landing page")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            name = input(self.LANDING_NAME_PROMPT).strip()
            title = input("Title: ").strip()
            message = input("Message: ").strip()
            self.landinggen.generate_landing(name, title, message)
            print("Landing page created.\n")
            log_action(f"Created landing page '{name}'")
        elif choice == '2':
            name = input(self.LANDING_NAME_PROMPT).strip()
            self.landinggen.generate_instagram_clone(name)
            print("Instagram clone landing page created.\n")
            log_action(f"Created Instagram clone landing '{name}'")
        elif choice == '3':
            name = input(self.LANDING_NAME_PROMPT).strip()
            self.landinggen.generate_facebook_clone(name)
            print("Facebook clone landing page created.\n")
            log_action(f"Created Facebook clone landing '{name}'")
        elif choice == '4':
            self.open_landing_in_browser()
        elif choice == '5':
            landings = [f for f in os.listdir(LANDING_DIR) if f.endswith('.html')]
            if not landings:
                print("No landing pages to delete.\n")
                return
            print("Available landing pages:")
            for idx, l in enumerate(landings):
                print(f"{idx+1}. {l}")
            sel = input("Choose the landing page number to delete: ").strip()
            try:
                sel_idx = int(sel) - 1
                confirm = input(f"Are you sure you want to delete '{landings[sel_idx]}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    os.remove(os.path.join(LANDING_DIR, landings[sel_idx]))
                    print("Landing page deleted.\n")
                    log_action(f"Deleted landing page '{landings[sel_idx]}'")
                else:
                    print("Deletion cancelled.\n")
            except Exception as e:
                print(f"Error deleting landing page: {e}\n")
        elif choice == '6':
            landings = [f for f in os.listdir(LANDING_DIR) if f.endswith('.html')]
            if not landings:
                print("No landing pages to edit.\n")
                return
            print("Available landing pages:")
            for idx, l in enumerate(landings):
                print(f"{idx+1}. {l}")
            sel = input("Choose the landing page number to edit: ").strip()
            try:
                sel_idx = int(sel) - 1
                landing_path = os.path.join(LANDING_DIR, landings[sel_idx])
                with open(landing_path, 'r') as f:
                    html = f.read()
                import re
                title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
                body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
                old_title = title_match.group(1).strip() if title_match else ""
                old_message = body_match.group(1).strip() if body_match else ""
                print(f"Current title: {old_title}")
                title = input("New title (leave blank to keep current): ").strip() or old_title
                print(f"Current message:\n{old_message}")
                message = input("New message (leave blank to keep current): ").strip() or old_message
                html = re.sub(r'(<title>)(.*?)(</title>)', rf'\1{title}\3', html, flags=re.DOTALL)
                html = re.sub(r'(<body[^>]*>)(.*?)(</body>)', rf'\1{message}\3', html, flags=re.DOTALL)
                with open(landing_path, 'w') as f:
                    f.write(html)
                print("Landing page updated.\n")
                log_action(f"Edited landing page '{landings[sel_idx]}'")
            except Exception as e:
                print(f"Error editing landing page: {e}\n")
        elif choice == '7':
            landings = [f for f in os.listdir(LANDING_DIR) if f.endswith('.html')]
            if not landings:
                print("No landing pages to preview.\n")
                return
            print("Available landing pages:")
            for idx, l in enumerate(landings):
                print(f"{idx+1}. {l}")
            sel = input("Choose the landing page number to preview: ").strip()
            try:
                sel_idx = int(sel) - 1
                landing_path = os.path.join(LANDING_DIR, landings[sel_idx])
                with open(landing_path, 'r') as f:
                    html = f.read()
                print(f"\n--- Landing Page Preview: {landings[sel_idx]} ---")
                print(html[:500] + ("..." if len(html) > 500 else ""))  # Show first 500 chars
                print("--- End Preview ---\n")
            except Exception as e:
                print(f"Error previewing landing page: {e}\n")
        else:
            print("Invalid option.\n")

    def open_landing_in_browser(self):
        landings = [f for f in os.listdir(LANDING_DIR) if f.endswith('.html')]
        if not landings:
            print("No landing pages found.\n")
            return
        print("Available landing pages:")
        for idx, l in enumerate(landings):
            print(f"{idx+1}. {l}")
        sel = input("Choose the landing page number to open: ").strip()
        try:
            sel_idx = int(sel) - 1
            landing_path = os.path.abspath(os.path.join(LANDING_DIR, landings[sel_idx]))
            os.system(f'"$BROWSER" "file://{landing_path}"')
            print("Landing page opened in browser.\n")
        except Exception as e:
            print(f"Error opening landing page: {e}\n")

    def send_email_cli(self):
        print("\n--- Send Email ---")
        use_template = input("Do you want to use a pre-made template? (y/n): ").strip().lower() == 'y'
        if use_template:
            templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.txt')]
            if not templates:
                print("No templates found.\n")
                return
            print("Available templates:")
            for idx, t in enumerate(templates):
                print(f"{idx+1}. {t}")
            sel = input("Choose the template number: ").strip()
            try:
                sel_idx = int(sel) - 1
                template_path = os.path.join(TEMPLATE_DIR, templates[sel_idx])
                with open(template_path, 'r') as f:
                    lines = f.readlines()
                    subject = lines[0].strip() if lines else ""
                    body = "".join(lines[1:]).strip() if len(lines) > 1 else ""
            except Exception as e:
                print(f"Error selecting template: {e}\n")
                return
        else:
            subject = input(self.SUBJECT_PROMPT).strip() or os.getenv("SMTP_SUBJECT", "")
            body = input(self.BODY_PROMPT).strip() or os.getenv("SMTP_BODY", "")

        smtp_host = input("SMTP host (e.g. smtp.gmail.com): ").strip() or os.getenv("SMTP_HOST", "")
        smtp_port_input = input("SMTP port (e.g. 587): ").strip()
        smtp_port = int(smtp_port_input) if smtp_port_input else int(os.getenv("SMTP_PORT", "587"))
        sender = input("Sender: ").strip() or os.getenv("SMTP_SENDER", "")
        recipient = input("Recipient: ").strip() or os.getenv("SMTP_RECIPIENT", "")
        use_auth_input = input("Use SMTP authentication? (y/n): ").strip()
        use_auth = (use_auth_input or os.getenv("SMTP_USE_AUTH", "n")).lower() == 'y'
        if use_auth:
            os.environ['SMTP_USER'] = input("SMTP username: ").strip() or os.getenv("SMTP_USER", "")
            os.environ['SMTP_PASS'] = getpass.getpass("SMTP password: ") or os.getenv("SMTP_PASS", "")
        use_ssl_input = input("Use SSL? (y/n): ").strip()
        use_ssl = (use_ssl_input or os.getenv("SMTP_SSL", "n")).lower() == 'y'
        use_tls_input = input("Use TLS? (y/n): ").strip()
        use_tls = (use_tls_input or os.getenv("SMTP_TLS", "n")).lower() == 'y'
        os.environ['SMTP_SSL'] = 'true' if use_ssl else 'false'
        os.environ['SMTP_TLS'] = 'true' if use_tls else 'false'
        try:
            self.emailgen.send_email(smtp_host, smtp_port, sender, recipient, subject, body)
            print("Email sent.\n")
        except Exception as e:
            print(f"Error sending email: {e}\n")

if __name__ == "__main__":
    PhishSoulCLI().main_menu()
