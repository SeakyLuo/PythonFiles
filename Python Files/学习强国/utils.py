import traceback
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from PIL import ImageChops, Image

#############################################################
######    Find Elements
#############################################################

def find_elements(driver, id_):
    '''
    Only supports id, xpath, class_name and android_uiautomator
    @params:
        driver: a webdriver object
        id_: can be any of the id, xpath, class_name and android_uiautomator
    @returns:
        a list of found elements
    '''
    # __handle_system_dialogs(driver)
    if ':id/' in id_:
        return driver.find_elements_by_id(id_)
    elif id_.startswith('android.widget'):
        return driver.find_elements_by_class_name(id_)
    elif id_.startswith('new '):
        return driver.find_elements_by_android_uiautomator(id_)
    else: # elif id_.startswith('//android.widget') or id_.startswith('//*[contains'):
        return driver.find_elements_by_xpath(id_)

def find_element(driver, id_: str, index: int = 0):
    '''
    This function calls find_elements and returns the indexed element from it.
    @params:
        driver: a webdriver object
        id_ (str): can be any of the id, xpath, class_name and android_uiautomator
        index (int): the index of element found, default is 0
    @returns:
        the indexed element if found, otherwise False
    '''
    elements = find_elements(driver, id_)
    return elements[index] if elements else False

def find_and_do(driver, id_: str, operation, index: int = 0):
    '''
    Find the indexed element and do an operation on it.
    @returns:
        True if element is found otherwise False
    '''
    try:
        elements = find_elements(driver, id_)
        if elements:
            operation(elements[index])
            return True
        return False
    except:
        return False

def click(driver, id_: str, index: int = 0):
    '''Find the indexed element and click it.'''
    return find_and_do(driver, id_, lambda x: x.click(), index)

def set_text(driver, id_: str, text: str, index: int = 0):
    '''Find the indexed element and set its text.'''
    return find_and_do(driver, id_, lambda x: x.set_text(text), index)

def get_text(driver, id_: str, index: int = 0):
    '''
    Find the indexed element and return its text. If not found, return ''.
    '''
    element = find_element(driver, id_, index)
    return element.text if element else ''

def get_attribute(driver, id_: str, attribute: str, index: int = 0):
    '''Find the indexed element and get its attribute.'''
    element = find_element(driver, id_, index)
    return element.get_attribute(attribute) if element else None

def is_selected(driver, id_: str, index: int = 0):
    '''Find if the indexed element has the attribute 'selected' equal to true.'''
    return get_attribute(driver, id_, 'selected', index) == 'true'

def is_checked(driver, id_: str, index: int = 0):
    '''Find if the indexed element has the attribute 'checked' equal to true.'''
    return get_attribute(driver, id_, 'checked', index) == 'true'

#############################################################
######    SWIPE
#############################################################

def __swipe(driver, fromX, fromY, toX, toY, duration) -> bool:
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    try:
        driver.swipe(width * fromX, height * fromY, width * toX, height * toY, 500)
        return True
    except (NoSuchElementException, TimeoutException, WebDriverException):
        print(traceback.format_exc())
        return False

def swipe(driver, start_x_ratio, start_y_ratio, end_x_ratio, end_y_ratio, duration=500):
    '''
    Swipe from (start_x_ratio * window_width, start_y_ratio * window * height) to (end_x_ratio * window_width, end_y_ratio * height)
    @params:
        driver: a webdriver object
        start_x_ratio, start_y_ratio, end_x_ratio, end_y_ratio: Swipe from (start_x_ratio * window_width, start_y_ratio * window * height)
                                                                      to   (end_x_ratio * window_width, end_y_ratio * height)
        duration: swipe time in milliseconds
    @returns:
        returns True if swipeable otherwise False
    @raises:
        AssertionException if start_x_ratio, start_y_ratio, end_x_ratio, end_y_ratio don't fall in range [0, 1]
    '''
    assert 0 <= start_x_ratio <= 1 and 0 <= start_y_ratio <= 1 and 0 <= end_x_ratio <= 1 and 0 <= end_y_ratio <= 1, "Ratio doesn't fall in range [0, 1]"
    return __swipe(driver, start_x_ratio, start_y_ratio, end_x_ratio, end_y_ratio, duration)

def swipe_left(driver, x_ratio=7/8, y_ratio=1/2) -> bool:
    '''
    @params:
        driver: a webdriver object
        x_ratio, y_ratio: swipe from (x_ratio * window_width, y_ratio * window_height)
                                to   ((1 - x_ratio) * window_width, y_ratio * window_height)
    @returns:
        returns True if swipeable otherwise False
    @raises:
        AssertionException if x_ratio doesn't fall in range (1/2, 1], y_ratio doesn't fall in range [0, 1]
    '''
    assert 1/2 < x_ratio <= 1, f"x_ratio ({x_ratio}) doesn't fall in range (1/2, 1]"
    assert 0 <= y_ratio <= 1, f"y_ratio ({y_ratio}) doesn't fall in range [0, 1]"
    return swipe(driver, x_ratio, y_ratio, 1 - x_ratio, y_ratio)
    
def swipe_right(driver, x_ratio=1/8, y_ratio=1/2) -> bool:
    '''
    @params:
        driver: a webdriver object
        x_ratio, y_ratio: swipe from (x_ratio * window_width, y_ratio * window_height)
                                to   ((1 - x_ratio) * window_width, y_ratio * window_height)
    @returns:
        returns True if swipeable otherwise False
    @raises:
        AssertionException if x_ratio doesn't fall in range [0, 1/2), y_ratio doesn't fall in range [0, 1]
    '''
    assert 0 <= x_ratio < 1/2, f"x_ratio ({x_ratio}) doesn't fall in range [0, 1/2)"
    assert 0 <= y_ratio <= 1, f"y_ratio ({y_ratio}) doesn't fall in range [0, 1]"
    return swipe(driver, x_ratio, y_ratio, 1 - x_ratio, y_ratio)
    
def swipe_up(driver, x_ratio=1/2, y_ratio=3/5) -> bool:
    '''
    @params:
        driver: a webdriver object
        x_ratio, y_ratio: swipe from (x_ratio * window_width, y_ratio * window_height)
                                to   (x_ratio * window_width, (1 - y_ratio) * window_height).
    @returns:
        returns True if swipeable otherwise False
    @raises:
        AssertionException if x_ratio doesn't fall in range [0, 1], y_ratio doesn't fall in range (1/2, 1]
    '''
    assert 0 <= x_ratio <= 1, f"x_ratio ({x_ratio}) doesn't fall in range [0, 1]"
    assert 1/2 < y_ratio <= 1, f"y_ratio ({y_ratio}) doesn't fall in range (1/2, 1]"
    return swipe(driver, x_ratio, y_ratio, x_ratio, 1 - y_ratio)

def swipe_down(driver, x_ratio=1/2, y_ratio=2/5) -> bool:
    '''
    @params:
        driver: a webdriver object
        x_ratio, y_ratio: swipe from (x_ratio * window_width, y_ratio * window_height)
                                to   (x_ratio * window_width, (1 - y_ratio) * window_height).
    @returns:
        returns True if swipeable otherwise False
    @raises:
        AssertionException if x_ratio doesn't fall in range [0, 1], y_ratio doesn't fall in range [0, 1/2)
    '''
    assert 0 <= x_ratio <= 1, f"x_ratio ({x_ratio}) doesn't fall in range [0, 1]"
    assert 0 <= y_ratio < 1/2, f"y_ratio ({y_ratio}) doesn't fall in range [0, 1/2)"
    return swipe(driver, x_ratio, y_ratio, x_ratio, 1 - y_ratio)

def compare_images(image1: str, image2: str) -> bool:
    '''
    @params:
        image1 (str): The path of image1.
        image2 (str): The path of image2.
    @returns:
        True if two images are identical otherwise False.
    '''
    return ImageChops.difference(Image.open(image1), Image.open(image2)).getbbox() is None