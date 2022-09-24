#!/usr/bin/env python

import argparse

from authentication import get_admin_session
from browser import solve_browser_challenges
from feedback import solve_feedback_challenges
from filehandling import solve_file_handling_challenges
from misc import solve_misc_challenges
from products import solve_product_challenges
from users import solve_user_challenges

parser = argparse.ArgumentParser(description='Run JuiceShop solver against a target.')
parser.add_argument('--hostname', nargs='?',
                    const='localhost', default='localhost',
                    help='The FQDN of the target host (default: localhost)')
parser.add_argument('--port', nargs='?', type=int, 
                    const=3000, default=3000,
                    help='The TCP port for JuiceShop (default: 3000)')
parser.add_argument('--protocol', nargs='?',
                    const='http', default='http',
                    help='Indicate [http/https] (default: http)')

args = parser.parse_args()

server = args.protocol+'://'+args.hostname+':'+str(args.port)
#server = 'http://localhost:3000'
#server = 'http://localhost:8080'

session = get_admin_session(server)
solve_file_handling_challenges(server)
solve_user_challenges(server)
solve_feedback_challenges(server)
solve_product_challenges(server)
solve_misc_challenges(server)
# Selenium-based - comment out the below if you don't have the Chromedriver set up.
#solve_browser_challenges(server)
