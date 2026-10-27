Feature: Shopping on Swag Labs
  As a customer with a shopping list
  I want to visit Swag Labs
  So that I can see what the shop has in store

  Scenario: The shop welcomes a customer
    Given I open Swag Labs

  Scenario: The shop identifies itself in the browser
    Given I open Swag Labs
    Then the Swag Labs page title should be "Swag Labs"

  Scenario: The login counter is ready for its next customer
    Given I open Swag Labs
    Then the Swag Labs login form should be ready

  Scenario: The login counter survives a page refresh
    Given I open Swag Labs
    When I refresh the Swag Labs login page
    Then the Swag Labs login form should be ready

  Scenario: A new customer's login details are not filled in
    Given I open Swag Labs
    Then the Swag Labs login fields should be empty

  Scenario: The username field gives a useful hint
    Given I open Swag Labs
    Then the Swag Labs username field should prompt "Username"

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