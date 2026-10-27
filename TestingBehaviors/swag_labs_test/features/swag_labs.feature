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

  Scenario: Entering a username leaves the password field alone
    Given I open Swag Labs
    When I enter "standard_user" as my Swag Labs username
    Then the Swag Labs username field should contain "standard_user"
    And the Swag Labs password field should still be empty
    And the Swag Labs login button should be enabled

  Scenario: A customer can enter the Swag Labs shop floor
    Given I open Swag Labs
    When I sign in to browse the Swag Labs catalog
    Then the Swag Labs page title should be "Swag Labs"

  Scenario: A customer can take stock of the shop floor
    Given I open Swag Labs
    When I sign in to browse the Swag Labs catalog
    Then the Swag Labs catalog should be headed "Products"
    And the Swag Labs catalog should list 6 products
    And the Swag Labs catalog should include "Sauce Labs Backpack"

  Scenario: Sorting helps a bargain hunter find the lowest-priced product
    Given I open Swag Labs
    When I sign in to browse the Swag Labs catalog
    And I sort the Swag Labs catalog from cheapest to priciest
    Then the first Swag Labs product should be "Sauce Labs Onesie"
    And the first Swag Labs product should cost "$7.99"

  Scenario: A customer can inspect a product before buying
    Given I open Swag Labs
    When I sign in to browse the Swag Labs catalog
    And I inspect the Swag Labs product "Sauce Labs Backpack"
    Then the Swag Labs product details should show "Sauce Labs Backpack"
    And the Swag Labs product details should cost "$29.99"