Feature: Squirreltown
  As a certified squirrel enjoyer
  I want to manage the squirrels in Squirreltown
  So that every squirrel has a place in town

  Background:
    Given I open the url "http://localhost:8000"

  Scenario: The town welcomes visitors with its name
    Then I expect that the title is "Squirreltown"
    And I expect that element "h1" contains the text "Welcome to Squirreltown"

  Scenario: The squirrel form stays out of the way until needed
    Then I expect that element "#squirrel-dialog" is not visible
    And I expect that element "#add-button" is visible
    And I expect that element "#add-button" is enabled

  Scenario: The plus button opens a clean squirrel form
    When I click on the element "#add-button"
    Then I expect that element "#squirrel-dialog" is visible
    And I expect that element "#dialog-title" contains the text "Add Squirrel"
    And I expect that the attribute "value" from element "#squirrel-name-input" is ""
    And I expect that the attribute "value" from element "#squirrel-size-input" is ""

  Scenario: A visitor can cancel a squirrel they have not finished entering
    When I click on the element "#add-button"
    And I set "Temporary Squirrel" to the inputfield "#squirrel-name-input"
    And I set "small" to the inputfield "#squirrel-size-input"
    And I click on the element "#cancel-button"
    Then I expect that element "#squirrel-dialog" is not visible
    When I click on the element "#add-button"
    Then I expect that the attribute "value" from element "#squirrel-name-input" is ""
    And I expect that the attribute "value" from element "#squirrel-size-input" is ""

  Scenario: A new squirrel can join and then leave the town
    When I click on the element "#add-button"
    And I set "Sir Nutsalot" to the inputfield "#squirrel-name-input"
    And I set "very large" to the inputfield "#squirrel-size-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Sir Nutsalot']" to exist
    And I expect that element "#squirrels-list" contains the text "Sir Nutsalot"
    When I click on the element "//li[div='Sir Nutsalot']//button[contains(@class,'fa-trash')]"
    Then I expect that a confirmbox contains the text "Are you sure you want to delete Sir Nutsalot?"
    When I accept the confirmbox
    Then I wait on element "//li[div='Sir Nutsalot']" to not exist

  Scenario: Dismissing a squirrel's removal confirmation keeps it in town
    When I click on the element "#add-button"
    And I set "Plot Armor" to the inputfield "#squirrel-name-input"
    And I set "tiny" to the inputfield "#squirrel-size-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Plot Armor']" to exist
    When I click on the element "//li[div='Plot Armor']//button[contains(@class,'fa-trash')]"
    And I dismiss the confirmbox
    Then I expect that element "#squirrels-list" contains the text "Plot Armor"
    When I click on the element "//li[div='Plot Armor']//button[contains(@class,'fa-trash')]"
    And I accept the confirmbox
    Then I wait on element "//li[div='Plot Armor']" to not exist

  Scenario: The town remembers a squirrel's size
    When I click on the element "#add-button"
    And I set "Big Boy" to the inputfield "#squirrel-name-input"
    And I set "gigantic" to the inputfield "#squirrel-size-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Big Boy']" to exist
    And I expect that element "//li[div='Big Boy']/div[@class='size']" contains the text "gigantic"
    When I click on the element "//li[div='Big Boy']//button[contains(@class,'fa-trash')]"
    And I accept the confirmbox
    Then I wait on element "//li[div='Big Boy']" to not exist

  Scenario: The edit form remembers a squirrel's current details
    When I click on the element "#add-button"
    And I set "Chonky Norris" to the inputfield "#squirrel-name-input"
    And I set "legendary" to the inputfield "#squirrel-size-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Chonky Norris']" to exist
    When I click on the element "//li[div='Chonky Norris']//button[contains(@class,'fa-pencil')]"
    Then I expect that element "#dialog-title" contains the text "Edit Squirrel"
    And I expect that the attribute "value" from element "#squirrel-name-input" is "Chonky Norris"
    And I expect that the attribute "value" from element "#squirrel-size-input" is "legendary"
    When I click on the element "#cancel-button"
    And I click on the element "//li[div='Chonky Norris']//button[contains(@class,'fa-trash')]"
    And I accept the confirmbox
    Then I wait on element "//li[div='Chonky Norris']" to not exist

  Scenario: A squirrel can change its name and keep its place in town
    When I click on the element "#add-button"
    And I set "Gary" to the inputfield "#squirrel-name-input"
    And I set "medium" to the inputfield "#squirrel-size-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Gary']" to exist
    When I click on the element "//li[div='Gary']//button[contains(@class,'fa-pencil')]"
    And I set "Gary but evil" to the inputfield "#squirrel-name-input"
    And I click on the element "#save-button"
    Then I wait on element "//li[div='Gary but evil']" to exist
    And I wait on element "//li[div='Gary']" to not exist
    When I click on the element "//li[div='Gary but evil']//button[contains(@class,'fa-trash')]"
    And I accept the confirmbox
    Then I wait on element "//li[div='Gary but evil']" to not exist

  Scenario: An untouched squirrel form can be opened and abandoned safely
    When I click on the element "#add-button"
    Then I expect that element "#squirrel-dialog" is visible
    And I expect that the attribute "value" from element "#squirrel-name-input" is ""
    And I expect that the attribute "value" from element "#squirrel-size-input" is ""
    When I click on the element "#cancel-button"
    Then I expect that element "#squirrel-dialog" is not visible
