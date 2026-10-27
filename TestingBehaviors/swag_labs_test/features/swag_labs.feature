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