#Task 05



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup Chrome Options to Disable Password Manager ---
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Define an explicit wait for robust element location
wait = WebDriverWait(driver, 20)

# Define website URL and user credentials
BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

def run_checkout_test():
    try:
        print("Step 1: Navigating to the website and logging in...")
        driver.get(BASE_URL)
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        wait.until(EC.url_contains("inventory.html"))
        print("✅ Verification PASSED: Successfully logged in and redirected to inventory page.")

        print("\nStep 2: Adding an item to the cart...")
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        shopping_cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert shopping_cart_badge.text == "1"
        print("✅ Verification PASSED: Item count in cart is 1.")

        shopping_cart_badge.click()
        wait.until(EC.url_contains("cart.html"))
        item_in_cart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name")))
        assert "Sauce Labs Backpack" in item_in_cart.text
        print("✅ Verification PASSED: Successfully navigated to the cart page with the correct item.")

        print("\nStep 3: Proceeding to checkout...")
        driver.find_element(By.ID, "checkout").click()

        wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
        assert "checkout-step-one.html" in driver.current_url
        print("✅ Verification PASSED: Navigated to the checkout information page.")

        print("\nStep 4: Filling form and verifying checkout overview...")
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        assert "checkout-step-two.html" in driver.current_url
        print("✅ Verification PASSED: Checkout overview page loaded successfully.")

        print("\nStep 5: Finalizing the purchase...")
        finish_button = driver.find_element(By.ID, "finish")
        driver.execute_script("arguments[0].click();", finish_button)

        success_header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))

        assert "checkout-complete.html" in driver.current_url
        assert "THANK YOU FOR YOUR ORDER" in success_header.text.upper()
        print("✅ Verification PASSED: Order confirmation and success message verified.")
        print("\n🎉 AUTOMATION TEST COMPLETED SUCCESSFULLY! 🎉")

    except Exception as e:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"failure_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n❌ TEST FAILED: An error occurred.")
        print(f"📄 Screenshot saved as {screenshot_name}")
        print(f"Error details: {e}")

    finally:
        print("\nClosing the browser.")
        driver.quit()

# --- Run the test ---
if __name__ == "__main__":
    run_checkout_test()

