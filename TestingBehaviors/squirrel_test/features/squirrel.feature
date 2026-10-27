Feature: Squirreltown
    As a certified squirrel enjoyer
    I want to poke at buttons in Squirreltown
    So that no nut goes unchecked

Background:
    Given I open Squirreltown

Scenario: The town knows its own name
    Then the page title is "Squirreltown"
    And the heading says "Welcome to Squirreltown"

Scenario: The secret dialog is hiding
    Then the dialog is hidden

Scenario: Poking the plus button summons the dialog
    When I click the add button
    Then the dialog is visible
    And the dialog title is "Add Squirrel"

Scenario: Chickening out of adding a squirrel
    When I click the add button
    And I click the cancel button
    Then the dialog is hidden

Scenario: Sir Nutsalot joins the town and then gets booted
    When I add a squirrel named "Sir Nutsalot" with size "very large"
    Then the squirrel list contains "Sir Nutsalot"
    When I click the delete button on the last squirrel
    Then the popup says "Are you sure you want to delete Sir Nutsalot?"
    When I accept the popup
    Then the squirrel list does not contain "Sir Nutsalot"

Scenario: Saying no to the delete popup saves the squirrel
    When I add a squirrel named "Plot Armor" with size "tiny"
    And I click the delete button on the last squirrel
    And I dismiss the popup
    Then the squirrel list contains "Plot Armor"
    When I click the delete button on the last squirrel
    And I accept the popup
    Then the squirrel list does not contain "Plot Armor"

Scenario: Squirrels remember how big they are
    When I add a squirrel named "Big Boy" with size "gigantic"
    Then the last squirrel has size "gigantic"
    When I click the delete button on the last squirrel
    And I accept the popup
    Then the squirrel list does not contain "Big Boy"

