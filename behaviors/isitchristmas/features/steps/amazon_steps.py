@step(u'I visit the Amazon home page')
def step_impl(context):
    context.behave_driver.open_url("https://amazon.com")

@when(u'I search for "{query}"')
def step_impl(context, query):
    #input_field = context.behave_driver.get_element('#twotabsearchtextbox')
    #input_field.clear()
    #input_field.send_keys(query)
    #context.behave_driver.click_element('#nav-search-submit-button')

    context.execute_steps(u'''
        When I set "{query}" to the inputfield "#twotabsearchtextbox"
        And I click on the button "#nav-search-submit-button"
    '''.format(query=query))

@then(u'I should see "Panda Teddy Bear Stuffed Animal Plush" in my search results')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "Panda Teddy Bear Stuffed Animal Plush" in my search results')

@when(u'I click the result "{result_text}"')
def step_impl(context, result_text):
    context.behave_driver.click_link_text(result_text, partial=True)

@when(u'I add the current item to my cart')
def step_impl(context):
    context.behave_driver.click_element('#addToCart_feature_div')
    context.behave_driver.pause(3000)

@when(u'I view my shopping cart')
def step_impl(context):
    context.behave_driver.click_element('#attach-sidesheet-view-cart-button')

@then(u'I should see "{text}" in my cart')
def step_impl(context, text):
    contains = context.behave_driver.element_contains("#activeCartViewForm", text)
    assert contains

