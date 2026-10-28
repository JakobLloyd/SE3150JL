Feature: Shopping on Swag Labs
  As a customer with a shopping list
  I want to visit Swag Labs
  So that I can see what the shop has in store

  Scenario: A new customer finds the shop and a clean login form
    Given I open Swag Labs
    Then the Swag Labs page title should be "Swag Labs"
    And the Swag Labs login form should be ready
    And the Swag Labs login fields should be empty
    And the Swag Labs login button should be enabled

  Scenario: The sign-in form labels both details a customer needs
    Given I open Swag Labs
    Then the Swag Labs username field should prompt "Username"
    And the Swag Labs password field should prompt "Password"
    And the Swag Labs login fields should be empty
    And the Swag Labs login form should be ready

  Scenario: A customer can check the sign-in controls before starting
    Given I open Swag Labs
    Then the Swag Labs login form should be ready
    And the Swag Labs page title should be "Swag Labs"
    And the Swag Labs login button should be enabled
    And the Swag Labs password field should mask what I type

  Scenario: Refreshing the sign-in page leaves it ready for another attempt
    Given I open Swag Labs
    When I refresh the Swag Labs login page
    Then the Swag Labs login form should be ready
    And the Swag Labs login fields should be empty
    And the Swag Labs login button should be enabled

  Scenario: A first-time customer sees empty fields with clear prompts
    Given I open Swag Labs
    Then the Swag Labs login fields should be empty
    And the Swag Labs username field should prompt "Username"
    And the Swag Labs password field should prompt "Password"
    And the Swag Labs password field should mask what I type

  Scenario: The username hint appears before a customer enters any details
    Given I open Swag Labs
    Then the Swag Labs username field should prompt "Username"
    And the Swag Labs login fields should be empty
    And the Swag Labs login form should be ready
    And the Swag Labs login button should be enabled

  Scenario: The login page is ready without exposing password entry
    Given I open Swag Labs
    Then the Swag Labs page title should be "Swag Labs"
    And the Swag Labs login form should be ready
    And the Swag Labs login fields should be empty
    And the Swag Labs password field should mask what I type

  Scenario: The login fields guide a customer without giving away details
    Given I open Swag Labs
    Then the Swag Labs login form should be ready
    And the Swag Labs login fields should be empty
    And the Swag Labs username field should prompt "Username"
    And the Swag Labs password field should prompt "Password"

  Scenario: The blank login form still lets a customer try
    Given I open Swag Labs
    Then the Swag Labs page title should be "Swag Labs"
    And the Swag Labs login form should be ready
    And the Swag Labs login fields should be empty
    And the Swag Labs login button should be enabled

  Scenario: Entering a username leaves the password field alone
    Given I open Swag Labs
    When I enter "standard_user" as my Swag Labs username
    Then the Swag Labs username field should contain "standard_user"
    And the Swag Labs password field should still be empty
    And the Swag Labs login button should be enabled

  Scenario: Submitting a blank sign-in asks for a username
    Given I open Swag Labs
    When I submit the Swag Labs login form
    Then the Swag Labs login message should say "Epic sadface: Username is required"
    And the Swag Labs login page should remain open
    And the Swag Labs login fields should be empty

  Scenario: A username without a password receives a specific prompt
    Given I open Swag Labs
    When I enter "standard_user" as my Swag Labs username
    And I submit the Swag Labs login form
    Then the Swag Labs login message should say "Epic sadface: Password is required"
    And the Swag Labs username field should contain "standard_user"
    And the Swag Labs password field should be empty

  Scenario: A password without a username asks for the missing username
    Given I open Swag Labs
    When I enter "not_the_demo_password_2026" as my Swag Labs password
    And I submit the Swag Labs login form
    Then the Swag Labs login message should say "Epic sadface: Username is required"
    And the Swag Labs username field should be empty
    And the Swag Labs password field should contain "not_the_demo_password_2026"

  Scenario: Unknown customer details are rejected with a clear message
    Given I open Swag Labs
    When I enter "unknown_customer_2026" as my Swag Labs username
    And I enter "not_the_demo_password_2026" as my Swag Labs password
    And I submit the Swag Labs login form
    Then the Swag Labs login message should say "Epic sadface: Username and password do not match any user in this service"
    And the Swag Labs login page should remain open

  Scenario: A customer can dismiss a required-field message
    Given I open Swag Labs
    When I submit the Swag Labs login form
    And I dismiss the Swag Labs login message
    Then the Swag Labs login message should be dismissed
    And the Swag Labs login form should be ready

  Scenario: Pressing Enter submits the sign-in form
    Given I open Swag Labs
    When I enter "unknown_customer_2026" as my Swag Labs username
    And I enter "not_the_demo_password_2026" as my Swag Labs password
    And I submit the Swag Labs login form by pressing Enter
    Then the Swag Labs login message should say "Epic sadface: Username and password do not match any user in this service"
    And the Swag Labs login page should remain open

  Scenario: A customer can correct a username after a rejected attempt
    Given I open Swag Labs
    When I enter "unknown_customer_2026" as my Swag Labs username
    And I enter "not_the_demo_password_2026" as my Swag Labs password
    And I submit the Swag Labs login form
    And I dismiss the Swag Labs login message
    And I clear the Swag Labs username field
    And I enter "standard_user" as my Swag Labs username
    And I submit the Swag Labs login form
    Then the Swag Labs login message should say "Epic sadface: Username and password do not match any user in this service"
    And the Swag Labs login page should remain open
