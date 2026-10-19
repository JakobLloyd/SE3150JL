Feature: find out if it's Christmas or not

  Scenario: it ain't Christmas today
    When I open the url "https://isitchristmas.com"
    Then I expect that element "#answer" is visible
    And I expect that element "#answer" contains the text "NO"
    And I expect that the title is "Is it Christmas?"
