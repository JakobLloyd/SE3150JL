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

