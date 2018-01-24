import sys
import webbrowser

from auth import auth_method
from tools import get_publickey_from_seed, get_uid_from_pubkey, message_exit, get_current_block
from network_tools import request
from constants import NO_MATCHING_ID
from wot import is_member, get_pubkey_from_id
from tabulate import tabulate

def send_certification(ep, c):
    certified_uid = c.subsubcmd
    certified_pubkey = get_pubkey_from_id(ep, certified_uid)

    # Check that the id exists on the network
    if (certified_pubkey is NO_MATCHING_ID):
        message_exit(NO_MATCHING_ID)

    # Display license in webbrowser and ask for confirmation
#    license_approval()

    # Authentication
    seed = auth_method(c)

    # Check if certification have already been sent (in the sandbox), written into the blockchain

    # Check current user is a member
    issuer_pubkey = get_publickey_from_seed(seed)
    issuer_id = get_uid_from_pubkey(ep, issuer_pubkey)
#    if not is_member(ep, issuer_pubkey, issuer_id):
#        message_exit("You can't certify an identity with this pubkey")

    # Certification confirmation
    if certification_confirmation(issuer_id, issuer_pubkey, certified_uid, certified_pubkey):
        cert_doc = generate_certification_document(ep, issuer_id, issuer_pubkey)
        message_exit("EXIT")

        # Send certification document
        transaction += sign_document_from_seed(cert_doc, seed) + "\n"

        retour = post_request(ep, "wot/certify", "transaction=" + urllib.parse.quote_plus(transaction))
        print("Certification successfully sent.")

def license_approval():
    if (input("In which language do you want to display Ğ1 license [en/fr]? ") is "en"):
        webbrowser.open("https://duniter.org/en/get-g1/")
    else:
        webbrowser.open("https://duniter.org/fr/wiki/licence-g1/")
    if (input("Do you approve Ğ1 license [y/n]? ") is not "y"):
        sys.exit(1)

def certification_confirmation(issuer_id, issuer_pubkey, certified_uid, certified_pubkey):
    cert = list()
    cert.append(["Cert", "From", "–>", "To"])
    cert.append(["ID", issuer_id, "–>", certified_uid])
    cert.append(["Pubkey", issuer_pubkey, "–>", certified_pubkey])
    if input(tabulate(cert, tablefmt="fancy_grid") + \
       "\nDo you confirm sending this certification? [yes/no]: ") == "yes":
        return(True)


def generate_certification_document(ep, issuer_id, issuer_pubkey):
    # Generate certification document
    #https://git.duniter.org/nodes/typescript/duniter/blob/1.6/doc/Protocol.md#certification
    cert_doc = "Version: 10\n\
Type: Certification\n\
Currency: " + get_current_block(ep)["currency"] + "\n\
Issuer: " + issuer_pubkey + "\n\
IdtyIssuer: " + issuer_id + "\n\
IdtyUniqueID: USER_ID\n\
IdtyTimestamp: BLOCK_UID\n\
IdtySignature: IDTY_SIGNATURE\n\
CertTimestamp: BLOCK_UID"
    print(cert_doc)
    #CERTIFIER_SIGNATURE
