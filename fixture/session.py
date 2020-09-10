

class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, user, pwd):
        driver = self.app.driver
        self.app.open_home_page()  # method
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys(user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(pwd)
        driver.find_element_by_css_selector('input[type="submit"]').click()

    def logout(self):
        driver = self.app.driver
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_name("user")

    def is_logged_in(self):
        driver = self.app.driver
        return len(driver.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        driver = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        driver = self.app.driver
        return driver.find_element_by_css_selector("td.login-info-left span").text

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def ensure_login(self, user, pwd):
        if self.is_logged_in():
            if self.is_logged_in_as(user):
                return
            else:
                self.logout()
        self.login(user, pwd)
