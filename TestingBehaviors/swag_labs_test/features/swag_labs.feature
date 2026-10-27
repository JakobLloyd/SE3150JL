Feature: Shopping on Swag Labs
  As a customer with a shopping list
  I want to visit Swag Labs
  So that I can see what the shop has in store

  Scenario: The shop welcomes a customer
    Given I open Swag Labs

  Scenario: The shop identifies itself in the browser
    Given I open Swag Labs
    Then the Swag Labs page title should be "Swag Labs"