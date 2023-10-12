
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import selenium.webdriver.support.ui as UI
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import tkinter.messagebox
 
def program():

    def before():
        if tkinter.messagebox.askyesno("AutoSBID", "Welcome to AutoSBID! Would you like to continue?"):
            main()

    def main():
        try:
            driver = webdriver.Chrome()
            data = readJSON()
            enterSBID(driver)
            acceptCookies(driver)
            login(driver, data)
            if confirmLogin(driver):
                while checkPending(driver, data):
                    checkPending(driver, data)
        except Exception as e:
            if tkinter.messagebox.askretrycancel("AutoSBID", "Unknown error! You should also check that the \"data.json\" file is correct, however, this error may also have been caused by a rare error when interacting with the sBid application, do you want to try again?"):
                end(driver)
                program()

        finally:
            end(driver)

    def readJSON():
        x = open('data.json')
        data = json.load(x)
        x.close()
        return data

    def enterSBID(driver):
        driver.implicitly_wait(1)
        driver.get('https://www.empresaiformacio.org/sBid/')

    def acceptCookies(driver):
        driver.switch_to.frame(driver.find_element(By.ID, "jspContainer"))
        driver.find_element(By.CLASS_NAME, 'acceptar').click()

    def login(driver, data):
        driver.find_element(By.ID, 'username').send_keys(data['user'])
        driver.find_element(By.ID, 'password').send_keys(data['password'])
        driver.find_element(By.CSS_SELECTOR, '#pageBody > div.row.mainMenu > div.col-sm-4.col-xs-12.mainMenu > form > div.form-group.text-right > div > button').click()

    def confirmLogin(driver):
        if driver.find_elements(By.XPATH, '//*[@id="messageBox"]/span'):
            if driver.find_element(By.XPATH, '//*[@id="messageBox"]/span').text == 'Ha intentat iniciar sessió molts cops sense èxit. Durant els pròxims minuts, rebrà un missatge per regenerar la contrasenya a l\'email de l\'usuari indicat.':
                tkinter.messagebox.showerror("AutoSBID", 'Login Error! Password reset required.')
                return False
            if driver.find_element(By.XPATH, '//*[@id="messageBox"]/span').text == 'Usuari o contrasenya incorrectes. Si us plau, intenteu-ho de nou o recupereu la contrasenya.':
                tkinter.messagebox.showerror("AutoSBID", 'Login Error! Check that the user and password in \'data.json\' is correct!')
                return False
            else:
                tkinter.messagebox.showerror("AutoSBID", 'Unknown login Error!')
                return False
        else:
            return True
        

    def checkPending(driver, data):
        driver.switch_to.frame(driver.find_element(By.ID, 'contentmain'))
        if driver.find_element(By.XPATH, "//*[@id=\"workingForm\"]/div[1]/div[1]/div[2]/div[1]/div[1]/h4/a/span").text != '0':
            if "Informe periòdic Dossier" in driver.find_element(By.XPATH, "//*[@id=\"collapse1\"]/ul/li[1]/a/strong").text:
                fillInforme(driver)
                return True
            elif "Activitat diària del dossier " in driver.find_element(By.XPATH, "//*[@id=\"collapse1\"]/ul/li[1]/a/strong").text:
                fillActivitat(driver, data)
                return True
            else:
                # Other types of forms not implemented yet (if they exist)
                tkinter.messagebox.showwarning("AutoSBID", 'Not automated form detected! Manual filling required!')
                return False
        else:
            tkinter.messagebox.showinfo("AutoSBID", 'All OK. No more forms pending at the moment!')
            return False

    def fillInforme(driver):
        driver.find_element(By.XPATH, "//*[@id=\"collapse1\"]/ul/li[1]/a").click()
        select = UI.Select(driver.find_element(By.ID, "inp_13352"))
        select.select_by_index(len(select.options)-1)
        select = UI.Select(driver.find_element(By.ID, "inp_13364"))
        select.select_by_index(len(select.options)-1)
        driver.find_element(By.XPATH, '//*[@id=\"workingForm\"]/div/div[2]/div[7]/span').click()
        # THIS PART MAY NOT WORK AND NEEDS FURTHER TESTING
        driver.execute_script("location.reload(true);")

    def fillActivitat(driver, data):
        driver.find_element(By.XPATH, "//*[@id=\"collapse1\"]/ul/li[1]/a").click()
        if data['task'] == 1:
            activitatSelect(driver, "inp_13352")
        elif data['task'] == 2:
            activitatSelect(driver, "inp_13364")
        elif data['task'] == 3:
            activitatSelect(driver, "inp_13373")
        else:
            tkinter.messagebox.showerror("AutoSBID", 'Error! Task specified out of range!')
            return False

    def activitatSelect(driver, selectID):
        select = UI.Select(driver.find_element(By.ID, selectID))
        select.select_by_index(len(select.options)-1)
        driver.find_element(By.XPATH, '//*[@id="workingForm"]/div[1]/div[3]/span[1]').click()
        end(driver)
        main()


    def end(driver):
        driver.quit()

    before()

program()