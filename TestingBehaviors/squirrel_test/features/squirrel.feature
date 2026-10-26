Feature: Squirreltown
    As a certified squirrel enjoyer
    I want to poke at buttons in Squirreltown
    So that no nut goes unchecked

Scenario: The town knows its own name
    Then the page title is "Squirreltown"
    And the heading says "Welcome to Squirreltown"

Scenario: Add button opens the dialog
    Given I am on the Squirreltown page
    When I click the add button
    Then the squirrel dialog should be visible
    And the dialog title should be "Add Squirrel"